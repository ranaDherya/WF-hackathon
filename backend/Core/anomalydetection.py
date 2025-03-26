import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest


def detect_outliers(data, contamination=0.05):
    """ Detects and removes outliers using Isolation Forest """
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    outliers = iso_forest.fit_predict(data.select_dtypes(include=[np.number]))

    data['Outlier'] = outliers
    cleaned_data = data[data['Outlier'] == 1].drop(columns=['Outlier'])
    outliers_data = data[data['Outlier'] == -1].drop(columns=['Outlier'])

    return cleaned_data, outliers_data

def generate_report(original_data, cleaned_data, outliers_data):
    """ Generates a detailed report about outliers removal """
    report = f"""
    Outlier Detection and Removal Report
    ====================================
    Total Records: {len(original_data)}
    Records Identified as Outliers: {len(outliers_data)}
    Records After Outlier Removal: {len(cleaned_data)}
    """

    print(report)

    # Save the report
    with open("data/temp/outlier_report.txt", "w") as f:
        f.write(report)

    # Boxplot before and after outlier removal
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    sns.boxplot(data=original_data.select_dtypes(include=[np.number]))
    plt.title("Before Outlier Removal")

    plt.subplot(1, 2, 2)
    sns.boxplot(data=cleaned_data.select_dtypes(include=[np.number]))
    plt.title("After Outlier Removal")

    plt.savefig("data/temp/outlier_removal_visualization.png")
    plt.show()

def run_anomaly_detection(data):
    cleaned_data, outliers_data = detect_outliers(data)
    generate_report(data, cleaned_data, outliers_data)

    cleaned_data.to_csv("data/temp/cleaned_dataset.csv", index=False)
    outliers_data.to_csv("data/temp/removed_outliers.csv", index=False)
    print("Cleaned dataset and outlier records saved successfully.")


