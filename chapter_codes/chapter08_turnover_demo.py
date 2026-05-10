"""
Chapter 8 — Portfolio Turnover and Optimal Alpha Model
======================================================
演示 turnover 与 forecast autocorrelation 的关系，移动平均如何降低换手。
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

T, N = 200, 500


# ----------------------------------------------------------------------
# 1) 生成两期标准化预测，控制自相关 ρ_f
# ----------------------------------------------------------------------
def make_correlated_forecasts(T, N, rho_f):
    F = np.zeros((T, N))
    F[0] = np.random.normal(size=N)
    F[0] = (F[0] - F[0].mean()) / F[0].std()
    for t in range(1, T):
        eps = np.random.normal(size=N)
        F[t] = rho_f * F[t - 1] + np.sqrt(1 - rho_f ** 2) * eps
        F[t] = (F[t] - F[t].mean()) / F[t].std()
    return F


# ----------------------------------------------------------------------
# 2) 把预测转化为权重，计算单期换手率
# ----------------------------------------------------------------------
def compute_turnover(F, sigma_model=0.05, spec_risk=0.30):
    sigma_i = np.full(F.shape[1], spec_risk)
    lam = 1 / (sigma_model / np.sqrt(F.shape[1] - 1))
    weights = (F / sigma_i) / lam
    turnover = 0.5 * np.abs(np.diff(weights, axis=0)).sum(axis=1)
    return turnover.mean()


# ----------------------------------------------------------------------
# 3) 对比不同 ρ_f 的换手率
# ----------------------------------------------------------------------
results = []
for rho in [0.0, 0.3, 0.6, 0.8, 0.9, 0.95, 0.99]:
    F = make_correlated_forecasts(T, N, rho)
    T_emp = compute_turnover(F)
    sigma_model = 0.05
    T_theory = np.sqrt(N / np.pi) * sigma_model * np.sqrt(1 - rho) / 0.30
    results.append({"rho_f": rho, "T_empirical": T_emp, "T_theory": T_theory})

df = pd.DataFrame(results)
print("[Turnover vs Forecast Autocorrelation]")
print(df.round(4))


# ----------------------------------------------------------------------
# 4) 移动平均的影响
# ----------------------------------------------------------------------
def moving_average(F, L):
    out = np.zeros_like(F)
    for t in range(F.shape[0]):
        s = max(0, t - L + 1)
        out[t] = F[s:t + 1].mean(axis=0)
    return out


F = make_correlated_forecasts(T, N, rho_f=0.8)

ma_results = []
for L in [1, 2, 3, 4, 6, 8, 12]:
    F_ma = moving_average(F, L)
    autocorr = pd.DataFrame(F_ma).corrwith(pd.DataFrame(F_ma).shift(1)).mean()
    T_emp = compute_turnover(F_ma)
    ma_results.append({"L": L, "rho_ma": autocorr, "Turnover": T_emp})

df_ma = pd.DataFrame(ma_results)
print("\n[Moving Average: L vs Autocorrelation/Turnover]")
print(df_ma.round(4))


# ----------------------------------------------------------------------
# 5) 滞后 IC 与视野 IC 的关系
# ----------------------------------------------------------------------
def lagged_horizon_ic(F, R, max_lag=8):
    T = F.shape[0]
    lagged = []
    horizon = []
    for l in range(max_lag):
        ic_l = np.array([np.corrcoef(F[t], R[t + l])[0, 1]
                         for t in range(T - max_lag)]).mean()
        lagged.append(ic_l)
        cum = R.cumsum(axis=0)
        ic_h_arr = []
        for t in range(T - max_lag - l - 1):
            window_ret = cum[t + l + 1] - cum[t]
            ic_h_arr.append(np.corrcoef(F[t], window_ret)[0, 1])
        horizon.append(np.mean(ic_h_arr) if ic_h_arr else np.nan)
    return np.array(lagged), np.array(horizon)


R = 0.05 * F + np.random.normal(0, 1, F.shape)
for t in range(T):
    R[t] = (R[t] - R[t].mean()) / R[t].std()

lag_ic, horizon_ic = lagged_horizon_ic(F, R, max_lag=6)
print("\n[Lagged IC vs Horizon IC]")
for i in range(len(lag_ic)):
    print(f"  Lag={i}: lagged IC={lag_ic[i]:.4f}, horizon IC={horizon_ic[i]:.4f}")


if __name__ == "__main__":
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(df["rho_f"], df["T_empirical"], marker="o", label="实证")
    axes[0].plot(df["rho_f"], df["T_theory"], marker="x",
                 linestyle="--", label="理论 √(1-ρ)")
    axes[0].set_xlabel("预测自相关 ρ_f")
    axes[0].set_ylabel("单期换手率")
    axes[0].set_title("换手率 vs 预测自相关")
    axes[0].legend()
    axes[0].grid(True)

    axes[1].plot(df_ma["L"], df_ma["Turnover"], marker="o")
    axes[1].set_xlabel("移动平均阶 L")
    axes[1].set_ylabel("单期换手率")
    axes[1].set_title("移动平均降低换手率")
    axes[1].grid(True)
    plt.tight_layout()
    plt.savefig("chapter08_demo.png", dpi=120)
    print("\n[OK] 图表已保存: chapter08_demo.png")
