"""
Chapter 6 — Valuation Techniques and Value Creation
===================================================
演示 DCF 估值框架、RIC 分解、三阶段 DCF、灵敏度分析。
"""

import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------
# 1) 基础公式：Operating Value = S0(p̄ - g/s̄)(1+g)/(w-g)
# ----------------------------------------------------------------------
def operating_value(sales, profitability, scalability, growth, wacc):
    return sales * (profitability - growth / scalability) * (1 + growth) / (wacc - growth)


S0 = 1.0
p_bar = 0.10
s_bar = 2.0
g = 0.05
w = 0.09

OV = operating_value(S0, p_bar, s_bar, g, w)
print(f"基本估值 OV = ${OV:.2f}")
print(f"FCFF margin = {p_bar - g / s_bar:.4f} = {(p_bar - g/s_bar)*100:.2f}%")
print(f"RIC = profitability × scalability = {p_bar * s_bar:.4f}")
print(f"EVC = RIC - WACC = {p_bar*s_bar - w:.4f}")


# ----------------------------------------------------------------------
# 2) 灵敏度分析
# ----------------------------------------------------------------------
def sensitivity(S0, p, s, g, w, dx=0.01):
    base = operating_value(S0, p, s, g, w)
    return {
        "Profitability": (operating_value(S0, p + dx, s, g, w) - base) / base / dx,
        "Scalability":   (operating_value(S0, p, s + dx, g, w) - base) / base / dx,
        "Growth":        (operating_value(S0, p, s, g + dx, w) - base) / base / dx,
        "Sales":         (operating_value(S0 + dx, p, s, g, w) - base) / base / dx,
        "WACC":          (operating_value(S0, p, s, g, w + dx) - base) / base / dx,
    }


sens = sensitivity(S0, p_bar, s_bar, g, w)
print("\n灵敏度（每 1%输入变化对应 OV 的相对变化）:")
for k, v in sens.items():
    print(f"  {k}: {v:.2f}")


# ----------------------------------------------------------------------
# 3) 三阶段 DCF：明确期 + 衰减期 + 永续期
# ----------------------------------------------------------------------
def three_stage_dcf(initial_sales, ric0, g0, wacc, rf,
                    explicit_yrs=5, fade_yrs=40, decay=0.10):
    sales = initial_sales
    nopat = sales * 0.073
    npv = 0
    ric, growth = ric0, g0

    for t in range(1, explicit_yrs + 1):
        sales *= (1 + growth)
        nopat = sales * 0.073
        delta_noa = nopat * growth / ric
        fcff = nopat - delta_noa
        npv += fcff / (1 + wacc) ** t

    for t in range(explicit_yrs + 1, explicit_yrs + fade_yrs + 1):
        ric = (ric - wacc) * (1 - decay) + wacc
        growth = (growth - rf) * (1 - decay) + rf
        sales *= (1 + growth)
        nopat = sales * 0.073
        delta_noa = nopat * growth / ric
        fcff = nopat - delta_noa
        npv += fcff / (1 + wacc) ** t

    terminal_nopat = nopat
    terminal_value = terminal_nopat / wacc
    npv += terminal_value / (1 + wacc) ** (explicit_yrs + fade_yrs)
    return npv


cake_value = three_stage_dcf(initial_sales=1399, ric0=0.138, g0=0.208,
                             wacc=0.084, rf=0.042)
print(f"\nCAKE 案例三阶段 DCF 估值: ${cake_value:,.0f} M")


# ----------------------------------------------------------------------
# 4) 蒙特卡罗多路径 DCF
# ----------------------------------------------------------------------
def monte_carlo_dcf(n_paths=5000):
    values = []
    for _ in range(n_paths):
        p = np.random.normal(0.10, 0.02)
        s = np.random.normal(2.0, 0.3)
        gg = np.random.normal(0.05, 0.015)
        ww = np.random.normal(0.09, 0.005)
        if ww > gg and s > 0 and p > gg / s:
            values.append(operating_value(S0, p, s, gg, ww))
    return np.array(values)


mc_values = monte_carlo_dcf()
print(f"\n蒙特卡罗 DCF: 均值=${mc_values.mean():.2f}, "
      f"中位数=${np.median(mc_values):.2f}, "
      f"std=${mc_values.std():.2f}")
print(f"5%–95% 区间: [${np.percentile(mc_values,5):.2f}, ${np.percentile(mc_values,95):.2f}]")


# ----------------------------------------------------------------------
# 5) RIC 衰减曲线
# ----------------------------------------------------------------------
def fade_path(ric0, wacc, years=40, decay=0.10):
    ric = [ric0]
    for _ in range(years):
        new = (ric[-1] - wacc) * (1 - decay) + wacc
        ric.append(new)
    return ric


ric_path = fade_path(0.18, 0.085, decay=0.10)


if __name__ == "__main__":
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(ric_path, label="RIC")
    axes[0].axhline(0.085, color="red", linestyle="--", label="WACC")
    axes[0].set_title("RIC 衰减路径")
    axes[0].set_xlabel("年")
    axes[0].set_ylabel("RIC")
    axes[0].legend()

    axes[1].hist(mc_values, bins=50, color="steelblue", alpha=0.7)
    axes[1].axvline(np.percentile(mc_values, 50), color="red",
                    linestyle="--", label="中位数")
    axes[1].set_title("蒙特卡罗 DCF 估值分布")
    axes[1].legend()
    plt.tight_layout()
    plt.savefig("chapter06_demo.png", dpi=120)
    print("\n[OK] 图表已保存: chapter06_demo.png")
