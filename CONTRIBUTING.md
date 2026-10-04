# 维护与贡献

## README 语言版本

`README.md` 是默认英文首页；`README.zh-CN.md`、`README.ja.md`、
`README.zh-TW.md` 分别提供简体中文、日语与繁体中文。修改功能介绍时同步四个版本的
安装命令、版本、知识统计、证据说明与语言切换链接；保留相同的导航 anchor。
README 的持续维护部分只介绍更新、审核与获取新版，调度、CI 矩阵和本机配置集中在
`docs/daily-maintenance.md`。文档尚未翻译时保留原链接，不伪装成已有本地化版本。

源目录是 `skills/kaggle-solutions-skills/`。安装目录是发布副本；在源目录修改，再校验和安装。
一个变更应说明它改变了哪个研究判断或修复了哪个可观察行为。

## 新资料与方法卡

1. 检索现有 sources/cards，确认不是重复内容。
2. 取得正文或相关代码，阅读决定所依赖的具体位置；记录 URL、时间、commit/hash、范围与作者。
3. 在 `sources.json` 注册来源，在 `patterns.json` 添加或修订卡片；字段按 skill 中的 schema。
4. 写清作者报告、自己的推断、实际重跑的区别。缺少消融/成本/分数就保留未知。
5. 给迁移假设配一个最小对照。新的事实约束可以修改旧卡；单次失败优先缩小条件。
6. 运行知识校验和相关测试，再更新版本与 changelog。

不要提交全文抓取缓存、访问 token、私有比赛数据、模型文件或未获许可的第三方代码。
来源链接、hash 和原创释义足够支持本知识库；复现证据可以保存在用户的私有执行项目。

## 索引更新

运行 `solutions.py refresh` 后审查 `last-refresh.json` 和 Git diff，尤其是删除、排名变化、指标
变更及源结构变更。refresh 只改档案，不改 curated files。相同 commit 不应产生内容变更。
如果上游结构变化，给 importer 增加针对实际变化的行为测试，避免默默丢字段或错判空值。

## 校验

```text
python skills/kaggle-solutions-skills/scripts/solutions.py validate
python -m unittest discover -s tests -v
python scripts/project.py check
```

结构/测试通过证明该版本能按测试场景工作；不证明方法卡在新比赛中有收益。
新增依赖、采集服务或搜索算法要附带可复查的实际理由。优先使用标准库与小型文件，保持
离线检索可用。不把个人过去的失败经验直接升级为每场比赛都必须遵守的额外门槛。
