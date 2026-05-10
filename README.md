# Quantitative Equity Portfolio Management — 学习资料

本目录包含 *Quantitative Equity Portfolio Management: Modern Techniques and Applications* (Qian, Hua, Sorensen, 2007) 的：

1. **每章中文详解笔记** (`chapter_summaries_zh/`)
2. **每章 Python 演示代码** (`chapter_codes/`)

## 章节索引

| 章 | 中文笔记 | Python Demo |
|---|---|---|
| 1 引言：信念、风险与流程 | [Chapter01_引言.md](chapter_summaries_zh/Chapter01_引言.md) | [chapter01_introduction_demo.py](chapter_codes/chapter01_introduction_demo.py) |
| 2 投资组合理论 | [Chapter02_投资组合理论.md](chapter_summaries_zh/Chapter02_投资组合理论.md) | [chapter02_portfolio_theory_demo.py](chapter_codes/chapter02_portfolio_theory_demo.py) |
| 3 风险模型与风险分析 | [Chapter03_风险模型与风险分析.md](chapter_summaries_zh/Chapter03_风险模型与风险分析.md) | [chapter03_risk_models_demo.py](chapter_codes/chapter03_risk_models_demo.py) |
| 4 Alpha 因子评估 | [Chapter04_Alpha因子评估.md](chapter_summaries_zh/Chapter04_Alpha因子评估.md) | [chapter04_alpha_evaluation_demo.py](chapter_codes/chapter04_alpha_evaluation_demo.py) |
| 5 量化因子 (Value/Quality/Momentum) | [Chapter05_量化因子.md](chapter_summaries_zh/Chapter05_量化因子.md) | [chapter05_quantitative_factors_demo.py](chapter_codes/chapter05_quantitative_factors_demo.py) |
| 6 估值技术与价值创造 (DCF) | [Chapter06_估值技术.md](chapter_summaries_zh/Chapter06_估值技术.md) | [chapter06_dcf_valuation_demo.py](chapter_codes/chapter06_dcf_valuation_demo.py) |
| 7 多因子 Alpha 模型 | [Chapter07_多因子Alpha模型.md](chapter_summaries_zh/Chapter07_多因子Alpha模型.md) | [chapter07_multifactor_alpha_demo.py](chapter_codes/chapter07_multifactor_alpha_demo.py) |
| 8 组合换手率与最优 Alpha 模型 | [Chapter08_组合换手率.md](chapter_summaries_zh/Chapter08_组合换手率.md) | [chapter08_turnover_demo.py](chapter_codes/chapter08_turnover_demo.py) |
| 9 高级 Alpha 建模技术 (Contextual/Nonlinear) | [Chapter09_高级Alpha建模.md](chapter_summaries_zh/Chapter09_高级Alpha建模.md) | [chapter09_advanced_alpha_demo.py](chapter_codes/chapter09_advanced_alpha_demo.py) |
| 10 因子择时模型 | [Chapter10_因子择时模型.md](chapter_summaries_zh/Chapter10_因子择时模型.md) | [chapter10_factor_timing_demo.py](chapter_codes/chapter10_factor_timing_demo.py) |
| 11 组合约束与信息比 | [Chapter11_组合约束.md](chapter_summaries_zh/Chapter11_组合约束.md) | [chapter11_constraints_demo.py](chapter_codes/chapter11_constraints_demo.py) |
| 12 交易成本与组合实施 | [Chapter12_交易成本与组合实施.md](chapter_summaries_zh/Chapter12_交易成本与组合实施.md) | [chapter12_transaction_cost_demo.py](chapter_codes/chapter12_transaction_cost_demo.py) |

## 运行方式

### 依赖
```bash
pip install numpy pandas scipy matplotlib statsmodels
```

### 运行示例
```bash
cd chapter_codes
python chapter01_introduction_demo.py
python chapter02_portfolio_theory_demo.py
# ...
```

每个脚本独立可执行，运行后会在当前目录生成 `chapterXX_demo.png` 图表。

## 内容覆盖

- **第一部分（理论）**: 第 1–3 章。Markowitz/CAPM 与多因子风险模型。
- **第二部分（Alpha 因子）**: 第 4–7 章。IC/IR 框架、价值/质量/动量、DCF 估值、多因子组合。
- **第三部分（实施）**: 第 8–12 章。换手率、情境建模、因子择时、组合约束、交易成本。
