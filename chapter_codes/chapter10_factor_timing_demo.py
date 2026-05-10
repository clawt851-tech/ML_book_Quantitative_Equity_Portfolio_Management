"""
Chapter 10 — Factor Timing Models
=================================
演示日历效应、盈利公告效应、宏观条件择时。
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(42)

T_months, N = 200, 500


# ----------------------------------------------------------------------
# 1) 模拟 IC 时间序列，含日历效应
# ----------------------------------------------------------------------
def simulate_calendar_ic(months=200):
    np.random.seed(42)
    months_idx = np.arange(months) % 12
    ic = np.zeros(months)
    for i in range(months):
        m = months_idx[i]
        if m < 5:
            mu = -0.04
        elif m >= 7:
            mu = 0.05
        else:
            mu = 0.01
        ic[i] = mu + np.random.normal(0, 0.05)
    return pd.Series(ic, index=pd.date_range(
        "2000-01-01", periods=months, freq="MS"))


ic_series = simulate_calendar_ic(T_months)


# ----------------------------------------------------------------------
# 2) 假设 I 检验：t-test 和 Wilcoxon
# ----------------------------------------------------------------------
first_half = ic_series[ic_series.index.month <= 5]
second_half = ic_series[ic_series.index.month >= 7]

t_stat, p_val = stats.ttest_ind(first_half, second_half, equal_var=False)
w_stat, w_p = stats.mannwhitneyu(first_half, second_half, alternative="two-sided")
f_stat = first_half.var() / second_half.var()

print(f"前 5 个月平均 IC: {first_half.mean():.4f}")
print(f"后 5 个月平均 IC: {second_half.mean():.4f}")
print(f"\nt-test: t={t_stat:.3f}, p={p_val:.4f}")
print(f"Mann-Whitney U: U={w_stat:.0f}, p={w_p:.4f}")
print(f"F-test (var比): {f_stat:.3f}")


# ----------------------------------------------------------------------
# 3) 横截面回报离散度的盈利公告效应
# ----------------------------------------------------------------------
def simulate_dispersion(months=200):
    is_jan = (np.arange(months) % 12) == 0
    is_dec = (np.arange(months) % 12) == 11
    is_announcement = np.isin(np.arange(months) % 12, [0, 3, 6, 9])
    is_warning = np.isin(np.arange(months) % 12, [2, 5, 8, 11])

    base = 1.0
    dispersion = (base
                  + 0.029 * is_jan
                  + 0.018 * is_dec
                  + 0.060 * is_warning
                  + 0.088 * is_announcement
                  + np.random.normal(0, 0.119, months))
    return pd.DataFrame({
        "dispersion": dispersion,
        "isJan": is_jan.astype(int),
        "isDec": is_dec.astype(int),
        "isWarning": is_warning.astype(int),
        "isAnnouncement": is_announcement.astype(int),
    })


df_disp = simulate_dispersion(T_months)


# ----------------------------------------------------------------------
# 4) 回归测试盈利公告效应
# ----------------------------------------------------------------------
import statsmodels.api as sm

X = df_disp[["isJan", "isDec", "isWarning", "isAnnouncement"]]
X = sm.add_constant(X)
y = df_disp["dispersion"]
model = sm.OLS(y, X).fit()
print("\n[Dispersion 回归结果]")
print(model.summary().tables[1])


# ----------------------------------------------------------------------
# 5) 宏观条件择时——货币政策扩张/紧缩
# ----------------------------------------------------------------------
def simulate_monetary_regime(months=200):
    regime = np.random.choice([0, 1], size=months, p=[0.5, 0.5])
    quality_ic = np.where(regime == 1,
                          np.random.normal(0.05, 0.03, months),
                          np.random.normal(-0.01, 0.04, months))
    return regime, quality_ic


regime, q_ic = simulate_monetary_regime(T_months)
print(f"\n紧缩期质量因子 IC: {q_ic[regime==1].mean():.4f}")
print(f"扩张期质量因子 IC: {q_ic[regime==0].mean():.4f}")
t2, p2 = stats.ttest_ind(q_ic[regime == 1], q_ic[regime == 0], equal_var=False)
print(f"t={t2:.3f}, p={p2:.4f}")


# ----------------------------------------------------------------------
# 6) 组合调仓策略：高 dispersion 月之前增加 alpha
# ----------------------------------------------------------------------
def alpha_with_dispersion_timing(ic_series, dispersion):
    sized_ic = ic_series.values[:len(dispersion)] * dispersion.values
    return sized_ic.cumsum()


timed_alpha = alpha_with_dispersion_timing(ic_series, df_disp["dispersion"])


if __name__ == "__main__":
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    monthly_avg = ic_series.groupby(ic_series.index.month).mean()
    axes[0, 0].bar(range(1, 13), monthly_avg.values, color="steelblue")
    axes[0, 0].axhline(0, color="k", linewidth=0.5)
    axes[0, 0].set_title("月份平均 IC（日历效应）")
    axes[0, 0].set_xlabel("月份")

    df_disp.boxplot(column="dispersion",
                    by=df_disp["isAnnouncement"].map({0: "Quiet", 1: "Announce"}),
                    ax=axes[0, 1])
    axes[0, 1].set_title("公告月 vs 静默月: 横截面 dispersion")

    axes[1, 0].plot(timed_alpha)
    axes[1, 0].set_title("dispersion-timed 累计 alpha")

    axes[1, 1].hist(q_ic[regime == 1], bins=20, alpha=0.5, label="紧缩")
    axes[1, 1].hist(q_ic[regime == 0], bins=20, alpha=0.5, label="扩张")
    axes[1, 1].set_title("货币政策 vs 质量因子 IC")
    axes[1, 1].legend()

    plt.tight_layout()
    plt.savefig("chapter10_demo.png", dpi=120)
    print("\n[OK] 图表已保存: chapter10_demo.png")
