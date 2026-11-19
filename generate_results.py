"""Web figures from the paper's reported tables; no inferred uncertainty."""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SITE = Path(__file__).resolve().parent
data = json.loads((SITE / "results.json").read_text(encoding="utf-8"))
colors = ["#aeb8c5", "#9fb8ce", "#b3a9c4", "#3f71ad"]
style = {
    "font.family": "Arial",
    "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
    "font.size": 18,
    "axes.labelsize": 18,
    "xtick.labelsize": 17,
    "ytick.labelsize": 18,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "axes.spines.bottom": True,
    "axes.edgecolor": "#596570",
    "axes.linewidth": .8,
    "svg.fonttype": "none",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "text.color": "#20262d",
    "axes.labelcolor": "#344454",
    "xtick.color": "#445261",
    "ytick.color": "#20262d",
    "grid.color": "#dce3ea",
    "grid.linewidth": .7,
    "grid.linestyle": "--",
}

def save(fig, name):
    fig.savefig(SITE / (name + ".svg"), format="svg", metadata={"Creator": "Look Ahead to Look Back research project", "Date": None})
    plt.close(fig)

mobile_style = {"font.size": 17, "axes.labelsize": 17, "xtick.labelsize": 17, "ytick.labelsize": 17}

for mobile in (False, True):
    suffix = "-mobile" if mobile else ""
    with plt.rc_context({**style, **mobile_style} if mobile else style):
        for key, benchmark in data["benchmarks"].items():
            fig, ax = plt.subplots(figsize=(4.5, 4.5) if mobile else (9.8, 3.5), layout="constrained")
            values = [r[-1] for r in benchmark["rows"]]
            yy = np.arange(4)
            ax.barh(yy, values, color=colors, height=.55, edgecolor="#65758a", linewidth=.5)
            for y, val in zip(yy, values):
                ax.text(val + 1.4, y, f"{val:.1f}%", va="center", fontsize=17 if mobile else 18, weight="bold" if y == 3 else "normal")
            ax.set_yticks(yy, data["methods"])
            ax.get_yticklabels()[-1].set_fontweight("bold")
            ax.invert_yaxis()
            ax.set_xlim(0, 100)
            ax.set_xticks([0,50,100] if mobile else [0,25,50,75,100])
            ax.set_xlabel("Task success (%)", labelpad=8)
            ax.grid(axis="x")
            ax.set_axisbelow(True)
            ax.tick_params(axis="both", length=0, pad=6 if mobile else 9)
            save(fig, "results-" + key + suffix)

        fig, ax = plt.subplots(figsize=(4.5, 6.8) if mobile else (9.8, 4.4), layout="constrained")
        values = data["ablations"]["success"]
        yy = np.arange(6)
        ax.barh(yy, values, height=.56, color=["#aeb8c5", "#9fb8ce", "#b3a9c4", "#bac2cc", "#c9b8b0", "#3f71ad"], edgecolor="#65758a", linewidth=.5)
        for y,val in zip(yy, values): ax.text(val+1.3,y,f"{val:.1f}%",va="center",weight="bold" if y==5 else "normal")
        ax.set_yticks(yy,[v.replace("Without gripper annotation","Without gripper\nannotation").replace("Without preplay", "Without\npreplay" if mobile else "Without preplay") for v in data["ablations"]["variants"]])
        ax.get_yticklabels()[-1].set_fontweight("bold")
        ax.invert_yaxis();ax.set_xlim(0,100);ax.set_xticks([0,50,100] if mobile else [0,25,50,75,100]);ax.set_xlabel("Complete-task success (%)",labelpad=9)
        ax.grid(axis="x");ax.set_axisbelow(True);ax.tick_params(axis="both",length=0,pad=6 if mobile else 9)
        save(fig,"context-ablations" + suffix)

        fig, ax = plt.subplots(figsize=(4.5, 6.4) if mobile else (10.6, 4.1), layout="constrained")
        y=np.arange(4);a=data["stages"]["without_preplay"];b=data["stages"]["ours"]
        ax.barh(y-.16,a,height=.28,color="#d1d7de",edgecolor="#758191",linewidth=.6,hatch="///",label="Without preplay")
        ax.barh(y+.16,b,height=.28,color="#3f71ad",edgecolor="#315f9e",linewidth=.6,label="Ours")
        for k in range(4):
            ax.text(a[k]+1,k-.16,str(a[k]),va="center",fontsize=17)
            ax.text(b[k]+1,k+.16,str(b[k]),va="center",fontsize=17,weight="bold")
        ax.set_yticks(y,[name.replace("Joint-goal completion","Joint-goal\ncompletion") if mobile else name for name in data["stages"]["names"]]);ax.invert_yaxis();ax.set_xlim(0,100);ax.set_xticks([0,50,100] if mobile else [0,25,50,75,100]);ax.set_xlabel("Stage continuation\nsuccess (%)" if mobile else "Stage continuation success (%)",labelpad=8)
        ax.grid(axis="x");ax.set_axisbelow(True);ax.tick_params(axis="both",length=0,pad=6 if mobile else 9)
        ax.legend(loc="lower left",bbox_to_anchor=(0,1.02),ncol=1 if mobile else 2,frameon=False,fontsize=17)
        save(fig,"stage-continuations" + suffix)
print("Exported 5 desktop and 5 mobile SVG figures from the reported result tables")
