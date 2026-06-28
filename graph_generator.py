import matplotlib.pyplot as plt
import seaborn as sns


def generate_graph(df, result):

    chart = result.get("chart_type", "").lower()
    x_col = result.get("x_column")
    y_col = result.get("y_column")
    agg = result.get("aggregation", "none").lower()

    if x_col not in df.columns:
        raise ValueError(f"{x_col} not found in dataset.")

    if y_col and y_col not in df.columns:
        raise ValueError(f"{y_col} not found in dataset.")

    # -------------------------------
    # Prepare Data
    # -------------------------------

    if chart in ["bar", "line", "pie"]:

        if agg == "sum":
            data = df.groupby(x_col)[y_col].sum()

        elif agg == "mean":
            data = df.groupby(x_col)[y_col].mean()

        elif agg == "count":
            data = df.groupby(x_col).size()

        else:
            data = df[x_col].value_counts()

        data = data.sort_values(ascending=False)

    # -------------------------------
    # BAR CHART
    # -------------------------------

    if chart == "bar":

        plt.figure(figsize=(16,8))

        data.plot(
            kind="bar",
            color="steelblue"
        )

        plt.title(f"{y_col} by {x_col}")
        plt.xlabel(x_col)
        plt.ylabel(y_col if y_col else "Count")
        plt.xticks(rotation=90)

        plt.tight_layout()

    # -------------------------------
    # PIE CHART
    # -------------------------------

    elif chart == "pie":

        # Too many categories → convert to bar chart
        if len(data) > 10:

            plt.figure(figsize=(16,8))

            data.plot(
                kind="bar",
                color="steelblue"
            )

            plt.title(f"{y_col} by {x_col} (Bar chart used because Pie chart is unsuitable for many categories)")
            plt.xticks(rotation=90)

            plt.tight_layout()

        else:

            plt.figure(figsize=(8,8))

            plt.pie(
                data,
                labels=data.index,
                autopct="%1.1f%%",
                startangle=90
            )

            plt.title(f"{y_col} by {x_col}")

            plt.tight_layout()

    # -------------------------------
    # LINE CHART
    # -------------------------------

    elif chart == "line":

        plt.figure(figsize=(14,6))

        plt.plot(
            data.index,
            data.values,
            marker="o"
        )

        plt.title(f"{y_col} by {x_col}")

        plt.xlabel(x_col)
        plt.ylabel(y_col)

        plt.xticks(rotation=45)

        plt.grid(True)

        plt.tight_layout()

    # -------------------------------
    # SCATTER
    # -------------------------------

    elif chart == "scatter":

        plt.figure(figsize=(10,6))

        plt.scatter(
            df[x_col],
            df[y_col]
        )

        plt.xlabel(x_col)
        plt.ylabel(y_col)

        plt.title("Scatter Plot")

        plt.tight_layout()

    # -------------------------------
    # HISTOGRAM
    # -------------------------------

    elif chart == "histogram":

        plt.figure(figsize=(10,6))

        plt.hist(
            df[y_col],
            bins=20
        )

        plt.title("Histogram")

        plt.xlabel(y_col)

        plt.tight_layout()

    # -------------------------------
    # BOXPLOT
    # -------------------------------

    elif chart == "box":

        plt.figure(figsize=(8,6))

        sns.boxplot(
            y=df[y_col]
        )

        plt.title("Box Plot")

        plt.tight_layout()

    # -------------------------------
    # HEATMAP
    # -------------------------------

    elif chart == "heatmap":

        plt.figure(figsize=(10,8))

        sns.heatmap(
            df.corr(numeric_only=True),
            annot=True,
            cmap="coolwarm"
        )

        plt.title("Correlation Heatmap")

        plt.tight_layout()

    else:

        raise ValueError(f"Unsupported chart type: {chart}")

    filename = "graph.png"

    plt.savefig(filename)

    plt.close()

    return filename