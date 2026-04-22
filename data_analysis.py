import io
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

BG      = "#06111f"
CARD    = "#0d1f3c"
BORDER  = "#1e3a5f"
CYAN    = "#38bdf8"
VIOLET  = "#818cf8"
PINK    = "#f472b6"
GREEN   = "#34d399"
YELLOW  = "#fbbf24"
PALETTE = [CYAN, VIOLET, PINK, GREEN, YELLOW, "#fb923c", "#a78bfa"]


def load_df(file) -> pd.DataFrame:
    name = file.name
    if name.endswith(".xlsx"):
        return pd.read_excel(file)
    if name.endswith(".tsv"):
        return pd.read_csv(file, sep="\t")
    return pd.read_csv(file)


def get_eda(df: pd.DataFrame) -> dict:
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    return {
        "shape": df.shape,
        "num_cols": num_cols,
        "cat_cols": cat_cols,
        "nulls": df.isnull().sum().to_dict(),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "duplicates": int(df.duplicated().sum()),
        "memory": f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB",
        "corr": df[num_cols].corr().round(3) if len(num_cols) >= 2 else None,
    }


def _style(fig, ax):
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(CARD)
    ax.tick_params(colors="#94a3b8", labelsize=10)
    ax.xaxis.label.set_color("#94a3b8")
    ax.yaxis.label.set_color("#94a3b8")
    ax.title.set_color("white")
    for spine in ax.spines.values():
        spine.set_edgecolor(BORDER)


def make_plot(df: pd.DataFrame, plot_type: str,
              x_col=None, y_col=None, hue_col=None) -> bytes:
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    fig, ax = plt.subplots(figsize=(10, 5))
    _style(fig, ax)

    if plot_type == "Histogram" and x_col:
        ax.hist(df[x_col].dropna(), bins=30, color=CYAN, alpha=0.85, edgecolor=BG)
        ax.set_xlabel(x_col); ax.set_ylabel("Frequency")
        ax.set_title(f"Distribution — {x_col}")

    elif plot_type == "Scatter" and x_col and y_col:
        if hue_col:
            for i, cat in enumerate(df[hue_col].unique()):
                mask = df[hue_col] == cat
                ax.scatter(df.loc[mask, x_col], df.loc[mask, y_col],
                           color=PALETTE[i % len(PALETTE)], label=str(cat), alpha=0.7, s=40)
            ax.legend(facecolor=CARD, edgecolor=BORDER, labelcolor="#e2e8f0")
        else:
            ax.scatter(df[x_col], df[y_col], color=CYAN, alpha=0.7, s=40)
        ax.set_xlabel(x_col); ax.set_ylabel(y_col)
        ax.set_title(f"{x_col} vs {y_col}")

    elif plot_type == "Box Plot":
        cols = num_cols[:8]
        data = [df[c].dropna().values for c in cols]
        bp = ax.boxplot(data, patch_artist=True)
        for i, patch in enumerate(bp["boxes"]):
            patch.set_facecolor(PALETTE[i % len(PALETTE)])
            patch.set_alpha(0.8)
        for el in ["whiskers", "caps", "medians", "fliers"]:
            for item in bp[el]:
                item.set(color="#94a3b8")
        ax.set_xticks(range(1, len(cols) + 1))
        ax.set_xticklabels(cols, rotation=30, ha="right")
        ax.set_title("Box Plot — Numeric Columns")

    elif plot_type == "Correlation Heatmap":
        plt.close(fig)
        n = max(7, len(num_cols))
        fig, ax = plt.subplots(figsize=(n, n - 1))
        _style(fig, ax)
        corr = df[num_cols].corr()
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax,
                    linewidths=0.5, linecolor=BG,
                    annot_kws={"color": "white", "size": 9})
        ax.set_title("Correlation Heatmap")

    elif plot_type == "Bar Chart" and x_col:
        y = y_col if y_col else (num_cols[0] if num_cols else None)
        if y:
            agg = df.groupby(x_col)[y].mean().sort_values(ascending=False).head(20)
            bars = ax.bar(range(len(agg)), agg.values, color=CYAN, alpha=0.85)
            for bar, val in zip(bars, agg.values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01 * agg.max(),
                        f"{val:.1f}", ha="center", va="bottom", color="#94a3b8", fontsize=8)
            ax.set_xticks(range(len(agg)))
            ax.set_xticklabels(agg.index, rotation=40, ha="right")
            ax.set_ylabel(y); ax.set_title(f"Avg {y} by {x_col}")

    elif plot_type == "Line Chart" and x_col and y_col:
        s = df.sort_values(x_col)
        ax.plot(s[x_col], s[y_col], color=CYAN, linewidth=2)
        ax.fill_between(s[x_col], s[y_col], alpha=0.12, color=CYAN)
        ax.set_xlabel(x_col); ax.set_ylabel(y_col)
        ax.set_title(f"{y_col} over {x_col}")

    elif plot_type == "Violin":
        cols = num_cols[:6]
        data = [df[c].dropna().values for c in cols]
        parts = ax.violinplot(data, showmeans=True, showmedians=True)
        for i, pc in enumerate(parts["bodies"]):
            pc.set_facecolor(PALETTE[i % len(PALETTE)])
            pc.set_alpha(0.75)
        ax.set_xticks(range(1, len(cols) + 1))
        ax.set_xticklabels(cols, rotation=30, ha="right")
        ax.set_title("Violin Plot — Numeric Columns")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=130, facecolor=BG)
    plt.close(fig)
    buf.seek(0)
    return buf.read()
