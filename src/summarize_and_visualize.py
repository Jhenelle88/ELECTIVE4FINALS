"""
Generate summary and data visualizations for CSV outputs.
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os

def summarize_and_visualize(csv_path: str | Path, output_dir: str | Path = None):
    import seaborn as sns
    csv_path = Path(csv_path)
    if output_dir is None:
        output_dir = csv_path.parent
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path)
    summary_path = output_dir / f"{csv_path.stem}_summary.md"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"# Summary for `{csv_path.name}`\n\n")
        f.write(f"**Rows:** {len(df)}  |  **Columns:** {len(df.columns)}\n\n")
        f.write(f"**Columns:** {', '.join(df.columns)}\n\n")
        f.write("<table style='width:100%; border-collapse:collapse;'>\n")
        f.write("<tr style='background-color:#8B0000; color:white;'><th>Column</th><th>Type</th><th>Non-Null</th><th>Unique</th><th>Most Common</th><th>Missing</th></tr>\n")
        for i, col in enumerate(df.columns):
            col_type = df[col].dtype
            non_null = df[col].count()
            unique = df[col].nunique()
            most_common = str(df[col].mode().iloc[0]) if not df[col].mode().empty else "-"
            missing = df[col].isna().sum()
            row_color = "#fff0f0" if i % 2 == 0 else "#ffeaea"
            f.write(f"<tr style='background-color:{row_color};'><td>{col}</td><td>{col_type}</td><td>{non_null}</td><td>{unique}</td><td>{most_common}</td><td>{missing}</td></tr>\n")
        f.write("</table>\n\n")
        # Add numeric summary
        if not df.select_dtypes(include=['number']).empty:
            f.write("<h3>Numeric Columns Summary</h3>\n")
            f.write(df.describe().to_html(classes='summary-table', border=0))

    # Set seaborn style for prettier plots
    # Use a dark red theme for all plots
    sns.set(style="whitegrid", font_scale=1.1)
    dark_red = "#8B0000"

    # Visualize numeric columns
    for col in df.select_dtypes(include=['number']).columns:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col].dropna(), bins=20, kde=True, color=dark_red)
        plt.title(f"Histogram of {col}", fontsize=14, color=dark_red)
        plt.xlabel(col, color=dark_red)
        plt.ylabel("Frequency", color=dark_red)
        plt.gca().spines["top"].set_color(dark_red)
        plt.gca().spines["right"].set_color(dark_red)
        plt.gca().spines["left"].set_color(dark_red)
        plt.gca().spines["bottom"].set_color(dark_red)
        plt.tight_layout()
        plt.savefig(output_dir / f"{csv_path.stem}_{col}_hist.png")
        plt.close()

    # Visualize categorical columns (bar chart for top 10)
    for col in df.select_dtypes(include=['object']).columns:
        plt.figure(figsize=(10, 5))
        vc = df[col].value_counts().head(10)
        sns.barplot(x=vc.index, y=vc.values, color=dark_red)
        plt.title(f"Top 10 {col}", fontsize=14, color=dark_red)
        plt.xlabel(col, color=dark_red)
        plt.ylabel("Count", color=dark_red)
        plt.xticks(rotation=30, ha='right', color=dark_red)
        plt.yticks(color=dark_red)
        plt.gca().spines["top"].set_color(dark_red)
        plt.gca().spines["right"].set_color(dark_red)
        plt.gca().spines["left"].set_color(dark_red)
        plt.gca().spines["bottom"].set_color(dark_red)
        plt.tight_layout()
        plt.savefig(output_dir / f"{csv_path.stem}_{col}_bar.png")
        plt.close()
