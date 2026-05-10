"""
Chapter 4 — Evaluation of Alpha Factors
=======================================
演示 IC, IR, FLAM, risk-adjusted IC, dispersion, breadth 与超额收益分解。
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

np.random.seed(42)

T, N = 80, 500


# ----------------------------------------------------------------------
# 1) 模拟因子和未来收益（含真实 IC）
# ----------------------------------------------------------------------
def simulate_factor_returns(T, N, true_ic=0.05, dispersion=1.0):
    F = np.random.normal(0, 1, size=(T, N))
    eps = np.random.normal(0, 1, size=(T, N))
    rho = true_ic
    R = (rho * F + np.sqrt(1 - rho ** 2) * eps) * dispersion
    return F, R


F, R = simulate_factor_returns(T, N, true_ic=0.05)


# ----------------------------------------------------------------------
# 2) 计算每期 IC，IR
# ----------------------------------------------------------------------
def compute_ic(F, R):
    return np.array([pearsonr(F[t], R[t])[0] for t in range(F.shape[0])])


ic = compute_ic(F, R)
print(f"平均 IC = {ic.mean():.4f}")
print(f"std(IC) = {ic.std():.4f}")
print(f"采样误差 1/√N = {1 / np.sqrt(N):.4f}")
print(f"实际 IR = {ic.mean() / ic.std():.3f}")
print(f"FLAM 预测 IR = IC·√N = {ic.mean() * np.sqrt(N):.3f}")


# ----------------------------------------------------------------------
# 3) 风险模型调整：把 F 和 R 减去 beta-市值-风格 因子
# ----------------------------------------------------------------------
beta = np.random.uniform(0.5, 1.5, size=N)
size = np.random.normal(0, 1, size=N)
risk_factors = np.column_stack([np.ones(N), beta, size])


def neutralize(x, X):
    coefs = np.linalg.lstsq(X, x, rcond=None)[0]
    return x - X @ coefs


F_adj = np.array([neutralize(F[t], risk_factors) for t in range(T)])
R_adj = np.array([neutralize(R[t], risk_factors) for t in range(T)])

ic_adj = compute_ic(F_adj, R_adj)
print(f"\n风险调整后:")
print(f"  平均 IC = {ic_adj.mean():.4f}")
print(f"  std(IC) = {ic_adj.std():.4f}")
print(f"  IR = {ic_adj.mean() / ic_adj.std():.3f}")


# ----------------------------------------------------------------------
# 4) 单期超额收益分解：α = IC·√N·σ_model·dis(R)
# ----------------------------------------------------------------------
sigma_model = 0.05
dis_R = R_adj.std(axis=1).mean()
mean_alpha = ic_adj.mean() * np.sqrt(N) * sigma_model * dis_R
print(f"\nα 分解:")
print(f"  IC = {ic_adj.mean():.4f}")
print(f"  √N = {np.sqrt(N):.2f}")
print(f"  σ_model = {sigma_model}")
print(f"  dis(R) = {dis_R:.4f}")
print(f"  预测平均 α = {mean_alpha:.4%}")


# ----------------------------------------------------------------------
# 5) 跟踪误差 σ = std(IC)·√N·σ_model·dis(R)
# ----------------------------------------------------------------------
te = ic_adj.std() * np.sqrt(N) * sigma_model * dis_R
print(f"\n跟踪误差 σ = {te:.4%}")
kappa = ic_adj.std() * np.sqrt(N)
print(f"κ = std(IC)·√N = {kappa:.3f}")
print(f"调整后 σ_model* = σ_model / κ = {sigma_model / kappa:.4%}")


# ----------------------------------------------------------------------
# 6) 多个因子的 IR 对比
# ----------------------------------------------------------------------
factors_perf = []
for true_ic, label in [(0.10, "Strong"), (0.05, "Medium"), (0.02, "Weak")]:
    F_, R_ = simulate_factor_returns(T, N, true_ic)
    ic_ = compute_ic(F_, R_)
    factors_perf.append({"factor": label, "avg_IC": ic_.mean(),
                         "std_IC": ic_.std(),
                         "IR": ic_.mean() / ic_.std()})
print("\n因子性能对比:")
print(pd.DataFrame(factors_perf).round(4))


if __name__ == "__main__":
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(ic, label="Raw IC", alpha=0.6)
    axes[0].plot(ic_adj, label="Risk-Adjusted IC", alpha=0.6)
    axes[0].axhline(0, color="k", linewidth=0.5)
    axes[0].set_title("信息系数时间序列")
    axes[0].legend()
    axes[0].set_xlabel("期")

    axes[1].hist(ic_adj, bins=20, alpha=0.7, color="steelblue")
    axes[1].axvline(ic_adj.mean(), color="red", linestyle="--", label="均值")
    axes[1].set_title("风险调整 IC 分布")
    axes[1].legend()
    plt.tight_layout()
    plt.savefig("chapter04_demo.png", dpi=120)
    print("\n[OK] 图表已保存: chapter04_demo.png")
