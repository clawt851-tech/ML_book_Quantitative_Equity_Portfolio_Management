"""
Chapter 2 — Portfolio Theory
============================
演示 Markowitz 均值-方差最优化、CAPM、Beta-中性组合。
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)


# ----------------------------------------------------------------------
# 1) 输入：3 只股票的预期收益、波动率、相关矩阵
# ----------------------------------------------------------------------
f = np.array([0.10, 0.00, -0.10])
sigma = np.array([0.30, 0.30, 0.30])
C = np.array([[1.0, 0.5, 0.5],
              [0.5, 1.0, 0.5],
              [0.5, 0.5, 1.0]])
Sigma = np.diag(sigma) @ C @ np.diag(sigma)
i = np.ones(len(f))


# ----------------------------------------------------------------------
# 2) 最小方差组合 w = Σ⁻¹i / (i'Σ⁻¹i)
# ----------------------------------------------------------------------
def min_variance(Sigma):
    invS = np.linalg.inv(Sigma)
    return invS @ i / (i @ invS @ i)


w_min = min_variance(Sigma)
print("最小方差组合权重:", np.round(w_min, 4))
print("最小方差组合波动率:", np.sqrt(w_min @ Sigma @ w_min))


# ----------------------------------------------------------------------
# 3) 均值-方差最优组合（全额投资）
# ----------------------------------------------------------------------
def mv_full_invest(f, Sigma, lam):
    invS = np.linalg.inv(Sigma)
    A = i @ invS @ i
    B = i @ invS @ f
    w_min = invS @ i / A
    tilt = (1 / lam) * (invS @ f - (B / A) * invS @ i)
    return w_min + tilt


for lam in [1, 5, 25]:
    w = mv_full_invest(f, Sigma, lam)
    mu = w @ f
    sd = np.sqrt(w @ Sigma @ w)
    print(f"λ={lam}: w={np.round(w,3)}, μ={mu:.3%}, σ={sd:.3%}, IR={mu/sd:.3f}")


# ----------------------------------------------------------------------
# 4) 有效前沿
# ----------------------------------------------------------------------
def efficient_frontier(f, Sigma, n=100):
    lams = np.logspace(-1, 3, n)
    mus, sds = [], []
    for lam in lams:
        w = mv_full_invest(f, Sigma, lam)
        mus.append(w @ f)
        sds.append(np.sqrt(w @ Sigma @ w))
    return np.array(sds), np.array(mus)


sds, mus = efficient_frontier(f, Sigma)


# ----------------------------------------------------------------------
# 5) Active 主动组合（dollar neutral）
# ----------------------------------------------------------------------
def active_mv(f, Sigma, lam):
    invS = np.linalg.inv(Sigma)
    A = i @ invS @ i
    B = i @ invS @ f
    return (1 / lam) * (invS @ f - (B / A) * invS @ i)


a = active_mv(f, Sigma, 5)
print("\n主动权重 (dollar neutral):", np.round(a, 4), "和=", a.sum())


# ----------------------------------------------------------------------
# 6) CAPM 下的最优组合（β-neutral）
# ----------------------------------------------------------------------
beta = np.array([1.5, 1.0, 0.5])
spec_risk = np.array([0.30, 0.30, 0.30])
S = np.diag(spec_risk ** 2)


def beta_neutral(f, S, beta, lam):
    invS = np.linalg.inv(S)
    l = (f @ invS @ beta) / (beta @ invS @ beta)
    return (1 / lam) * invS @ (f - l * beta)


w_bn = beta_neutral(f, S, beta, 1)
print("\nβ-中性组合权重:", np.round(w_bn, 4))
print(f"组合 beta = {w_bn @ beta:.6f} (应为 0)")


# ----------------------------------------------------------------------
# 绘图
# ----------------------------------------------------------------------
if __name__ == "__main__":
    plt.figure(figsize=(8, 5))
    plt.plot(sds, mus, label="有效前沿(全额投资)")
    plt.scatter(np.sqrt(w_min @ Sigma @ w_min), w_min @ f,
                color="red", s=80, label="最小方差")
    plt.xlabel("波动率 σ")
    plt.ylabel("期望收益 μ")
    plt.title("均值-方差有效前沿")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("chapter02_demo.png", dpi=120)
    print("\n[OK] 图表已保存: chapter02_demo.png")
