"""
Chapter 12 — Transaction Costs and Portfolio Implementation
============================================================
演示带交易成本的最优权重、最优交易路径 (calculus of variation)。
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

np.random.seed(42)


# ----------------------------------------------------------------------
# 1) 单资产带平方成本
# ----------------------------------------------------------------------
def optimal_w_quadratic(f, sigma, lam, w0, psi):
    return (f + 2 * psi * w0) / (lam * sigma ** 2 + 2 * psi)


f, sigma, lam, w0 = 0.15, 0.15, 10, 0.50
print("[平方成本]")
for psi in [0, 1, 5, 20]:
    w = optimal_w_quadratic(f, sigma, lam, w0, psi)
    print(f"  ψ={psi}: w*={w:.4f}")


# ----------------------------------------------------------------------
# 2) 单资产带线性成本
# ----------------------------------------------------------------------
def optimal_w_linear(f, sigma, lam, w0, theta):
    if (f + theta) / (lam * sigma ** 2) < w0:
        return (f + theta) / (lam * sigma ** 2)
    elif (f - theta) / (lam * sigma ** 2) > w0:
        return (f - theta) / (lam * sigma ** 2)
    return w0


print("\n[线性成本]")
for theta in [0, 0.005, 0.01, 0.02, 0.04]:
    w = optimal_w_linear(f, sigma, lam, w0, theta)
    print(f"  θ={theta}: w*={w:.4f}")


# ----------------------------------------------------------------------
# 3) 多资产 QP 形式（线性成本）
# ----------------------------------------------------------------------
def multi_asset_with_linear_cost(f, Sigma, w0, theta, lam=1.0):
    N = len(f)

    def utility(W):
        wB = W[:N]
        wS = W[N:]
        w = w0 + wB - wS
        return -(f @ w - 0.5 * lam * w @ Sigma @ w - theta * (wB.sum() + wS.sum()))

    bounds = [(0, 1)] * (2 * N)
    W0 = np.zeros(2 * N)
    res = minimize(utility, W0, method="SLSQP", bounds=bounds,
                   options={"maxiter": 200})
    wB = res.x[:N]
    wS = res.x[N:]
    return w0 + wB - wS, wB, wS


N = 20
f = np.random.normal(0, 0.05, N)
Sigma = np.diag(np.random.uniform(0.04, 0.25, N))
w0 = np.random.uniform(-0.05, 0.10, N)
w0 = w0 - w0.mean()

w_opt, wB, wS = multi_asset_with_linear_cost(f, Sigma, w0, theta=0.005)
print(f"\n多资产 QP: turnover = {(wB+wS).sum():.4f}")
print(f"组合 alpha = {f @ w_opt:.4f}")
print(f"成本 = {0.005 * (wB.sum() + wS.sum()):.4f}")


# ----------------------------------------------------------------------
# 4) 最优交易路径 h(t) — case s=g=0 (匀速)
# ----------------------------------------------------------------------
def optimal_path_g0_s0(T_total, n_steps=50):
    return np.linspace(0, 1, n_steps)


def optimal_path_g0(T_total, s, n_steps=50):
    t = np.linspace(0, T_total, n_steps)
    h = t / T_total + (s / 2) * t * (T_total - t)
    return np.clip(h, 0, 1)


def optimal_path_general(g, s, T_total, n_steps=100):
    t = np.linspace(0, T_total, n_steps)
    if abs(g) < 1e-8:
        return optimal_path_g0(T_total, s, n_steps)
    if g * T_total > 50:
        h = 1 - np.exp(-g * t)
        h_T = h[-1]
        if h_T < 1:
            h = h / h_T
        return np.clip(h, 0, 1)
    coef_a = (1 + s / g ** 2) * np.cosh(g * T_total) - s / g ** 2
    coef_a /= np.sinh(g * T_total)
    h = coef_a * np.sinh(g * t) - (1 + s / g ** 2) * (np.cosh(g * t) - 1)
    return np.clip(h, 0, 1)


T_total = 1.0
t = np.linspace(0, T_total, 100)
h_uniform = optimal_path_general(0, 0, T_total)
h_pos_s = optimal_path_general(0, 1.5, T_total)
h_neg_s = optimal_path_general(0, -1.5, T_total)
h_high_g = optimal_path_general(8, 0, T_total)


# ----------------------------------------------------------------------
# 5) 风险/成本前沿
# ----------------------------------------------------------------------
def cost_risk_frontier(g_values, s=0, T_total=1.0):
    points = []
    for g in g_values:
        h_path = optimal_path_general(g, s, T_total, n_steps=200)
        h_dot = np.gradient(h_path, T_total / 200)
        cost = (h_dot ** 2).sum() * (T_total / 200)
        risk_var = ((h_path - 1) ** 2).sum() * (T_total / 200)
        points.append({"g": g, "cost": cost, "risk_var": risk_var})
    return pd.DataFrame(points)


frontier = cost_risk_frontier(np.linspace(0.5, 10, 20))
print("\n[Risk-Cost Frontier]")
print(frontier.head().round(4))


if __name__ == "__main__":
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(t, h_uniform, label="g=0, s=0 (匀速)")
    axes[0].plot(t, h_pos_s, label="s>0 (先快)")
    axes[0].plot(t, h_neg_s, label="s<0 (先慢)")
    axes[0].plot(t, h_high_g, label="g 大 (急速)")
    axes[0].set_xlabel("时间 t / T")
    axes[0].set_ylabel("累计执行 h(t)")
    axes[0].set_title("最优交易路径")
    axes[0].legend()
    axes[0].grid(True)

    axes[1].plot(frontier["risk_var"], frontier["cost"], marker="o")
    axes[1].set_xlabel("实施风险 (variance)")
    axes[1].set_ylabel("市场冲击成本")
    axes[1].set_title("风险-成本有效前沿")
    axes[1].grid(True)
    plt.tight_layout()
    plt.savefig("chapter12_demo.png", dpi=120)
    print("\n[OK] 图表已保存: chapter12_demo.png")
