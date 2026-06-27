import pandas as pd


def generate_insights(df):

    insights = []

    insights.append(f"Total Rows: {len(df)}")
    insights.append(f"Total Columns: {len(df.columns)}")

    # Missing Values
    missing = df.isnull().sum()
    insights.append("\nMissing Values:")
    insights.append(missing.to_string())

    # Numeric Columns
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

        insights.append("\nNumeric Column Statistics:")

        for col in numeric_cols:

            insights.append(f"\n{col}")
            insights.append(f"Maximum : {df[col].max()}")
            insights.append(f"Minimum : {df[col].min()}")
            insights.append(f"Average : {round(df[col].mean(),2)}")

    return "\n".join(insights)