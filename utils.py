import os


def file_exists(path):
    return os.path.exists(path)


def is_numeric(df, column):
    return column in df.columns and df[column].dtype.kind in "iuf"


def clean_column_name(name):
    return str(name).strip()