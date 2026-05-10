# 第3章 风险模型与风险分析 (Risk Models and Risk Analysis)

## 3.1 章节概述

本章详细讨论 **多因子风险模型 (Multifactor Risk Models)**，并介绍三大风险分析工具：
- **MCR**：边际风险贡献 (Marginal Contribution to Risk)
- **CR**：风险贡献 (Risk Contribution / Risk Budget)
- **VaR**：风险价值贡献 (Contribution to Value at Risk)

## 3.2 核心要点

### 3.2.1 套利定价理论 APT 与多因子模型

回报通过 K 个因子建模：

r_i = α_i + b_{i,1}f_1 + ... + b_{i,K}f_K + ε_i

矩阵形式：

Σ = B Σ_f B' + S

其中：
- B: N×K 因子暴露矩阵
- Σ_f: K×K 因子协方差矩阵
- S: 对角矩阵（特异方差）

### 3.2.2 三类多因子模型

| 类型 | 代表 | 特点 |
|------|------|------|
| **宏观因子模型** | Chen-Roll-Ross (1986) | 因子=GDP增长、通胀、利率等可观测变量 |
| **基本面因子模型** | BARRA, Fama-French | 因子=市值、估值、动量、行业等 |
| **统计因子模型** | PCA-based (Connor-Korajczyk) | 因子由历史回报 PCA 得出 |

#### Fama-MacBeth 横截面回归

r_i^{t+1} = b_0 + b_1 I_{i,1}^t + ... + b_K I_{i,K}^t + ε_i

对每期回归一次，得到时间序列 {b_k^t}，再计算因子收益的协方差矩阵。

#### 时间衰减权重

最近一期权重为 1，半衰期 H = -ln(2)/lnω。

#### 主成分分析（统计因子）

- Σ = LPL'，L 为正交矩阵（特征向量），P=diag(λ_i)。
- 选前 K 个最大特征值即为统计因子。
- 缺点：缺乏经济解释，结构可能随时间漂移。

### 3.2.3 风险分析工具

#### A. 边际风险贡献 (MCR)

MCR_i = ∂σ/∂w_i = (Σw)_i / σ

向量形式：MCR = Σw / σ

可分解为系统/特异部分：
- MCR^{sys} = BΣ_f B'w / σ^{sys}
- MCR^{spec} = Sw / σ^{spec}

#### B. 组合 MCR (Group MCR)

对一组股票（如某行业）：MCR_S = Σ_{i∈S} w_i MCR_i。

#### C. 风险贡献 (Risk Contribution, CR)

CR_i = w_i · ∂σ/∂w_i

向量：CR = w ⊗ ∂σ/∂w = w ⊗ (Σw)/σ

性质：Σ CR_i = σ。

PCR_i = w_i (∂σ/∂w_i) / σ，Σ PCR_i = 1。

#### D. CR 的经济解释——Loss Contribution

PCL_i = E[w_i r_i | w'r = L] / L

定理（Qian 2006）：
- 当所有 μ_i = 0 或组合是均值-方差最优时，PCL = PCR。
- 否则 PCL ≈ PCR + D_i / L，其中 D_i 体现 MV 偏离度。
- 当损失 L 远大于 D_i 时，PCL ≈ PCR。

### 3.2.4 风险价值贡献 (Contribution to VaR)

VaR 定义：Prob(r ≤ VaR) = α (典型 5% 或 1%)

MCV_i = ∂VaR/∂w_i, CV_i = w_i ∂VaR/∂w_i

定理：MCV_i = E[r_i | r_p = VaR]，因此 CV_i 可解释为损失 L=VaR 时该股票的贡献。

VaR 计算方法：
- 解析法（正态假设）
- 蒙特卡罗模拟
- Cornish-Fisher 展开（近似处理偏度/峰度）

## 3.3 应用：风险预算 (Risk Budgeting)

通过 PCR 监控组合是否把风险"押对了地方"：
- 卖空组合：长头与空头各贡献多少风险。
- 多空对冲：系统风险和特异风险各占比例。
- 行业中性组合：每个行业贡献是否平衡。

## 3.4 学习目标

- 理解风险分解（系统+特异）的代数与几何意义。
- 计算 MCR, CR, PCR, PCL, MCV。
- 区分"风险贡献" vs "损失贡献"。
- 运用风险预算来校准组合配置。
