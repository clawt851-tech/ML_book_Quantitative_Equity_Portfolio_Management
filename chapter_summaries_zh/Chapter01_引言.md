# 第1章 引言：信念、风险与流程 (Introduction: Beliefs, Risk, and Process)

## 1.1 章节概述

本章为全书的开篇，介绍量化股票投资组合管理（Quantitative Equity Portfolio Management, QEPM）的三大支柱：
1. **信念 (Beliefs)** ——投资经理对市场可获利性的认知体系。
2. **风险 (Risk)** ——把不确定性转化为风险/收益权衡的方法论。
3. **投资流程 (Process)** ——从研究到实盘的完整流程。

作者强调：现代量化投资是科学方法（数学、统计、运筹）与金融经济学的融合，量化经理（"quants"）通过系统化方式开发因子、构建组合、执行交易、监控风险。

## 1.2 核心要点

### 1.2.1 信念 (BELIEFS)

- 1950 年代之前，主流是"基本面选股"，其核心信念是"股市存在持续的赢家"。
- 学术研究和实践共同表明：在恰当考虑风险后，长期持续战胜市场极其困难。
- 量化投资的信念体系建立在三方面：
  - 市场存在系统性的、可被识别的"异象"（anomalies）。
  - 投资者行为偏差（behavioral biases）造成可预测的回报模式。
  - 通过严谨的统计与模型，可在风险控制下捕获 alpha。

### 1.2.2 风险 (RISK)

- 风险不仅是"亏损概率"，更是"未来回报相对于预期的偏离度"。
- 量化方法用以下统计度量风险：
  - 方差/标准差（波动率）
  - 跟踪误差 (Tracking Error)
  - 风险价值 (Value-at-Risk, VaR)
  - 风险贡献 (Risk Contribution / Risk Budget)

### 1.2.3 量化投资流程 (QUANTITATIVE INVESTMENT PROCESS)

完整流程包括：
1. 数据采集与清洗（Compustat、IBES、价格、风险模型）
2. Alpha 因子研究（Value, Quality, Momentum）
3. 因子组合（Multifactor Alpha Model）
4. 风险建模（Risk Model: 多因子结构）
5. 组合优化（均值-方差最优化）
6. 交易执行（最优交易策略，控制冲击成本）
7. 业绩归因与监控

### 1.2.4 信息捕捉 (INFORMATION CAPTURE)

量化经理通过三类信息流入构建 alpha：
- **基本面信息**：财报、行业数据。
- **市场信息**：价格、动量。
- **预期信息**：分析师预测（IBES）。

## 1.3 附录：心理学与行为金融

- **行为金融（Behavioral Finance）**:
  - 过度反应、反应不足
  - 处置效应（disposition effect）：盈利早抛、亏损死扛
  - 锚定与代表性启发（anchoring & representativeness heuristics）
- **行为模型**:
  - Barberis, Shleifer & Vishny (1998) 的 BSV 模型
  - Hong-Stein (1999) 的信息扩散模型
  - Daniel-Hirshleifer-Subrahmanyam (1998) 的过度自信模型

## 1.4 章节结构

后续章节按三部分组织：

**第一部分（理论基础）**：
- 第2章 投资组合理论（Markowitz, CAPM）
- 第3章 风险模型与风险分析（APT, MCR, VaR）

**第二部分（Alpha 因子）**：
- 第4章 Alpha 因子评估（IC, IR, FLAM）
- 第5章 量化因子（Value, Quality, Momentum）
- 第6章 估值技术与价值创造（DCF）
- 第7章 多因子 Alpha 模型

**第三部分（高级技术与实施）**：
- 第8章 组合换手率与最优 Alpha 模型
- 第9章 高级 Alpha 建模技术（Contextual, Nonlinear）
- 第10章 因子择时模型（Factor Timing）
- 第11章 组合约束与信息比
- 第12章 交易成本与组合实施

## 1.5 学习目标

读完本章后，读者应该能够：
- 理解量化股票投资的"哲学逻辑"。
- 区分"裸 IR"与"风险调整 IR"。
- 把每一类信息流（fundamental、market、expectational）映射到对应的 alpha 因子。
- 解释为何"行为金融"为大多数量化异象提供了经济解释。
