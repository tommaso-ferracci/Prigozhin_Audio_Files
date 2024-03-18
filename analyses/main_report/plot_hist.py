import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.data_cleaning.processing import processing_result_for_hist

res_data = pd.read_csv("data/derived/res_data.csv", index_col=0)
weekly_data = processing_result_for_hist(res_data)
index = weekly_data.index
weekly_general = weekly_data["general_complaint"]
weekly_specific = weekly_data["specific_complaint"]

plt.rc("axes", axisbelow=True)
plt.rcParams["grid.color"] = (0.5, 0.5, 0.5, 0.2)
plt.rc("xtick", direction="out", color="#3F5661")
plt.rc("ytick", direction="out", color="#3F5661")
plt.rc("text", usetex=True)
plt.rc("font", family="cm")
plt.rcParams.update({"font.size": 11})

fig, ax = plt.subplots(1, 1, figsize=(8, 5))
ax.bar(index, weekly_general, width=6, alpha=0.9, color="#006BA2", label="Generic complaint")
ax.bar(index, weekly_specific, bottom=weekly_general, color="#3EBCD2", width=6, alpha=0.9, label="Mentioning Shoigu and/or Gerasimov")
ax.axvline(pd.to_datetime("2023-06-25"), color="#0C0C0C", lw=0.5, ymin=0, ymax=0.915, alpha=0.8, marker="o", markersize=1)
ax.axvline(pd.to_datetime("2023-06-04"), color="#0C0C0C", lw=0.5, ymin=0, ymax=0.58, alpha=0.8, marker="o", markersize=1)
ax.set_title(r"\boldmath$\mathrm{Prigozhin\textrm's\;woes}$", loc="left", fontsize=16, color="#3F5661", pad=20)
subtitle_text = "Complaints on Wagner's official telegram channel, weekly count"
ax.text(0, 1.025, subtitle_text, fontsize=11, color="#3F5661", transform=ax.transAxes)
ax.text(0.4, 0.575, "Ukrainian Bakhmut counteroffensive", fontsize=11, color="#3F5661", transform=ax.transAxes)
ax.text(0.7225, 0.9075, "March of justice", fontsize=11, color="#3F5661", transform=ax.transAxes)
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.tick_right()
ax.set_ylim((0, 30))
legend = ax.legend(bbox_to_anchor=(0.5, 0.995))
legend.get_frame().set_linewidth(0)
for text in legend.get_texts():
    text.set_color("#3F5661")
ax.yaxis.grid(True, linestyle="-", linewidth=0.25, which="major") 
ax.tick_params(axis="y", direction="inout", pad=5)
fig.savefig("outputs/main_report/figures/hist.pdf", dpi=300)

