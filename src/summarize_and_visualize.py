"""
Generate summary and data visualizations for CSV outputs.
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os

def summarize_and_visualize(csv_path: str | Path, output_dir: str | Path = None):
    csv_path = Path(csv_path)
    if output_dir is None:
        output_dir = csv_path.parent
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path)
    summary_path = output_dir / f"{csv_path.stem}_summary.txt"
    with open(summary_path, "w") as f:
        f.write(f"Summary for {csv_path.name}\n")
        f.write(f"Rows: {len(df)}\n")
        f.write(f"Columns: {len(df.columns)}\n")
        f.write(f"Columns: {list(df.columns)}\n\n")
        f.write(str(df.describe(include='all')))

    # Visualize numeric columns
    for col in df.select_dtypes(include=['number']).columns:
        plt.figure()
        df[col].hist(bins=20)
        plt.title(f"Histogram of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(output_dir / f"{csv_path.stem}_{col}_hist.png")
        plt.close()

    # Visualize categorical columns (bar chart for top 10)
    for col in df.select_dtypes(include=['object']).columns:
        plt.figure()
        df[col].value_counts().head(10).plot(kind='bar')
        plt.title(f"Top 10 {col}")
        plt.xlabel(col)
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(output_dir / f"{csv_path.stem}_{col}_bar.png")
        plt.close()
