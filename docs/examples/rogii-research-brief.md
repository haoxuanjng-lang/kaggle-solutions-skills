# ROGII 解法研究交接示例

研究日期：2026-10-04（Asia/Shanghai）。上游档案 commit：
`6414951ae88d252a6c92d4489ba389b2b7cb40c7`。
本示例展示研究产出，没有训练、比赛提交或官方新成绩。

## 画像与来源

档案定位到 `rogii-wellbore-geology-prediction`，其指标字段写作 Mean Squared Error。
[作者冠军报告](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/writeups/1st-place-solution)
的实验表使用 RMSE。因此执行前要查官方 evaluation 与实际评分实现，明确 MSE/RMSE 的关系，
不能把历史档案里的名字直接当成本地函数。当前用户基线/数据/最新提交在本示例中未知。

实际已读：冠军报告正文，包括 Task Formulation and Loss、Features、XY Neighbor Information、
Ensemble 和 What didn't work。作者训练仓库和推理 notebook 仅从正文发现，未在此示例重跑。
正文 hash 与 read time 保存在 knowledge 的 `sources.json` 中 `rogii` 记录。

## 改变决策的观察

| 决定 | 作者报告 | 迁移条件与风险 |
|---|---|---|
| 回归重构为二维对齐 | U-Net 输出 typewell × horizontal-well 概率图，再得到期望 TVT 路径 | 目标确实是参考序列对齐；网格范围可能截断路径 |
| 物理与辅助信号 | 使用 GR、几何、粒子滤波和 XY 邻域通道 | 必须按 held-out well 独立构造，不能引入目标井隐藏标签 |
| 解释 CV/LB 冲突 | XY 信息稳定改善作者本地 CV，但恶化公共 LB；作者分析邻域可靠性后仍信任 CV | “标签不一致”是作者归因，尚未由本项目验证 |
| 按可靠性选择模型 | 对没有可靠 XY 信息的井使用无 XY 模型 | 路由统计应只依赖可见输入，并在训练内确定 |
| 保留有用的弱成员 | PF 通道不再改善最强单模型，却用于集成多样性 | 需要实测边际集成收益，而不是只看单模型分数 |

作者最终表报告：CV 4.627、public LB 5.980、private LB 5.639，表中按 RMSE 解释。
这些是作者历史报告，不能当成我们的复现结果或当前线上基线。

## 可检验的方向

1. 先核对现有 baseline 与数据划分：当前最新源版本、按井划分、评分公式、可见前缀与隐藏区域。
2. 如果当前是直接回归，固定 split 和预算，比较粗分辨率对齐概率图；查看整体指标及网格边界错误。
3. 在同一基础模型上只增加一种辅助通道，单独记录误差分组；不要把全部冠军特征一次加入。
4. 若辅助信息覆盖不稳定，比较固定全局集成与输入可靠性路由；同时看有/无可靠邻域的子组。

资源成本在读取当前代码前保持未知。这些实验方向应交给用户选定的比赛 workflow 和当前
项目要求；本简报不自行定义新的提交资格，也不替代官方计分。

## 对照的相似历史问题

[M5 冠军报告](https://www.kaggle.com/competitions/m5-forecasting-accuracy/discussion/163684)
说明不同时间窗口下递归/非递归模型互补；可借鉴“按结构和子组比较”的研究方法，不能照搬销量预测
的 folds 和损失。[RSNA 冠军报告](https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/540091)
说明上游估计误差需要在下游训练体现；只有当 ROGII 的辅助通道也来自估计模型时才有迁移价值。
