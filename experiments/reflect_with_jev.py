#!/usr/bin/env python3
"""
reflect_with_jev.py
使用官方 JevClient 规范，调用 JEV 对当前 AdgaiWalker 进行系统性反思。
"""

import json
from jev_client import JevClient, Choice, Score, Noul

API_KEY = "apikey_2998e6693e0329444758839b8e9f443cf4e_b83254734358781cd5052308f8a0426736d50140c91fe368289899f68461840e"

STATE_CONTEXT = """
【AdgaiWalker 当前技术现状与改造回顾】
1. 架构定位：Walker 是个人数字工作站（iwalk.pro），采用「如无必要，勿增实体」哲学，全站基于 SQLite Native 与 NestJS + React。
2. JEV 赋能现状：
   - 实现了 JevFastPathService（门控路由器），拦截 4 种意图：日常打招呼、询问站主Dora背景、行动卡点导流/tools、提示词注入防御。
   - 客户端目前通过公网访问海外 TypeSafe AI API，单次网络往返约 1200ms~1600ms。
   - 与本地 DeepSeek 大模型分工：JEV 负责 System One 快思考，未命中时放行至 DeepSeek 慢思考。
3. 访客配额管理现状：
   - 全局将访客配额从 1 调整到 15 次。
   - 在 Admin 工作台新增了可实时调控配额、快捷预设与一键清空重置的面板。
   - 目前访客不管问“你好”还是复杂分析，都在公共会话中消耗 1 次额度。
"""

def main():
    client = JevClient(api_key=API_KEY)

    questions = {
        # 维度 1：配额正义性（打招呼是否应该白嫖/免扣额度？）
        "fast_path_should_exempt_quota": Noul(
            "被 JEV Fast Path 毫秒级拦截的轻量请求（如日常打招呼、安全拒绝），是否应当免除消耗访客宝贵的 15 次深度大模型问答额度？"
        ),

        # 维度 2：是否应当引入客户端/内存级 0ms 零延迟极速缓存
        "should_add_zero_latency_cache": Noul(
            "对于最常见的固化问候（如纯文本'你好'、'hi'），是否应在请求海外 JEV 之前加入本地内存/正则 0ms 直出层以消除 1.2s 的跨国网络延迟？"
        ),

        # 维度 3：是否需要继续扩充意图维度
        "should_expand_commercial_intent": Noul(
            "是否应该扩充 JEV 意图识别，例如增加'商业/咨询合作'、'精选文章推荐'等直接赋能站主 Dora 变现与内容曝光的意图？"
        ),

        # 维度 4：管理端是否应当提供 JEV 投资回报率（ROI）可视化看板
        "should_visualize_jev_roi": Noul(
            "在 Admin 工作台设置页，是否应当加入 JEV 拦截数据看板（如：替站主拦截了多少次大模型调用、节省了多少 Token 与成本、平均响应耗时）？"
        ),

        # 维度 5：最具紧迫性与性价比的下一阶段改进方向（单选判决）
        "highest_priority_improvement": Choice(
            "在现有 Walker 系统中，接下来最具实战价值和用户体验提升的改进方向是哪个？",
            {
                "quota_differentiation": "配额差异化：打招呼/FAQ 不扣除珍贵的深度 LLM 额度，只有复杂卡点才扣除",
                "zero_latency_cache": "本地极速缓存：对高频简单打招呼纯本地 0ms 返回，避免跨国网络往返",
                "intent_expansion": "意图扩充：新增合作意向与文章推荐两大商业与内容闭环路由",
                "admin_roi_observability": "数据看板：在管理后台直观展示 JEV 带来的 Token 节省与成本拦截数据"
            }
        ),

        # 维度 6：整体架构成熟度评分（1-5 阶梯）
        "architecture_maturity_rating": Score(
            "对当前 JEV Fast Path 与 DeepSeek 慢思考结合的 System 1 + System 2 架构在可用性与优雅度上打分：",
            [
                "1级 - 玩具 Demo，极度脆弱，不具备容错",
                "2级 - 初步打通，但主备链路高度耦合且容易误伤",
                "3级 - 架构清晰解耦，具备基本 fail-open 容错与门控分流",
                "4级 - 生产级完备，具备毫秒级响应、缓存、统计与细粒度配额",
                "5级 - 行业标杆级自治架构，自愈、自标定且全自动演进"
            ]
        )
    }

    print("🚀 正在呼叫 TypeSafe JEV System One 决策引擎进行技术反思...")
    result = client.decide(state=STATE_CONTEXT, questions=questions)
    
    print("\n" + "="*50)
    print("🎯 JEV 决策与反思评估结果：")
    print("="*50)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    with open("jev_reflection_eval.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
