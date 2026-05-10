"""
Chapter 9 — Advanced Alpha Modeling Techniques
==============================================
演示情境建模 (Contextual Modeling)、非线性效应、模型距离测试。
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

T, N = 60, 600


# ----------------------------------------------------------------------
# 1) 模拟两个 context（高/低 P/B）
# ----------------------------------------------------------------------
def simulate_context_data(T, N, ic_high=0.06, ic_low=0.015):
    pb = np.random.lognormal(0, 0.7, size=N)
    is_high = pb < np.median(pb)

    F = np.zeros((T, N))
    R = np.zeros((T, N))
    for t in range(T):
        F[t] = np.random.normal(size=N)
        F[t] = (F[t] - F[t].mean()) / F[t].std()
        eps = np.random.normal(size=N)
        ic = np.where(is_high, ic_high, ic_low)
        R[t] = ic * F[t] + np.sqrt(1 - ic ** 2) * eps
        R[t] = (R[t] - R[t].mean()) / R[t].std()
    return F, R, is_high


F, R, is_high = simulate_context_data(T, N)


def context_ic(F, R, mask):
    ic = []
    for t in range(F.shape[0]):
        f_sub = F[t, mask]
        r_sub = R[t, mask]
        if f_sub.std() > 0 and r_sub.std() > 0:
            ic.append(np.corrcoef(f_sub, r_sub)[0, 1])
    return np.array(ic)


ic_H = context_ic(F, R, is_high)
ic_L = context_ic(F, R, ~is_high)
print(f"高 context IC: 均值={ic_H.mean():.4f}, std={ic_H.std():.4f}")
print(f"低 context IC: 均值={ic_L.mean():.4f}, std={ic_L.std():.4f}")
print(f"IC 差异 t-stat: {(ic_H.mean()-ic_L.mean())/np.sqrt(ic_H.var()/T+ic_L.var()/T):.3f}")


# ----------------------------------------------------------------------
# 2) 整体 vs 情境化模型的 IR 对比
# ----------------------------------------------------------------------
ic_combined = np.array([np.corrcoef(F[t], R[t])[0, 1] for t in range(T)])

print(f"\n一刀切模型: IC={ic_combined.mean():.4f}, IR={ic_combined.mean()/ic_combined.std():.3f}")
print(f"情境化模型(高): IC={ic_H.mean():.4f}, IR={ic_H.mean()/ic_H.std():.3f}")
print(f"情境化模型(低): IC={ic_L.mean():.4f}, IR={ic_L.mean()/ic_L.std():.3f}")


# ----------------------------------------------------------------------
# 3) 最优情境权重
# ----------------------------------------------------------------------
def optimal_context_weights(ic_H, ic_L):
    sigma_H, sigma_L = ic_H.std(), ic_L.std()
    rho = np.corrcoef(ic_H, ic_L)[0, 1]
    v_H = ic_H.mean() / sigma_H ** 2 - rho * ic_L.mean() / (sigma_H * sigma_L)
    v_L = ic_L.mean() / sigma_L ** 2 - rho * ic_H.mean() / (sigma_H * sigma_L)
    s = v_H + v_L
    if abs(s) < 1e-12:
        s = 1
    return v_H / s, v_L / s


vH, vL = optimal_context_weights(ic_H, ic_L)
print(f"\n最优情境权重: 高={vH:.3f}, 低={vL:.3f}")


# ----------------------------------------------------------------------
# 4) Bootstrap 模型距离测试
# ----------------------------------------------------------------------
def model_distance(weights1, weights2):
    diff = np.array(weights1) - np.array(weights2)
    return np.sqrt(np.dot(diff, diff) / len(diff))


def bootstrap_distance(F, R, mask, n_bootstrap=200):
    distances = []
    T_n = F.shape[0]
    for _ in range(n_bootstrap):
        idx = np.random.choice(T_n, T_n, replace=True)
        F_b, R_b = F[idx], R[idx]
        ic_H_b = context_ic(F_b, R_b, mask)
        ic_L_b = context_ic(F_b, R_b, ~mask)
        if len(ic_H_b) > 5 and len(ic_L_b) > 5:
            wH, wL = optimal_context_weights(ic_H_b, ic_L_b)
            distances.append(model_distance([wH, wL], [0.5, 0.5]))
    return np.array(distances)


dists = bootstrap_distance(F, R, is_high)
print(f"\n模型距离均值: {dists.mean():.4f}, std: {dists.std():.4f}")


# ----------------------------------------------------------------------
# 5) 非线性效应：CAPEX 例
# ----------------------------------------------------------------------
def simulate_capex_returns(N=2000):
    capex = np.random.lognormal(0, 0.7, size=N)
    base_return = -0.5 * (capex - 1) ** 2 + 0.05
    noise = np.random.normal(0, 0.3, size=N)
    returns = base_return + noise
    return capex, returns


capex, ret = simulate_capex_returns()

bins = pd.qcut(capex, q=20, labels=False)
df_box = pd.DataFrame({"capex_rank": bins, "ret": ret})


def fit_polynomial(capex, ret, deg=2):
    X = np.column_stack([capex ** i for i in range(deg + 1)])
    coefs = np.linalg.lstsq(X, ret, rcond=None)[0]
    return coefs


coefs = fit_polynomial(capex, ret, deg=2)
print(f"\n二次多项式拟合系数: {coefs.round(4)}")


if __name__ == "__main__":
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    df_box.boxplot(column="ret", by="capex_rank", ax=axes[0])
    axes[0].set_title("CAPEX 分位 vs 收益（凹形非线性）")
    axes[0].set_xlabel("CAPEX 分位")

    axes[1].hist(dists, bins=30, color="steelblue", alpha=0.7)
    axes[1].set_title("模型距离 Bootstrap 分布")
    axes[1].set_xlabel("model distance d")
    plt.tight_layout()
    plt.savefig("chapter09_demo.png", dpi=120)
    print("\n[OK] 图表已保存: chapter09_demo.png")
