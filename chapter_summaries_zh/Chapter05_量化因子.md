# 第5章 量化因子 (Quantitative Factors)

## 5.1 章节概述

本章详细介绍三大类核心量化因子：
1. **价值因子 (Value Factors)**
2. **质量因子 (Quality Factors)**
3. **动量因子 (Momentum Factors)**

并给出每类因子的定义、构造、历史业绩、宏观敏感度。

## 5.2 价值因子 (Value Factors)

### 5.2.1 八种代表性价值因子

| 简称 | 含义 |
|------|------|
| CFO2EV | 经营现金流 / 企业价值 |
| EBITDA2EV | EBITDA / 企业价值 |
| E2PFY0 | 滚动 12 月盈利收益率 |
| E2PFY1 | 下年预期盈利收益率 (IBES) |
| BB2P | 股票回购+股息 / 市值 |
| BB2EV | 净外部融资 / EV |
| B2P | 账面/市值 |
| S2EV | 销售额 / EV |

### 5.2.2 实证表现 (Russell 3000, 1986–2004)

- 现金流类（CFO2EV）IC=7.20%, IR=0.82——最强。
- 资产价值（B2P）IC=1.54%, IR=0.18——最弱。
- 高 90–95% 显著性水平的因子普遍。

### 5.2.3 关键设计考虑

- **Earnings Yield vs PE**：避免负盈利。
- **Peer Group**：行业内排名以减小行业偏置。
- **Stock vs Enterprise Ratios**：考虑财务杠杆。

### 5.2.4 宏观敏感度

- 价值策略在"市场下跌、利率上升、价值跑赢成长"时表现最佳。
- B2P 与 S2EV 适合做因子择时。

## 5.3 质量因子 (Quality Factors)

### 5.3.1 两大类质量信号

1. **业务竞争力 (Competitiveness)**
   - RNOA: Return on Net Operating Assets
   - CFROI: Cash Flow Return on Investment
   - OL: Operating Leverage
   - OLinc: Increase in Operating Leverage
2. **代理问题 (Agency Problem)**
   - WCinc: Working Capital Increase（应计盈余）
   - NCOinc: Net Noncurrent Operating Asset Increase
   - icapx, capxG: 资本支出过度
   - XF: 净外部融资
   - shareInc: 股本增发

### 5.3.2 关键账户恒等式

ΔNOA = ΔXF + NI = ΔWC + ΔNCO + ΔCASH

XF + RNOA = WCinc + NCOinc + ΔCASH/NOA

意义：现金的来源（业务/外部融资）与去向（流动资本/长期资本/现金账户）之间的会计平衡。

### 5.3.3 实证表现

- 质量因子整体 IR 高，IC 标准差小（更稳定，但不利于择时）。
- 竞争力因子（RNOA, CFROI, OL, OLinc）IC > 0，IR ≈ 0.4–1.1。
- 代理问题因子（WCinc, NCOinc, capxG, XF, shareInc）IC < 0，IR ≈ -0.4–-1.0。

### 5.3.4 非线性

- XF 关系大体线性（信息不对称效应）。
- icapx, capxG, WCinc 呈 **凹函数**：极端低值并不对应高回报，最佳是"温和保守"。

## 5.4 动量因子 (Momentum Factors)

### 5.4.1 三类动量

1. **价格动量 (Price Momentum)**
   - Ret9：过去 9 个月累计收益
   - Ret9Monx1：过去 9 个月（剔除最近 1 个月）
2. **盈利动量 (Earnings Momentum)**
   - EarnRev9：过去 9 个月分析师盈利预测修订
3. **长期成长 (Long-term Growth)**
   - LtgRev9：长期增长预测修订

### 5.4.2 时间序列自相关

- 价值因子自相关 ≈ 0.9（信息衰减慢，低换手）。
- 质量因子 ≈ 0.7–0.9。
- 动量因子 ≈ 0.4–0.6（信息衰减快，高换手）。

## 5.5 因子之间的相关性

- 价值因子之间 IC 相关性 60%–90%（多样化潜力小）。
- 价值与动量负相关（约 -0.5），是天然的分散组合。
- 价值与质量分类内部高相关，跨类相关较低。

## 5.6 学习目标

- 区分"基于股票"与"基于企业"的估值比率。
- 理解会计恒等式 ΔNOA = ΔXF + NI 的含义。
- 应用动量因子时考虑"剔除最近 1 个月"以减小反转噪声。
- 利用因子间负相关性提升组合 IR。
