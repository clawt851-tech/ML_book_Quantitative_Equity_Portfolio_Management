# 第6章 估值技术与价值创造 (Valuation Techniques and Value Creation)

## 6.1 章节概述

本章把"自下而上"的 DCF 估值方法系统地纳入量化框架，介绍：
- DCF 估值结构 (Operating Value, FCFF, Terminal Value)
- 业务经济建模 (RIC = profitability × scalability)
- 多路径 DCF (MDCF: Monte Carlo)
- 实例：Cheesecake Factory (CAKE)

## 6.2 估值框架 (Valuation Framework)

### 6.2.1 企业价值结构

EV = Operating Value + Excess Cash + Other Equity Investments
   - Market Value of Debt
   - Market Value of Preferred Stock
   - Minority Interests

Operating Value 又分：

OV = (WACC - g) / (WACC · (1+g)) 部分（已有业务）+ g·(1+WACC)/(WACC·(1+g)) 部分（增长）

例：g = 5%, WACC = 9% → 已有业务 42%，增长 58%。

### 6.2.2 自由现金流 (FCF)

- **FCFF (Free Cash Flow to Firm)**: 全体投资者可分配的现金流
- **FCFE (Free Cash Flow to Equity)**: 股东可分配现金流

FCFF = NOPAT - ΔCapital
ΔCAPITAL = ΔWC + ICAPEX + Δother investments

NOPAT = (Sales - COGS - SGA - DA)·(1 - tax rate)

### 6.2.3 业务经济模型——RIC 分解

**RIC = ΔNOPAT / ΔNOA = profitability × scalability**

- profitability = ΔNOPAT/ΔSales（边际利润率）
- scalability = ΔSales/ΔNOA（资产周转率）

进一步分解：

profitability = (1 - ΔCOGS/ΔSales - ΔSGA/ΔSales - ΔDA/ΔSales) · (1 - taxRate)

1/scalability = ΔWC/ΔSales + (CAPEX-DA)/ΔSales + Δother/ΔSales

### 6.2.4 公司公允价值

OV = S_0 (p̄ - g/s̄) (1+g) / (w - g)

灵敏度（数值示例：S=1, p=10%, s=2, g=5%, WACC=9%）：

| 输入 | 灵敏度 |
|------|--------|
| profitability | 13.33 |
| WACC | -25.00 |
| growth | 19.29 |
| sales | 1 |
| scalability | 0.17 |

### 6.2.5 资本成本 (WACC)

WACC = (k_s · S + k_b · (1-tax) · B + k_p · P) / V

- k_s = 股权成本（CAPM 或多因子模型）
- k_b = 债务成本（公司债券收益）
- k_p = 优先股成本

### 6.2.6 三阶段 DCF

1. **明确预测期 (Explicit Period)**：5–10 年明确预测。
2. **衰减期 (Fade Period)**：RIC → WACC，g → r_f。
3. **永续期 (Constant Growth Period)**：使用永续增长公式得 Terminal Value。

衰减公式：

RIC_{t+1} = (RIC_t - WACC)·F_t + WACC
g_{t+1} = (g_t - r_f)·F_t + r_f

F_t 为衰减函数（典型半衰期 6 年指数衰减）。

## 6.3 多路径 DCF (Multipath DCF)

- 单路径 DCF 的脆弱性：对参数高度敏感。
- 多路径 DCF：用 Monte Carlo 模拟 profitability/scalability/growth 等关键变量的随机过程。
- 输出：fair value 的概率分布而非单点估计。

## 6.4 案例：Cheesecake Factory (CAKE)

- WACC = 8.4%
- RIC = 13.8%（profit margin 7.3%, asset turnover 1.89）
- EVC = RIC - WACC = 5.4%
- 估值结果：Equity value $35.64/股 vs 市价 $37.95（被高估约 6%）。
- Operating Value 占企业价值 97%，其中 62% 来自未来增长。

## 6.5 学习目标

- 推导 OV = S₀(p̄-g/s̄)(1+g)/(w-g)。
- 拆分 RIC 为 profitability × scalability。
- 应用三阶段 DCF（explicit + fade + terminal）。
- 理解为何 WACC 是估值最敏感的输入。
