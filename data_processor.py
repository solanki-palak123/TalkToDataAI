import pandas as pd


def load_data(file):
    return pd.read_csv(file.name)


def get_summary(df):

    summary = f"""
Rows: {df.shape[0]}
Columns: {df.shape[1]}

Column Names:
{list(df.columns)}

Data Types:
{df.dtypes}

Missing Values:
{df.isnull().sum()}

First 5 Rows:

{df.head().to_string()}
"""

    return summary