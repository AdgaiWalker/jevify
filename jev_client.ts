/**
 * TypeSafe AI Jev TypeScript / Node.js Client (Zero Dependencies)
 * High-efficiency, typed client for System One non-autoregressive decision models.
 * Compatible with Node.js 18+, Bun, Deno, Next.js, NestJS, Cloudflare Workers.
 */

export interface QuestionPayload {
  type: 'choice' | 'score' | 'noul';
  instructions: string;
  criteria?: Record<string, string> | string[];
}

export function Choice(instructions: string, criteria: Record<string, string>): QuestionPayload {
  return { type: 'choice', instructions, criteria };
}

export function Score(instructions: string, criteria: string[]): QuestionPayload {
  return { type: 'score', instructions, criteria };
}

export function Noul(instructions: string): QuestionPayload {
  return { type: 'noul', instructions };
}

export interface JevDecisionResponse {
  model: string;
  answers: Record<
    string,
    {
      type: 'choice' | 'score' | 'noul';
      choice?: string;
      score?: number;
      noul?: number;
      confidence?: number;
      probabilities?: Record<string, number>;
      legend?: Record<string, string>;
    }
  >;
  usage?: {
    input_tokens: number;
    output_tokens: number;
  };
  _latency_ms?: number;
}

export interface JevClientOptions {
  apiKey: string;
  endpoint?: string;
  timeoutMs?: number;
}

export class JevClient {
  private readonly apiKey: string;
  private readonly endpoint: string;
  private readonly timeoutMs: number;

  constructor(options: JevClientOptions) {
    this.apiKey = options.apiKey?.trim() || '';
    this.endpoint = options.endpoint || 'https://api.typesafe.ai/v1/systemone';
    this.timeoutMs = options.timeoutMs ?? 3500;
  }

  isEnabled(): boolean {
    return Boolean(this.apiKey);
  }

  async decide(
    state: unknown,
    questions: Record<string, QuestionPayload>,
    model = 'jev-latest',
  ): Promise<JevDecisionResponse | null> {
    if (!this.isEnabled()) return null;

    const stateStr = typeof state === 'string' ? state : JSON.stringify(state);
    const payload = {
      model,
      state: stateStr,
      questions,
    };

    const t0 = Date.now();
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), this.timeoutMs);

      const res = await fetch(this.endpoint, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
          'User-Agent': 'TypeSafe-JevClient-TS/1.14.0',
        },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });

      clearTimeout(timer);

      if (!res.ok) {
        return null;
      }

      const data = (await res.json()) as JevDecisionResponse;
      data._latency_ms = Date.now() - t0;
      return data;
    } catch {
      // Fail-open: 网络超时或异常时静默放行，绝对不阻断主链路
      return null;
    }
  }
}
