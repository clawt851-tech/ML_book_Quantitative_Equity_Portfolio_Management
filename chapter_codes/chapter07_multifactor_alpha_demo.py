"""
Chapter 7 — Multifactor Alpha Models
====================================
演示多因子 alpha 模型的最优权重 v* = s·Σ_IC⁻¹·IC̄ 与 Gram-Schmidt 正交化。
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

T, N, M = 80, 500, 3


# ----------------------------------------------------------------------
# 1) 生成 3 个因子和股票收益
# ----------------------------------------------------------------------
true_ICs = [0.06, 0.04, 0.05]
factor_corr = np.array([[1.0, 0.30, -0.10],
                        [0.30, 1.0, -0.20],
                        [-0.10, -0.20, 1.0]])

L = np.linalg.cholesky(factor_corr)
F_arr = np.zeros((T, M, N))
for t in range(T):
    Z = np.random.normal(size=(M, N))
    F_arr[t] = L @ Z
    F_arr[t] = (F_arr[t] - F_arr[t].mean(axis=1, keepdims=True)) / F_arr[t].std(axis=1, keepdims=True)

R = np.zeros((T, N))
for t in range(T):
    eps = np.random.normal(0, 1, N)
    weighted = sum(true_ICs[i] * F_arr[t, i] for i in range(M))
    norm = np.sqrt(sum(true_ICs[i] ** 2 for i in range(M)))
    R[t] = weighted + np.sqrt(1 - norm ** 2) * eps


# ----------------------------------------------------------------------
# 2) 计算 IC、IC 协方差矩阵
# ----------------------------------------------------------------------
IC = np.zeros((T, M))
for t in range(T):
    for i in range(M):
        IC[t, i] = np.corrcoef(F_arr[t, i], R[t])[0, 1]

IC_mean = IC.mean(axis=0)
IC_cov = np.cov(IC.T)
IC_corr = np.corrcoef(IC.T)
print("平均 IC 向量:", IC_mean.round(4))
print(f"\nIC 协方差矩阵:\n{IC_cov.round(6)}")
print(f"\nIC 相关矩阵:\n{IC_corr.round(3)}")


# ----------------------------------------------------------------------
# 3) 计算最优权重 v* = s·Σ_IC⁻¹·IC̄
# ----------------------------------------------------------------------
def optimal_weights(IC_mean, IC_cov):
    raw = np.linalg.inv(IC_cov) @ IC_mean
    return raw / raw.sum()


w_opt = optimal_weights(IC_mean, IC_cov)
print(f"\n最优权重: {w_opt.round(3)}")

w_eq = np.ones(M) / M


def composite_IR(w, IC_mean, IC_cov):
    return (w @ IC_mean) / np.sqrt(w @ IC_cov @ w)


print(f"等权 IR: {composite_IR(w_eq, IC_mean, IC_cov):.3f}")
print(f"最优 IR: {composite_IR(w_opt, IC_mean, IC_cov):.3f}")


# ----------------------------------------------------------------------
# 4) Gram-Schmidt 正交化
# ----------------------------------------------------------------------
def gram_schmidt(F_arr):
    T, M, N = F_arr.shape
    F_orth = F_arr.copy()
    for t in range(T):
        for p in range(1, M):
            for q in range(p):
                rho = np.corrcoef(F_orth[t, p], F_orth[t, q])[0, 1]
                F_orth[t, p] = F_orth[t, p] - rho * F_orth[t, q]
            v = F_orth[t, p].std()
            if v > 1e-8:
                F_orth[t, p] = F_orth[t, p] / v
    return F_orth


F_orth = gram_schmidt(F_arr)


def factor_corr_sample(F_arr, t=0):
    M = F_arr.shape[1]
    return np.corrcoef([F_arr[t, i] for i in range(M)])


print(f"\n原始因子相关矩阵 (t=0):\n{factor_corr_sample(F_arr).round(3)}")
print(f"\n正交化后因子相关矩阵 (t=0):\n{factor_corr_sample(F_orth).round(3)}")


# ----------------------------------------------------------------------
# 5) 复合因子表现对比
# ----------------------------------------------------------------------
def composite_factor_score(F_arr, weights):
    T, M, N = F_arr.shape
    return np.array([sum(weights[i] * F_arr[t, i] for i in range(M)) for t in range(T)])


comp_eq = composite_factor_score(F_arr, w_eq)
comp_opt = composite_factor_score(F_arr, w_opt)


def factor_ic(comp, R):
    return np.array([np.corrcoef(comp[t], R[t])[0, 1] for t in range(comp.shape[0])])


ic_eq = factor_ic(comp_eq, R)
ic_opt = factor_ic(comp_opt, R)
print(f"\n等权复合因子: IC={ic_eq.mean():.4f}, IR={ic_eq.mean()/ic_eq.std():.3f}")
print(f"最优复合因子: IC={ic_opt.mean():.4f}, IR={ic_opt.mean()/ic_opt.std():.3f}")


# ----------------------------------------------------------------------
# 6) 两因子情形——IR 关于因子相关性的曲线
# ----------------------------------------------------------------------
def two_factor_IR(rho, IR1=1.0, IR2=0.5):
    return np.sqrt((IR1 ** 2 + IR2 ** 2 - 2 * rho * IR1 * IR2) / (1 - rho ** 2))


rhos = np.linspace(-0.5, 0.5, 21)
IRs = [two_factor_IR(r) for r in rhos]


if __name__ == "__main__":
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(rhos, IRs, marker="o")
    axes[0].set_xlabel("IC 相关性 ρ")
    axes[0].set_ylabel("最优复合 IR")
    axes[0].set_title("两因子模型: IR 关于 IC 相关性")
    axes[0].grid(True)

    axes[1].bar(["F1", "F2", "F3"], w_opt, color="orange", alpha=0.7, label="最优")
    axes[1].bar(["F1", "F2", "F3"], w_eq, color="steelblue", alpha=0.5, label="等权")
    axes[1].set_title("因子权重对比")
    axes[1].legend()
    plt.tight_layout()
    plt.savefig("chapter07_demo.png", dpi=120)
    print("\n[OK] 图表已保存: chapter07_demo.png")
