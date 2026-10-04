# OTTO 多 Agent 研究试用

2026-10-04，在本机以“将 OTTO 的候选召回与排序思路迁移到另一个 session 推荐比赛”为真实研究请求，使用项目 Skill 和实际缓存资料完成前向试用。

## 实际完成的工作

- scout 建立比赛画像；evidence 与 validation 两个独立 Agent 并行审读作者正文并审查验证边界；transfer 与 reviewer 由宿主按前置结果继续研究。
- 五个角色输出均实际存在，带来源 ID、具体位置、claim type、未知项和交接说明；结果校验通过。这里有两个独立研究 Agent，五个角色不表示五个独立 Agent。
- 审读的 OTTO 缓存正文覆盖 Candidates、Reranker、Cv strategy 与 ablation study。按 LF 规范化后的正文 SHA256 与已记录来源匹配；Windows 原始 CRLF 字节的 hash 单独保留。
- 原帖引用的其他 CV 文章、附件图与作者代码没有在这次试用中读取，仍按未读处理。

## 交付的最小实验

| 实验 | 比较内容 | 需要先确认的条件 |
|---|---|---|
| E0 | 对目标数据的 session 前缀、可见历史与资产使用做泄漏审查 | 时间截点、split 单位、允许外部资料 |
| E1 | 固定候选生成，比较基线排序与一种新增排序阶段 | 目标官方指标、K、事件类型及预算 |
| E2 | 在固定排序策略上比较一种互补候选来源 | 候选覆盖、边际召回与最终指标分别记录 |

未命名目标比赛的官方指标、事件权重、数据边界和计算预算保留未知。作者报告中的数字不能作为这些实验的实际结果。这次没有训练、Kaggle 提交或性能验证。

## 试用发现与修复

一个真实研究 Agent 将 `handoff` 写成 JSON object，暴露出初始结果契约只列字段名、未明确字段类型的问题。保留原输出后，由该 Agent 改为字符串；项目同步补充类型契约和验证逻辑。

更新后的校验会拒绝数值 `statement`、object `locator` 与 list `handoff`。已有研究输出迁移到澄清后的契约并通过校验，迁移不宣称重新执行了研究。

本机执行记录、产物 hash 与原始负例保存在忽略的 `cache/forward-review/`，原始全文缓存未公开。公开说明只保留原创研究摘要与观察到的工具行为。

相关入口：[多 Agent 流程](../../skills/kaggle-solutions-skills/references/multi-agent-research.md)、[场景使用方式](team-research.md)、[原比赛](https://www.kaggle.com/competitions/otto-recommender-system)。
