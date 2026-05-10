"""
Chapter 1 — Introduction: Beliefs, Risk, and Process
====================================================
本章演示量化投资的三大支柱：信念、风险、流程。
通过模拟数据展示行为金融偏差（过度反应/反应不足）以及量化因子的雏形。
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)


# ----------------------------------------------------------------------
# Demo 1: 信念——市场可预测性 vs 不可预测性
# 模拟两种世界：(a) 完全有效市场；(b) 存在动量异象的市场
# ----------------------------------------------------------------------
def simulate_market(n_periods=240, n_stocks=50, momentum=False):
    returns = np.random.normal(0.005, 0.06, size=(n_periods, n_stocks))
    if momentum:
        for t in range(1, n_periods):
            past_avg = returns[max(0, t - 6):t].mean(axis=0)
            returns[t] += 0.1 * past_avg
    return pd.DataFrame(returns)


eff = simulate_market(momentum=False)
mom = simulate_market(momentum=True)


def momentum_factor_test(returns):
    past = returns.rolling(6).sum().shift(1)
    fwd = returns
    ic = past.corrwith(fwd, axis=1).mean()
    return ic


print(f"[Beliefs] 有效市场动量 IC = {momentum_factor_test(eff):.4f}")
print(f"[Beliefs] 动量异象市场动量 IC = {momentum_factor_test(mom):.4f}")


# ----------------------------------------------------------------------
# Demo 2: 风险——三种常用度量
# ----------------------------------------------------------------------
def basic_risk_metrics(returns: pd.Series):
    vol = returns.std() * np.sqrt(252)
    var_95 = np.percentile(returns, 5)
    cvar_95 = returns[returns <= var_95].mean()
    return {"年化波动率": vol, "VaR(95%)": var_95, "CVaR(95%)": cvar_95}


port_returns = mom.mean(axis=1)
print("\n[Risk] 等权组合风险度量:")
for k, v in basic_risk_metrics(port_returns).items():
    print(f"  {k}: {v:.4f}")


# ----------------------------------------------------------------------
# Demo 3: 流程——从因子构建到组合
# ----------------------------------------------------------------------
def quant_process(returns: pd.DataFrame, lookback=6):
    factor = returns.rolling(lookback).sum().shift(1)
    z = factor.sub(factor.mean(axis=1), axis=0).div(factor.std(axis=1), axis=0)
    z = z.clip(-3, 3)
    weights = z.div(z.abs().sum(axis=1), axis=0).fillna(0)
    port_ret = (weights.shift(1) * returns).sum(axis=1)
    return port_ret, weights


pnl, w = quant_process(mom)
sharpe = pnl.mean() / pnl.std() * np.sqrt(252)
print(f"\n[Process] 多空动量组合年化夏普比率 = {sharpe:.3f}")
print(f"[Process] 累计收益 = {pnl.sum():.3f}")


# ----------------------------------------------------------------------
# Demo 4: 行为金融示例——过度反应（mean-reversion）
# ----------------------------------------------------------------------
def overreaction_test(returns, k=12):
    past = returns.rolling(k).sum().shift(1)
    fwd = returns.rolling(k).sum().shift(-k)
    ic_long = past.corrwith(fwd, axis=1).dropna().mean()
    return ic_long


ic_long = overreaction_test(mom)
print(f"\n[Behavioral] 长期反向 IC（12 月窗口）= {ic_long:.4f}")


if __name__ == "__main__":
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    pnl.cumsum().plot(ax=axes[0], title="动量策略累计收益")
    axes[0].set_xlabel("时间")
    axes[0].set_ylabel("累计收益")

    port_returns.hist(ax=axes[1], bins=40, alpha=0.7)
    axes[1].set_title("等权组合收益分布")
    axes[1].axvline(np.percentile(port_returns, 5), color="r",
                    linestyle="--", label="VaR(95%)")
    axes[1].legend()
    plt.tight_layout()
    plt.savefig("chapter01_demo.png", dpi=120)
    print("\n[OK] 图表已保存: chapter01_demo.png")
