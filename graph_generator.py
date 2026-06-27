import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def generate_graph(df, config):

    chart = config.get("chart_type", "").lower()
    x = config.get("x_column")
    y = config.get("y_column")
    agg = config.get("aggregation", "none").lower()

    plt.figure(figsize=(10,6))

    # -------- BAR --------
    if chart == "bar":
        plot_df = df.copy()

        if agg == "sum":
            plot_df = df.groupby(x)[y].sum().reset_index()

        elif agg == "mean":
            plot_df = df.groupby(x)[y].mean().reset_index()

        elif agg == "count":
            plot_df = df.groupby(x)[y].count().reset_index()

        plt.bar(plot_df[x], plot_df[y])

    # -------- LINE --------
    elif chart == "line":
        plot_df = df.copy()

        if agg == "sum":
            plot_df = df.groupby(x)[y].sum().reset_index()

        plt.plot(plot_df[x], plot_df[y], marker="o")

    # -------- SCATTER --------
    elif chart == "scatter":
        plt.scatter(df[x], df[y])

    # -------- PIE --------
    elif chart == "pie":

        if agg == "sum":
            plot_df = df.groupby(x)[y].sum()

        elif agg == "count":
            plot_df = df.groupby(x)[y].count()

        else:
            plot_df = df.groupby(x)[y].mean()

        plt.pie(
            plot_df.values,
            labels=plot_df.index,
            autopct="%1.1f%%"
        )

    # -------- HISTOGRAM --------
    elif chart == "histogram":
        plt.hist(df[x], bins=20)

    # -------- BOX --------
    elif chart == "box":
        plt.boxplot(df[x])

    # -------- HEATMAP --------
    elif chart == "heatmap":
        corr = df.select_dtypes(include="number").corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm")

    else:
        raise Exception("Unsupported chart")

    plt.title(chart.upper())
    plt.xticks(rotation=45)
    plt.tight_layout()

    filename = "graph.png"

    plt.savefig(filename)
    plt.close()

    return filename