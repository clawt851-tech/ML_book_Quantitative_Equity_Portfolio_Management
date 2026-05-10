# 第4章 Alpha 因子评估 (Evaluation of Alpha Factors)

## 4.1 章节概述

本章建立 Alpha 因子的量化评估框架。核心是把 **超额收益、信息系数 (IC)、信息比 (IR)** 三者用数学方式联系起来，并指出"主动管理基本定律 (FLAM)"的应用条件。

## 4.2 核心要点

### 4.2.1 Alpha 业绩基准：比率 (Ratios)

- **Sharpe Ratio**: SR = (μ_p - r_f) / σ_p
- **Information Ratio**: IR = α / σ_α（超额收益/跟踪误差）
- **风险调整 IR (Risk-Adjusted IR)**: 用风险模型对 alpha 与 return 调整后再算 IC。

### 4.2.2 单期信息系数 (Single-Period IC)

- 原始 IC：IC = corr(F_t, R_t)，F 为预测，R 为实际收益。
- 风险调整 IC：把预测和实际收益都先对风险模型做"中性化"。

风险调整预测：F_t = (Σ⁻¹ f_t) · σ_i² 或类似形式。

风险调整收益：R_i = (r_i - β_i r_M)/θ_i (类似 z-score)。

### 4.2.3 单期超额收益的关键分解

α_t = IC_t · √N · σ_{model} · dis(R_t)

- **IC** = skill (技能)
- **√N** = breadth (覆盖广度)
- **σ_{model}** = risk budget (风险预算/跟踪误差)
- **dis(R_t)** = opportunity (机会, 横截面回报离散度)

### 4.2.4 多期 IR

公式 (4.33):

IR = E[IC_t] / std(IC_t)

#### Fundamental Law of Active Management (FLAM)

经典 Grinold 公式：IR = IC · √N（假设 std(IC_t) = 1/√N）。

**重要警告**：FLAM 只在 IC 的标准差等于纯采样误差 1/√N 时成立。实证表明：std(IC_t) 通常远高于 1/√N，因此 FLAM **会显著高估** IR。

### 4.2.5 三种风险概念

- **Risk-Model Tracking Error** σ_{model}：风险模型预测的跟踪误差。
- **Strategy Risk** std(IC_t)：策略本身 IC 的波动。
- **Active Risk** σ：组合实际跟踪误差。

公式 (4.32): σ = std(IC_t) · √N · σ_{model} · dis(R_t)

### 4.2.6 实证发现

- 风险模型（如 BARRA US E3）系统性低估 ex-post 跟踪误差约 50%（中位数 κ ≈ 1.5）。
- 调整后 σ*_{model} = σ_{model} / κ 给出更准确预估。

### 4.2.7 "纯化"Alpha (Purified Alpha)

把因子对所有风险因子做横截面回归，残差就是 purified alpha：

f_pure = f - n_0 - n_1 b_1 - ... - n_K b_K

性质：
- 在某些理想化风险模型下，purified alpha 与 risk-adjusted forecast 等价。
- 否则 purified alpha 仍带有特异风险偏差。

## 4.3 经验示例

- 60 个 alpha 因子分析（Russell 3000，1987–2003）。
- 平均 ex-post 跟踪误差 7.7%（目标 5%），范围 5.0%–13.1%。
- 表 4.2 对比 GP2EV 与 E2P 两个价值因子：GP2EV (IR=0.90) 显著优于 E2P (IR=0.38)。

## 4.4 关键公式速查

| 概念 | 公式 |
|------|------|
| 单期超额收益 | α_t ≈ IC_t · √N · σ_{model} · dis(R_t) |
| 跟踪误差 | σ = std(IC_t) · √N · σ_{model} · dis(R_t) |
| 信息比 | IR = E[IC]/std(IC) |
| FLAM | IR = IC · √N (仅理想情形) |
| 风险模型偏差 | κ = std(IC)·√N ≈ σ/σ_{model} |

## 4.5 学习目标

- 区分 "原始 IC" 和 "风险调整 IC"。
- 推导 α = IC·√N·σ·dis(R) 分解。
- 理解 FLAM 的局限。
- 应用 κ 来调整风险预测。
