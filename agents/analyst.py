import pandas as pd
import matplotlib.pyplot as plt

def analyze_csv(file):
    df = pd.read_csv(file)

    analysis = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "data_types": df.dtypes.astype(str).to_dict(),
        "summary": df.describe(include="all").fillna("").to_dict()
    }
    return df, analysis

def answer_question(df, question):
    question = question.lower()

    if "column" in question:
        return f"Columns in dataset: {', '.join(df.columns)}"
    
    if "row" in question:
        return f"The dataset contains {len(df)} rows."
    
    if "missing" in question:
        missing = df.isnull().sum()
        return missing[missing > 0].to_string() if missing.any() else "No missing values found."
    
    if "duplicate" in question:
        return f"Duplicate rows: {df.duplicated().sum()}"

    if "describe" in question:
        return df.describe(include="all").to_string()

    for column in df.select_dtypes(include="number").columns:
        if column.lower() in question:
            if "average" in question or "mean" in question:
                return f"Average of {column}: {df[column].mean():.2f}"

            if "maximum" in question or "max" in question:
                return f"Maximum of {column}: {df[column].max()}"

            if "minimum" in question or "min" in question:
                return f"Minimum of {column}: {df[column].min()}"

    return "I couldn't identify that question. Try asking about columns, rows, missing values, duplicates, summary, average, maximum, or minimum."

def create_chart(df, column):
    if column not in df.columns:
        return None

    plt.figure(figsize=(8,4))

    if pd.api.types.is_numeric_dtype(df[column]):
        df[column].dropna().plot(kind="hist", bins=20)
        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")

    else:
        df[column].value_counts().head(10).plot(kind="bar")
        plt.title(f"Top Values in {column}")
        plt.xlabel(column)
        plt.ylabel("Count")
        plt.xticks(rotation=45)

    plt.tight_layout()
    return plt.gcf()