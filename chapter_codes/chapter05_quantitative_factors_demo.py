"""
Chapter 5 — Quantitative Factors
================================
演示价值、质量、动量三类因子的构造、IC 计算和小型 backtest。
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

T, N = 60, 300


# ----------------------------------------------------------------------
# 1) 模拟基本面/价格数据并构造因子
# ----------------------------------------------------------------------
sectors = np.random.choice(["Tech", "Fin", "Health", "Energy", "Cons"], size=N)
prices = 100 * np.exp(np.cumsum(np.random.normal(0.005, 0.06, size=(T, N)), axis=0))
returns = pd.DataFrame(np.diff(np.log(prices), axis=0))


def make_value_factors():
    book = np.random.uniform(10, 100, size=N) + np.random.normal(0, 5, size=(T - 1, N))
    sales = np.random.uniform(50, 500, size=N) + np.random.normal(0, 10, size=(T - 1, N))
    cfo = np.random.uniform(5, 50, size=N) + np.random.normal(0, 2, size=(T - 1, N))
    mv = prices[1:] * np.random.uniform(50, 200, size=N)
    return {
        "B2P": pd.DataFrame(book / mv),
        "S2P": pd.DataFrame(sales / mv),
        "CFO2P": pd.DataFrame(cfo / mv),
    }


value_factors = make_value_factors()


def make_quality_factors():
    rnoa = np.random.normal(0.10, 0.05, size=(T - 1, N))
    capx = np.random.uniform(0, 30, size=N) + np.random.normal(0, 1, size=(T - 1, N))
    sales = np.random.uniform(50, 500, size=N) + np.random.normal(0, 10, size=(T - 1, N))
    capx_growth = capx / sales
    return {
        "RNOA": pd.DataFrame(rnoa),
        "CapxGrowth": pd.DataFrame(-capx_growth),
    }


qual_factors = make_quality_factors()


def make_momentum_factors():
    R = returns.values
    ret9 = pd.DataFrame(R).rolling(9).sum().shift(1)
    ret9_x1 = pd.DataFrame(R).rolling(9).sum().shift(2)
    return {
        "Ret9": ret9,
        "Ret9MonEx1": ret9_x1,
    }


mom_factors = make_momentum_factors()


# ----------------------------------------------------------------------
# 2) 行业内排名（peer-group ranking）
# ----------------------------------------------------------------------
def peer_rank(factor_df, sectors):
    df = factor_df.copy()
    sec = pd.Series(sectors)
    out = pd.DataFrame(index=df.index, columns=df.columns, dtype=float)
    for t in df.index:
        row = df.loc[t]
        for s in sec.unique():
            mask = (sec == s).values
            ranks = pd.Series(row[mask]).rank(pct=True) - 0.5
            out.loc[t, mask] = ranks.values
    return out


B2P_rank = peer_rank(value_factors["B2P"], sectors)


# ----------------------------------------------------------------------
# 3) IC、IR、自相关
# ----------------------------------------------------------------------
def factor_ic(factor, fwd_returns):
    common_idx = factor.index.intersection(fwd_returns.index)
    factor = factor.loc[common_idx].dropna(how='all')
    rets = fwd_returns.loc[factor.index]
    return factor.corrwith(rets, axis=1)


def factor_summary(name, factor, fwd_returns):
    ic = factor_ic(factor, fwd_returns).dropna()
    autocorr = factor.shift(1).corrwith(factor, axis=1).dropna().mean()
    return {
        "Factor": name,
        "Avg IC": ic.mean(),
        "IC StDev": ic.std(),
        "IR (annualized)": ic.mean() / ic.std() * np.sqrt(4),
        "AutoCorr": autocorr,
    }


fwd = returns.shift(-1)
results = []
for name, f in {**value_factors, **qual_factors, **mom_factors}.items():
    results.append(factor_summary(name, f, fwd))
df_summary = pd.DataFrame(results)
print("\n[因子综合表现]")
print(df_summary.round(4))


# ----------------------------------------------------------------------
# 4) 分位组合回测（top decile - bottom decile）
# ----------------------------------------------------------------------
def decile_backtest(factor, returns, n_groups=10):
    excess = []
    for t in factor.index[:-1]:
        ranks = factor.loc[t].rank(pct=True)
        if ranks.isnull().all():
            continue
        top = (ranks > 0.9).values
        bot = (ranks < 0.1).values
        r_t1 = returns.loc[t + 1]
        excess.append(r_t1[top].mean() - r_t1[bot].mean())
    return pd.Series(excess)


for name in ["B2P", "RNOA", "Ret9"]:
    f = {**value_factors, **qual_factors, **mom_factors}[name]
    pnl = decile_backtest(f, returns)
    print(f"\n[Decile Backtest] {name}: 年化超额={pnl.mean()*4:.4f} | "
          f"年化波动={pnl.std()*2:.4f} | Sharpe={pnl.mean()/pnl.std()*2:.3f}")


if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(10, 5))
    df_summary.plot.bar(x="Factor", y=["Avg IC", "IR (annualized)"],
                        ax=ax, secondary_y=["IR (annualized)"])
    ax.set_title("各因子平均 IC 与 年化 IR")
    plt.tight_layout()
    plt.savefig("chapter05_demo.png", dpi=120)
    print("\n[OK] 图表已保存: chapter05_demo.png")
