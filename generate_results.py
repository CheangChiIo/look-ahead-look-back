"""Web figures from the paper's reported tables; no inferred uncertainty."""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SITE = Path(__file__).resolve().parent
data = json.loads((SITE / "results.json").read_text(encoding="utf-8"))
colors = ["#7b8993", "#43847e", "#746b9b", "#c6533b"]
style = {"font.family": "DejaVu Sans", "font.size": 17, "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False, "axes.spines.bottom": False, "svg.fonttype": "none", "figure.facecolor": "white", "axes.facecolor": "white", "text.color": "#263335", "axes.labelcolor": "#566466", "xtick.color": "#647174", "ytick.color": "#263335"}

def save(fig, name):
    fig.savefig(SITE / (name + ".svg"), format="svg", metadata={"Creator": "Look Ahead to Look Back research project", "Date": None})
    plt.close(fig)

with plt.rc_context(style):
    for key, benchmark in data["benchmarks"].items():
        fig, ax = plt.subplots(figsize=(9.8, 3.5), layout="constrained")
        values = [r[-1] for r in benchmark["rows"]]
        yy = np.arange(4)
        ax.barh(yy, values, color=colors, height=.55)
        for y, val in zip(yy, values):
            ax.text(val + 1.4, y, f"{val:.1f}%", va="center", fontsize=17, weight="bold" if y == 3 else "normal")
        ax.set_yticks(yy, data["methods"])
        ax.invert_yaxis()
        ax.set_xlim(0, 100)
        ax.set_xticks([0,25,50,75,100])
        ax.set_xlabel("Task success (%)", labelpad=8)
        ax.grid(axis="x", color="#e5e8e5", lw=.8)
        ax.set_axisbelow(True)
        ax.tick_params(axis="both", length=0, pad=9)
        save(fig, "results-" + key)

    fig, ax = plt.subplots(figsize=(9.8, 4.4), layout="constrained")
    values = data["ablations"]["success"]
    yy = np.arange(6)
    ax.barh(yy, values, height=.56, color=["#abb3b8", "#43847e", "#746b9b", "#8f989d", "#b4a59a", "#c6533b"])
    for y,val in zip(yy, values): ax.text(val+1.3,y,f"{val:.1f}%",va="center",weight="bold" if y==5 else "normal")
    ax.set_yticks(yy,[v.replace("Without gripper annotation","Without gripper\nannotation") for v in data["ablations"]["variants"]])
    ax.invert_yaxis();ax.set_xlim(0,100);ax.set_xticks([0,25,50,75,100]);ax.set_xlabel("Complete-task success (%)",labelpad=9)
    ax.grid(axis="x",color="#e5e8e5",lw=.8);ax.set_axisbelow(True);ax.tick_params(axis="both",length=0,pad=9)
    save(fig,"context-ablations")

    fig, ax = plt.subplots(figsize=(10.6, 4.1), layout="constrained")
    y=np.arange(4);a=data["stages"]["without_preplay"];b=data["stages"]["ours"]
    ax.barh(y-.16,a,height=.28,color="#89949b",label="Without preplay")
    ax.barh(y+.16,b,height=.28,color="#c6533b",label="Ours")
    for k in range(4):
        ax.text(a[k]+1,k-.16,str(a[k]),va="center",fontsize=15)
        ax.text(b[k]+1,k+.16,str(b[k]),va="center",fontsize=15,weight="bold")
    ax.set_yticks(y,data["stages"]["names"]);ax.invert_yaxis();ax.set_xlim(0,100);ax.set_xticks([0,25,50,75,100]);ax.set_xlabel("Stage continuation success (%)",labelpad=8)
    ax.grid(axis="x",color="#e5e8e5",lw=.8);ax.set_axisbelow(True);ax.tick_params(axis="both",length=0,pad=9)
    ax.legend(loc="lower left",bbox_to_anchor=(0,1.02),ncol=2,frameon=False,fontsize=15)
    save(fig,"stage-continuations")
print("Exported 5 SVG data figures from the reported result tables")
