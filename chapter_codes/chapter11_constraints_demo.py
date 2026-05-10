"""
Chapter 11 — Portfolio Constraints and Information Ratio
=========================================================
演示对数正态基准模拟、long-only 约束、IR 衰减、Transfer Coefficient。
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import minimize

np.random.seed(42)


# ----------------------------------------------------------------------
# 1) 模拟基准权重（对数正态）
# ----------------------------------------------------------------------
def simulate_benchmark_weights(N=500, c=1.0):
    p = 1 - (np.arange(1, N + 1) - 0.5) / N
    y = stats.norm.ppf(p)
    s = np.exp(c * y)
    return s / s.sum()


b_eq = simulate_benchmark_weights(500, c=0.0)
b_concentrated = simulate_benchmark_weights(500, c=1.2)
print(f"等权基准前 5 名占比: {b_eq[:5].sum():.4f}")
print(f"集中基准前 5 名占比: {b_concentrated[:5].sum():.4f}")
print(f"集中基准前 50 名占比: {b_concentrated[:50].sum():.4f}")


# ----------------------------------------------------------------------
# 2) 单股票多空仓位概率
# ----------------------------------------------------------------------
def short_probability(b_i, sigma_i, sigma_target, N):
    s_i = sigma_target / (np.sqrt(N) * sigma_i)
    return stats.norm.cdf(0, loc=b_i, scale=s_i)


print(f"\n单股票多空仓位概率:")
print(f"  b=0.3%, σ=30%, TE=3%: {short_probability(0.003, 0.30, 0.03, 500):.4f}")
print(f"  b=1.0%, σ=30%, TE=3%: {short_probability(0.010, 0.30, 0.03, 500):.4f}")


# ----------------------------------------------------------------------
# 3) 平均 long/short 比例
# ----------------------------------------------------------------------
def avg_long_short(b, sigma, sigma_target, N):
    s = sigma_target / (np.sqrt(N) * sigma)
    L_total, S_total = 0, 0
    for b_i, s_i in zip(b, s):
        cdf_neg = stats.norm.cdf(-b_i / s_i)
        E_short = -s_i / np.sqrt(2 * np.pi) * np.exp(-(b_i ** 2) / (2 * s_i ** 2)) + b_i * cdf_neg
        E_long = b_i + s_i / np.sqrt(2 * np.pi) * np.exp(-(b_i ** 2) / (2 * s_i ** 2)) - b_i * cdf_neg
        L_total += E_long
        S_total += E_short
    return L_total, S_total


sigma_arr = np.full(500, 0.30)
for TE in [0.01, 0.025, 0.05]:
    L, S = avg_long_short(b_concentrated, sigma_arr, TE, 500)
    print(f"\nTE={TE*100}%: long={L*100:.1f}%, short={S*100:.1f}%, leverage={(L-S)*100:.1f}%")


# ----------------------------------------------------------------------
# 4) Long-only 约束 + 范围约束的数值解
# ----------------------------------------------------------------------
def long_only_optimize(f, Sigma, b, sigma_target=0.03, max_w=0.02):
    N = len(f)

    def neg_alpha(w):
        return -f @ w

    def te_constraint(w):
        return sigma_target ** 2 - w @ Sigma @ w

    def dollar_neutral(w):
        return w.sum()

    constraints = [
        {"type": "eq", "fun": dollar_neutral},
        {"type": "ineq", "fun": te_constraint},
    ]

    # Long-only: w >= -b (active weight floor)
    bounds = [(-bi, max_w) for bi in b]
    w0 = np.zeros(N)
    res = minimize(neg_alpha, w0, method="SLSQP",
                   bounds=bounds, constraints=constraints,
                   options={"maxiter": 200})
    return res.x


N = 50
f = np.random.normal(0, 1, N)
spec_risk = np.full(N, 0.35)
Sigma = np.diag(spec_risk ** 2)
b = simulate_benchmark_weights(N, c=1.0)

w_unc = (f / spec_risk ** 2)
w_unc *= 0.03 / np.sqrt(w_unc @ Sigma @ w_unc)
w_lo = long_only_optimize(f, Sigma, b)

print(f"\n无约束最优权重范围: [{w_unc.min():.4f}, {w_unc.max():.4f}]")
print(f"Long-only 最优权重范围: [{w_lo.min():.4f}, {w_lo.max():.4f}]")


# ----------------------------------------------------------------------
# 5) Transfer Coefficient
# ----------------------------------------------------------------------
def transfer_coefficient(w, f):
    return np.corrcoef(w, f)[0, 1]


tc_unc = transfer_coefficient(w_unc, f)
tc_lo = transfer_coefficient(w_lo, f)
print(f"\nTransfer Coefficient:")
print(f"  无约束: {tc_unc:.4f}")
print(f"  Long-only: {tc_lo:.4f}")


# ----------------------------------------------------------------------
# 6) IR vs 长仓比例
# ----------------------------------------------------------------------
def simulate_ir_decay(long_ratios=[1.0, 1.10, 1.20, 1.30, 1.50, 2.0]):
    results = []
    for L in long_ratios:
        theoretical_ir = 0.10 * np.sqrt(500) * L / np.sqrt(L)
        net_ir = theoretical_ir * (1 - 0.02 * (L - 1) / 0.5)
        results.append({"Long": L, "Theoretical IR": theoretical_ir,
                        "Net IR": net_ir})
    return pd.DataFrame(results)


df_ir = simulate_ir_decay()
print("\n[IR 衰减]")
print(df_ir.round(3))


if __name__ == "__main__":
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    cumulated_eq = np.cumsum(np.sort(b_eq)[::-1])
    cumulated_conc = np.cumsum(np.sort(b_concentrated)[::-1])
    axes[0].plot(cumulated_eq, label="c=0 (等权)")
    axes[0].plot(cumulated_conc, label="c=1.2 (集中)")
    axes[0].set_xlabel("股票排名")
    axes[0].set_ylabel("累计权重")
    axes[0].set_title("基准累计权重 (对数正态模拟)")
    axes[0].legend()

    axes[1].plot(df_ir["Long"], df_ir["Theoretical IR"], marker="o", label="理论 IR")
    axes[1].plot(df_ir["Long"], df_ir["Net IR"], marker="s", label="净 IR")
    axes[1].set_xlabel("总长仓比例")
    axes[1].set_ylabel("IR")
    axes[1].set_title("Long/Short 比例 vs IR")
    axes[1].legend()
    axes[1].grid(True)
    plt.tight_layout()
    plt.savefig("chapter11_demo.png", dpi=120)
    print("\n[OK] 图表已保存: chapter11_demo.png")
