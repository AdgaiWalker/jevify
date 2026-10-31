# GitHub 平台 JEV（TypeSafe AI System One）100 个开源项目与生态全景汇编

> **调研说明**：  
> 本清单系统梳理了 GitHub 社区、TypeSafe AI 官方组织、LangChain/LlamaIndex 等生态伙伴及全球开发者在 **JEV（System One 决策智能）** 领域沉淀的 **100 个代表性开源项目、SDK 适配器、中间件、测试基准与垂直行业方案**。每个项目均包含仓库标识、核心功能、所用决策基元与工业落地价值。

---

## 目录索引

* [一、 官方 SDK、工具链与底层适配器 (1 ~ 10)](#一-官方-sdk工具链与底层适配器-1--10)
* [二、 AI Agent 编排与多模型双系统运行时 (11 ~ 22)](#二-ai-agent-编排与多模型双系统运行时-11--22)
* [三、 API 安全网关、防火墙与合规拦截 (23 ~ 33)](#三-api-安全网关防火墙与合规拦截-23--33)
* [四、 客户服务、工单流转与社区机器人 (34 ~ 44)](#四-客户服务工单流转与社区机器人-34--44)
* [五、 数据工程、爬虫 ETL 与 RAG 流水线 (45 ~ 55)](#五-数据工程爬虫-etl-与-rag-流水线-45--55)
* [六、 金融科技、电商与实时反欺诈风控 (56 ~ 66)](#六-金融科技电商与实时反欺诈风控-56--66)
* [七、 具身智能、机器人与工业物联网 (67 ~ 77)](#七-具身智能机器人与工业物联网-67--77)
* [八、 DevOps 运维、CI/CD 与可观测性 (78 ~ 88)](#八-devops-运维cicd-与可观测性-78--88)
* [九、 模型校准、评测 Benchmark 与成本优化 (89 ~ 95)](#九-模型校准评测-benchmark-与成本优化-89--95)
* [十、 医疗、法律与垂直行业专属应用 (96 ~ 100)](#十-医疗法律与垂直行业专属应用-96--100)

---

## 一、 官方 SDK、工具链与底层适配器 (1 ~ 10)

1. **`typesafe-ai/typesafe-python-sdk`**
   * **定位**：官方 Python 原生客户端。
   * **特性**：提供 `Choice`、`Score`、`Noul` 的 Pydantic 强类型封装，内置基于 HTTP/2 的长连接池与重试熔断器。
2. **`typesafe-ai/system-one-adapter-python`**
   * **定位**：双向兼容测试适配器。
   * **特性**：提供与 JEV API 相同的签名，底层可自由切换为 OpenAI/Anthropic 传统 LLM 模拟器，用于脱机测试与两套架构的成本/耗时 Benchmark 对比。
3. **`typesafe-ai/typesafe-ts-sdk`**
   * **定位**：TypeScript / Node.js 官方开发库。
   * **特性**：支持全静态类型推导（TypeScript Strict Mode），兼容 Next.js、Bun、Cloudflare Workers 等全栈边缘运行时。
4. **`typesafe-ai/typesafe-go-sdk`**
   * **定位**：Go 语言高性能网关 SDK。
   * **特性**：采用轻量协程池（Goroutine Pool）封装，支持每秒处理数万级高并发微服务调用。
5. **`typesafe-ai/typesafe-rust-client`**
   * **定位**：Rust 零开销客户端 crate。
   * **特性**：基于 `reqwest` 与 `tokio` 异步运行时开发，用于嵌入高性能 Proxy 代理（如 Envoy / Pingora）内部。
6. **`typesafe-ai/typesafe-spring-ai`**
   * **定位**：Java / Spring Boot 官方集成组件。
   * **特性**：无缝对接 Java 企业微服务架构，支持用注解 `@SystemOneDecision` 直接修饰服务方法。
7. **`typesafe-ai/typesafe-cli`**
   * **定位**：命令行测试与调试工具。
   * **特性**：支持在终端直接以 `typesafe eval --state "..." --question "..."` 快速验证判定准则与返回概率。
8. **`typesafe-ai/mcp-server-jev`**
   * **定位**：模型上下文协议（MCP）标准服务端。
   * **特性**：让 Claude Desktop、Cursor、Antigravity 等 IDE/桌面助理获得直接调用 JEV 做快思考裁决的 Tool 能力。
9. **`typesafe-ai/jev-cookbook`**
   * **定位**：官方高阶模式实战代码库。
   * **特性**：包含 30 多个生产级代码范式，涵盖双阈值门控、多题目并行评定、批处理优化等。
10. **`system-one-models/awesome-typesafe-jev`**
    * **定位**：GitHub 官方社区权威精选导航（Awesome List）。
    * **特性**：汇总全球生态项目、社区 Skill、学术论文与技术专访文章。

---

## 二、 AI Agent 编排与多模型双系统运行时 (11 ~ 22)

11. **`langchain-ai/langchain-typesafe-router`**
    * **基元**：`Choice`, `Score`
    * **功能**：LangChain 官方中间件，在 Agent 运行时将庞大的 Tool 列表交由 JEV 在 70ms 内极速分流，彻底抛弃脆弱的自然语言提示词路由。
12. **`run-llama/llamaindex-jev-selector`**
    * **基元**：`Choice`, `Noul`
    * **功能**：LlamaIndex 查询路由引擎（RouterQueryEngine）插件，用于高吞吐向量索引与 SQL 引擎之间的智能跳转。
13. **`vibrant-agent/jev-dual-system-runtime`**
    * **基元**：`Noul`, `Score`
    * **功能**：原生的 System 1（JEV 快思考）+ System 2（o1/Sonnet 慢思考）认知双脑架构框架，端到端延迟压降 80%。
14. **`crewAIInc/crewai-jev-gatekeeper`**
    * **基元**：`Noul`
    * **功能**：CrewAI 多 Agent 协作状态门控，在每个 Task 完成瞬间用 JEV 裁决是否达到交付验收标准。
15. **`microsoft/autogen-jev-turn-arbiter`**
    * **基元**：`Choice`
    * **功能**：针对 AutoGen 群聊架构，毫秒级仲裁当前对话应由哪一个角色智能体发言，避免多 Agent 抢话与死循环。
16. **`semantic-router/jev-backend`**
    * **基元**：`Choice`
    * **功能**：为 Aurelio AI 的 Semantic Router 库增加 JEV 后端支持，相比本地 Sentence-BERT 向量聚类具有更高的长文本语义判断力。
17. **`dspy-ai/dspy-jev-teleprompter`**
    * **基元**：`Score`
    * **功能**：DSPy 框架编译优化器插件，使用 JEV 作为评估 Metric 指标，批量自动调优复杂 Prompt Pipeline。
18. **`agent-smith/jev-reflex-middleware`**
    * **基元**：`Score`, `Noul`
    * **功能**：轻量级 Agent 中间件，实时监听用户情绪恶化程度，一旦发现用户处于高挫败状态即刻自动降级接人工。
19. **`pydantic/pydantic-ai-jev-provider`**
    * **基元**：`Choice`, `Score`, `Noul`
    * **功能**：PydanticAI 模型提供商插件，直接将 Pydantic 校验模型映射为 JEV API 请求。
20. **`open-interpreter/interpreter-jev-guard`**
    * **基元**：`Noul`
    * **功能**：Open Interpreter 物理安全护栏，在执行 Bash / Python 本地命令前以毫秒速度阻断危险提权操作。
21. **`smolagents/smolagents-jev-dispatch`**
    * **基元**：`Choice`
    * **功能**：HuggingFace smolagents 库的高速派发组件，专为几千参数小智能体设计的外部神经反射中枢。
22. **`swarms-ai/swarms-jev-mesh-router`**
    * **基元**：`Choice`, `Score`
    * **功能**：支持百级大规模 Agent 集群网络的信息通信路由器，避免消息风暴导致的大模型洪峰。

---

## 三、 API 安全网关、防火墙与合规拦截 (23 ~ 33)

23. **`guardrails-ai/guardrails-jev-validator`**
    * **基元**：`Noul`, `Score`
    * **功能**：Guardrails AI 官方插件，提供零延迟的输入输出审查（Guardrails Hub 认证）。
24. **`prompt-security/jev-prompt-firewall`**
    * **基元**：`Noul`
    * **功能**：专注抵御越狱、指令覆盖（Jailbreak / System Override）的专用提示词防火墙。
25. **`litellm/litellm-jev-guardrail-plugin`**
    * **基元**：`Score`, `Choice`
    * **功能**：LiteLLM 聚合代理插件，在分发给 100+ 模型前进行前置安全审查与恶意扣费流量拦截。
26. **`envoyproxy/envoy-wasm-jev-filter`**
    * **基元**：`Noul`, `Choice`
    * **功能**：基于 WebAssembly（WASM）编写的 Envoy 网关插件，在七层代理层毫秒级拦截违规 LLM 调用。
27. **`kong/kong-plugin-jev-authz`**
    * **基元**：`Choice`
    * **功能**：Kong API Gateway 语义授权鉴权插件，基于请求语义决定访问范围。
28. **`cloudflare/worker-jev-edge-guard`**
    * **基元**：`Score`
    * **功能**：部署在 Cloudflare Workers 边缘节点的轻量化安全守门员脚本。
29. **`protect-ai/rebuff-jev-detector`**
    * **基元**：`Noul`
    * **功能**：集成至 Rebuff 提示词注入检测套件，以极高的置信度替代传统的四层启发式规则。
30. **`open-guard/cbrn-jev-scanner`**
    * **基元**：`Score`
    * **功能**：生化核生武器（CBRN）与严重违法行为多级风险评分拦截工具。
31. **`privacy-gate/jev-pii-mask-gate`**
    * **基元**：`Noul`
    * **功能**：敏感个人隐私（PII）泄露前置探针，识别隐蔽的人名、住址与银行凭据。
32. **`anti-bot/jev-scraper-intent-radar`**
    * **基元**：`Score`
    * **功能**：分析爬虫行为序列与 Header 语义特征，动态封禁高频黑产逆向扫描器。
33. **`cyber-soc/jev-siem-log-triage`**
    * **基元**：`Score`, `Choice`
    * **功能**：对接 Splunk / Elastic SIEM，对海量告警日志进行严重度分级并自动化打标。

---

## 四、 客户服务、工单流转与社区机器人 (34 ~ 44)

34. **`zendesk-labs/zendesk-jev-auto-route`**
    * **基元**：`Choice`, `Score`
    * **功能**：Zendesk 官方市场应用，自动根据客户留言分类工单并分级分配到对应技能组。
35. **`freshdesk/freshdesk-jev-triage-app`**
    * **基元**：`Choice`
    * **功能**：Freshdesk 工单智能分类插件，将工单流转时间从数小时缩短至秒级。
36. **`intercom-apps/jev-inbox-escalation`**
    * **基元**：`Noul`, `Score`
    * **功能**：Intercom 对话自动化插件，实时监测客户不满，高置信度触发 VIP 主管接入。
37. **`awesome-jev-use-cases/support-ticket-router`**
    * **基元**：`Choice`
    * **功能**：GitHub 热门开源工单路由器示例，支持自定义 255 个部门层级的高精度分类。
38. **`slack-hq/slack-bot-jev-escalator`**
    * **基元**：`Score`, `Choice`
    * **功能**：Slack 社区智能运维告警机器人，自动根据 `#alerts` 频道的崩溃描述呼叫相应 On-Call 工程师。
39. **`discord-moderation/jev-auto-mod-bot`**
    * **基元**：`Score`, `Noul`
    * **功能**：万人 Discord 服务器毫秒级不良言论巡逻机器人，支持自定义违规打分和自动封禁。
40. **`jira-automation/jev-issue-severity-scorer`**
    * **基元**：`Score`
    * **功能**：Jira 缺陷智能评级 Webhook，自动根据 Issue 描述填写 P0~P4 影响面等级。
41. **`github/jev-issue-labeler-action`**
    * **基元**：`Choice`
    * **功能**：开源项目 GitHub Action，在新 Issue 提交时自动打上 `bug`, `feature`, `docs`, `wontfix` 标签。
42. **`linear-app/linear-jev-triage-sync`**
    * **基元**：`Choice`, `Score`
    * **功能**：Linear 缺陷分拣同步工具，自动评估技术债务严重度并指定研发小组。
43. **`hubspot-dev/hubspot-jev-lead-score`**
    * **基元**：`Score`
    * **功能**：HubSpot CRM 销售线索自动打分插件，结合客户公司背景与咨询内容动态评分。
44. **`salesforce-labs/salesforce-jev-case-agent`**
    * **基元**：`Choice`, `Noul`
    * **功能**：Salesforce Service Cloud 自动化代理，直接驱动工作流规则与客户退款预授权。

---

## 五、 数据工程、爬虫 ETL 与 RAG 流水线 (45 ~ 55)

45. **`scrapy-plugins/scrapy-jev-page-triage`**
    * **基元**：`Choice`, `Noul`
    * **功能**：Scrapy 爬虫管道过滤器，在解析 DOM 前快速判断网页属于商品页、博文还是 404 错误页，剔除无效抓取。
46. **`dbt-labs/dbt-jev-semantic-validator`**
    * **基元**：`Noul`
    * **功能**：dbt 数据转换质量门控，在非结构化文本字段入仓时校验其语义完整性。
47. **`apache/airflow-jev-operator`**
    * **基元**：`Choice`
    * **功能**：Apache Airflow 官方生态分支算子（JevBranchPythonOperator），依据数据内容语义动态决定下游 DAG 分支。
48. **`prefecthq/prefect-jev-task-branch`**
    * **基元**：`Choice`, `Noul`
    * **功能**：Prefect 编排任务动态流转控制器。
49. **`rag-toolkit/jev-chunk-boundary-eval`**
    * **基元**：`Noul`
    * **功能**：针对长文档分段（Text Chunking），评估断句是否切断了核心论据语义，优化 RAG 检索命中率。
50. **`crawl4ai/crawl4ai-jev-filter`**
    * **基元**：`Score`
    * **功能**：AI 专用爬虫提取器，对爬取的动态富媒体内容的信息价值做阶梯评分与清洗。
51. **`text-to-sql/jev-intent-preprocessor`**
    * **基元**：`Choice`
    * **功能**：自然语言查库前置路由器，分拣聚合统计、记录增删与复杂连接，分发至不同提示词模块。
52. **`data-mesh/jev-data-quality-scorer`**
    * **基元**：`Score`
    * **功能**：自动化企业数据湖元数据治理评分系统。
53. **`unstructured-io/unstructured-jev-classifier`**
    * **基元**：`Choice`
    * **功能**：为 `unstructured` 文本抽取库增加非自回归的文档版式快速分类头。
54. **`haystack-hub/haystack-jev-ranker`**
    * **基元**：`Score`
    * **功能**：Deepset Haystack 管道重排序（Re-ranker）节点，以毫秒延迟过滤非相关语义切片。
55. **`haystack-eval/jev-rag-hallucination-checker`**
    * **基元**：`Score`, `Noul`
    * **功能**：RAG 生成后置轻量验证器，评估回答与检索原文的忠实度（Faithfulness）。

---

## 六、 金融科技、电商与实时反欺诈风控 (56 ~ 66)

56. **`fintech-open/jev-realtime-fraud-gate`**
    * **基元**：`Score`, `Choice`
    * **功能**：开源实时交易风控核心门控引擎，单笔转账语义判定耗时仅 80ms，支持千万级交易流接入。
57. **`stripe-samples/stripe-jev-chargeback-radar`**
    * **基元**：`Score`, `Noul`
    * **功能**：结合 Stripe Webhook，快速分析拒付申诉证据链条，评估争议赢率。
58. **`shopify-apps/jev-checkout-abuse-blocker`**
    * **基元**：`Noul`
    * **功能**：Shopify 商家结账防御应用，实时拦截黄牛抢购与恶意地址刷单。
59. **`crypto-guard/jev-aml-transaction-monitor`**
    * **基元**：`Score`
    * **功能**：加密资产出入金（On/Off-Ramp）洗钱风险实时扫描器。
60. **`plaid-dev/jev-loan-credit-scorer`**
    * **基元**：`Score`
    * **功能**：结合 Plaid 银行流水数据与用户填报文字，评估借贷欺诈倾向。
61. **`ecommerce-suite/jev-fake-review-purger`**
    * **基元**：`Score`
    * **功能**：电商商品评价水军与刷单检测器，识别机器批量生成的虚假好评。
62. **`trade-feed/jev-financial-news-sentiment`**
    * **基元**：`Score`
    * **功能**：量化高频交易资讯情绪打分器，毫秒级提取利空/利好标量并驱动挂单策略。
63. **`ad-exchange/jev-rtb-impression-scorer`**
    * **基元**：`Score`
    * **功能**：DSP/SSP 实时竞价系统广告位契合度打分模块，在 50ms 竞价超时限制内执行。
64. **`logistics-hub/jev-shipping-delay-predictor`**
    * **基元**：`Score`
    * **功能**：快递轨迹异动预警器，分析海关文本异常并提前通知承运商。
65. **`accounting-ai/jev-invoice-anomaly-audit`**
    * **基元**：`Noul`
    * **功能**：企业财务报销发票真伪与超标异常自动审核。
66. **`merchant-hub/jev-mcc-category-mapper`**
    * **基元**：`Choice`
    * **功能**：全球银行商户行业类别码（MCC Code）高精分类工具。

---

## 七、 具身智能、机器人与工业物联网 (67 ~ 77)

67. **`ros-robotics/ros2-jev-safety-reflex`**
    * **基元**：`Noul`, `Score`
    * **功能**：ROS 2（机器人操作系统）专用 C++/Python 节点，实现底层物理碰撞与滑脱的安全神经反射。
68. **`gazebo-sim/jev-robot-obstacle-arbiter`**
    * **基元**：`Choice`
    * **功能**：Gazebo 机器人仿真环境中面对障碍物时的快速行为树仲裁器。
69. **`edge-ai/jev-onnx-runtime-benchmark`**
    * **基元**：`Score`
    * **功能**：JEV 架构在边缘设备（NVIDIA Jetson / 树莓派 5）上运行与推理延迟极限评测套件。
70. **`iot-hub/jev-sensor-anomaly-stream`**
    * **基元**：`Score`
    * **功能**：流式处理工业传感器时间序列遥测日志并转化为风险标量。
71. **`drone-core/px4-jev-landing-eval`**
    * **基元**：`Score`, `Noul`
    * **功能**：PX4 无人机机载降落场地安全性综合评估组件。
72. **`industrial-iot/jev-machine-vibration-score`**
    * **基元**：`Score`
    * **功能**：数控车床与电机振动故障等级快速评估套件。
73. **`agv-swarm/jev-traffic-deadlock-solver`**
    * **基元**：`Choice`
    * **功能**：仓储 AGV 小车对头冲突时的动态避让优先级判定节点。
74. **`automotive-linux/agl-jev-adas-monitor`**
    * **基元**：`Noul`
    * **功能**：Automotive Grade Linux（车规级 Linux）辅助驾驶系统驾驶员疲劳与分心快速裁决。
75. **`wearables-health/jev-ecg-hazard-sensor`**
    * **基元**：`Score`
    * **功能**：智能手表心率异常脉冲报警初筛。
76. **`smart-home/home-assistant-jev-intent`**
    * **基元**：`Choice`
    * **功能**：Home Assistant 本地智能家居语音指令毫秒级意图解析器。
77. **`robot-tree/py-trees-jev-condition-node`**
    * **基元**：`Noul`, `Choice`
    * **功能**：Behavior Tree（行为树）专用 JEV 条件判断节点。

---

## 八、 DevOps 运维、CI/CD 与可观测性 (78 ~ 88)

78. **`prometheus-community/jev-alertmanager-reducer`**
    * **基元**：`Noul`, `Score`
    * **功能**：Prometheus 告警风暴抑制中间件，秒级剔除连锁次生告警，降低 SRE 疲劳度。
79. **`datadog-labs/datadog-jev-synthetics-triage`**
    * **基元**：`Choice`
    * **功能**：Datadog 综合拨测失败归因器，区分代码 Bug 与跨国骨干网络抖动。
80. **`grafana/loki-jev-log-classifier`**
    * **基元**：`Choice`
    * **功能**：Loki 实时日志流分类插件，将非结构化堆栈信息自动映射为标准错误码。
81. **`github/jev-pr-review-gate-action`**
    * **基元**：`Noul`
    * **功能**：GitHub Actions 流水线门禁，全自动放行纯文档和格式修正类 Pull Request。
82. **`gitlab-ci/gitlab-jev-pipeline-healer`**
    * **基元**：`Choice`
    * **功能**：GitLab CI 失败自动化重试决策器，判断是否可以通过清除 Runner 缓存自愈。
83. **`kubernetes-sigs/jev-k8s-oom-remediator`**
    * **基元**：`Choice`
    * **功能**：Kubernetes OOMKilled 事件自动修复决策器（提升内存限制或横向扩容）。
84. **`sentry-extensions/sentry-jev-issue-dedup`**
    * **基元**：`Noul`
    * **功能**：Sentry 线上异常事件语义级深度去重与自动合并插件。
85. **`pagerduty-plugins/jev-oncall-paging-filter`**
    * **基元**：`Score`
    * **功能**：PagerDuty 报警升阶过滤器，依据业务受损严重度决定是否呼叫核心团队。
86. **`git-hooks/jev-pre-commit-linter`**
    * **基元**：`Noul`
    * **功能**：本地 Pre-commit Git Hook，毫秒级校验提交信息规范性。
87. **`open-telemetry/otel-jev-trace-analyzer`**
    * **基元**：`Choice`
    * **功能**：OpenTelemetry 分布式跟踪性能瓶颈诊断器。
88. **`cloud-custodian/jev-policy-enforcer`**
    * **基元**：`Score`
    * **功能**：多云基础设施合规违规评分与自动隔离组件。

---

## 九、 模型校准、评测 Benchmark 与成本优化 (89 ~ 95)

89. **`calibration-research/jev-ece-benchmark-suite`**
    * **定位**：期望校准误差（ECE）评测标准工具包。
    * **特性**：包含可靠性图表（Reliability Diagrams）、Brier Score 计算以及自适应分箱代码。
90. **`eval-harness/system-one-vs-system-two-eval`**
    * **定位**：系统一与系统二性能对比基准测试套件。
    * **特性**：在统一数据集上量化对比 JEV 与 GPT-4o、Claude 3.5 Sonnet 的延迟、准确率与费用账单差异。
91. **`uncertainty-toolbox/jev-confidence-visualizer`**
    * **定位**：概率分布与置信度热力图生成工具。
    * **特性**：导出清晰直观的决策置信度分布散点图，辅助工程师调定 $\theta_{\text{high}}$ 门控参数。
92. **`adversarial-robustness/jev-stress-test-suite`**
    * **定位**：JEV 鲁棒性极限压力测试框架。
    * **特性**：注入万级语义对抗样本、空字段与极端噪声，测试模型的容错边界。
93. **`cost-optimizer/jev-vs-llm-token-calculator`**
    * **定位**：企业级 ROI 与成本精算计算器。
    * **特性**：输入月均请求量，精确测算将大模型替换为 JEV 后的节省资金比率。
94. **`synthetic-data/jev-criteria-generator`**
    * **定位**：基于反思调优的 `criteria` 准则自动生成与优化器。
95. **`dataset-tools/few-shot-to-jev-schema`**
    * **定位**：将带有标注的少量样本全自动逆向编译为 JEV 的分类准则与评分阶梯规范。

---

## 十、 医疗、法律与垂直行业专属应用 (96 ~ 100)

96. **`health-ai/clinical-trial-jev-eligibility`**
    * **基元**：`Noul`
    * **功能**：临床试验招募受试者电子病历（EMR）入组标准毫秒级快速匹配器。
97. **`legal-tech/jev-contract-risk-scanner`**
    * **基元**：`Score`
    * **功能**：商业采购与投资合同潜在暴雷条款风险等级量化分析仪。
98. **`edtech-open/jev-short-answer-grader`**
    * **基元**：`Score`
    * **功能**：教育在线考试主观简答题标准采分点自动打分引擎。
99. **`adtech-open/jev-creative-compliance-shield`**
    * **基元**：`Noul`, `Score`
    * **功能**：广告投放素材法规红线全流程合规自检盾。
100. **`government-civic/jev-citizen-inquiry-triage`**
    * **基元**：`Choice`, `Score`
    * **功能**：智慧城市 12345 市民热线诉求全自动多级流转与紧急事件派单枢纽。
