/**
 * Quota Exemption Guard Pattern (TypeScript)
 *
 * Protects high-value business quota (e.g. 15 turns per visitor) from being
 * depleted by casual greetings or exploratory probing.
 */

import { FastPathGateway } from './3-tier-fastpath';

export interface UserRequest {
  userId: string;
  query: string;
}

export async function processRequestWithQuotaGuard(
  req: UserRequest,
  gateway: FastPathGateway,
  quotaManager: { isExhausted: (uid: string) => Promise<boolean>; consume: (uid: string) => Promise<boolean> },
  invokeSlowLLM: (q: string) => Promise<string>,
) {
  const cleanQuery = req.query.trim();

  // 1. Fast-Path 意图检测与额度豁免
  const fastPath = await gateway.check(cleanQuery);
  if (fastPath && fastPath.quotaExempt) {
    // 命中打招呼或轻量问答：直接返回，不扣减用户宝贵的配额！
    return {
      answer: fastPath.answer,
      quotaConsumed: false,
      latencyMs: fastPath.latencyMs,
    };
  }

  // 2. 真实复杂业务问题才检查并扣减配额
  if (await quotaManager.isExhausted(req.userId)) {
    throw new Error('Your question quota has been exhausted. Please upgrade or sign in.');
  }

  await quotaManager.consume(req.userId);

  // 3. 唤醒大模型进行慢思考
  const answer = await invokeSlowLLM(cleanQuery);
  return {
    answer,
    quotaConsumed: true,
  };
}
