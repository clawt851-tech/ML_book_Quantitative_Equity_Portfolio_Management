"""
Chapter 3 — Risk Models and Risk Analysis
=========================================
演示多因子风险模型、MCR、CR、PCR、VaR 贡献。
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

N, K, T = 50, 4, 600


# ----------------------------------------------------------------------
# 1) 合成多因子模型: r_i = b_i'f + ε_i
# ----------------------------------------------------------------------
B = np.random.normal(0, 1, size=(N, K))
factor_vol = np.array([0.04, 0.03, 0.02, 0.02])
F_corr = np.eye(K)
F_corr[0, 1] = F_corr[1, 0] = 0.2
Sigma_f = np.diag(factor_vol) @ F_corr @ np.diag(factor_vol)
spec_vol = np.random.uniform(0.10, 0.30, size=N)
S = np.diag(spec_vol ** 2)
Sigma = B @ Sigma_f @ B.T + S


# ----------------------------------------------------------------------
# 2) 计算 MCR、CR、PCR
# ----------------------------------------------------------------------
def risk_decomposition(w, Sigma):
    sd = np.sqrt(w @ Sigma @ w)
    mcr = Sigma @ w / sd
    cr = w * mcr
    pcr = cr / sd
    return sd, mcr, cr, pcr


w = np.ones(N) / N
sd, mcr, cr, pcr = risk_decomposition(w, Sigma)
print(f"组合波动率: {sd:.4f}")
print(f"PCR 之和（应 = 1）: {pcr.sum():.6f}")
print(f"\n前 5 只股票的 MCR / CR / PCR:")
df = pd.DataFrame({"MCR": mcr[:5], "CR": cr[:5], "PCR": pcr[:5]})
print(df)


# ----------------------------------------------------------------------
# 3) 系统/特异 MCR
# ----------------------------------------------------------------------
sys_var = (w @ B) @ Sigma_f @ (B.T @ w)
spec_var = w @ S @ w
sys_sd = np.sqrt(sys_var)
spec_sd = np.sqrt(spec_var)
print(f"\n系统波动率: {sys_sd:.4f}")
print(f"特异波动率: {spec_sd:.4f}")
print(f"总波动率验证: {np.sqrt(sys_var + spec_var):.4f} == {sd:.4f}")

mcr_sys = (B @ Sigma_f @ B.T @ w) / sys_sd
mcr_spec = (S @ w) / spec_sd


# ----------------------------------------------------------------------
# 4) 蒙特卡罗 VaR + 边际 VaR
# ----------------------------------------------------------------------
def simulate_returns(Sigma, T=20000, mu=None):
    if mu is None:
        mu = np.zeros(Sigma.shape[0])
    L = np.linalg.cholesky(Sigma + 1e-8 * np.eye(Sigma.shape[0]))
    Z = np.random.normal(size=(T, Sigma.shape[0]))
    return mu + Z @ L.T


R = simulate_returns(Sigma)
port_R = R @ w
VaR95 = -np.percentile(port_R, 5)
print(f"\n蒙特卡罗 VaR(95%) = {VaR95:.4f}")

# 边际 VaR: E[r_i | r_p ≈ -VaR]
tail_idx = port_R <= -VaR95
mcv = R[tail_idx].mean(axis=0)
cvar_contrib = w * mcv
print(f"VaR 验证（应 ≈ -VaR）: {cvar_contrib.sum():.4f}")


# ----------------------------------------------------------------------
# 5) 风险贡献按行业分组
# ----------------------------------------------------------------------
sectors = np.random.choice(["Tech", "Fin", "Health", "Energy"], size=N)
sector_pcr = pd.Series(pcr).groupby(sectors).sum()
print("\n按行业风险贡献占比:")
print(sector_pcr.round(4))


if __name__ == "__main__":
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].bar(range(N), pcr, color="steelblue")
    axes[0].set_title("各股票风险贡献占比 (PCR)")
    axes[0].set_xlabel("股票编号")
    axes[0].set_ylabel("PCR")

    axes[1].hist(port_R, bins=60, color="lightcoral", alpha=0.7)
    axes[1].axvline(-VaR95, color="red", linestyle="--", label=f"VaR(95%)={VaR95:.3f}")
    axes[1].set_title("组合收益分布与 VaR")
    axes[1].legend()
    plt.tight_layout()
    plt.savefig("chapter03_demo.png", dpi=120)
    print("\n[OK] 图表已保存: chapter03_demo.png")
