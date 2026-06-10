from typing import Any
from pathlib import Path
import pandas as pd
import numpy as np

THREADHOLDS = [.5, .55, .6, .65, .7, .75, .8, .85, .9, .95]
OUTPUT_DIR = "/mnt/d/Datasets/FingerNet_Artifacts"

def main():
    results_series: list[pd.Series] = []

    csvs_folder = Path(OUTPUT_DIR).resolve()
    csvs = list(csvs_folder.glob("*.csv"))

    for t in THREADHOLDS:
        for csv in csvs:
            comps = pd.read_csv(csv)
            users = comps["user_1"].unique()
            frr_per_user: list[float] = []
            far_per_user: list[float] = []
            for user in users:
                genuine_attemps = comps[(comps["user_1"] == user) & (comps["user_2"] == user)]
                impostor_attemps = comps[(comps["user_1"] == user) & (comps["user_2"] != user)]
                true_positives = genuine_attemps[genuine_attemps["score"] >= t].count()
                false_rejections = genuine_attemps[genuine_attemps["score"] < t].count()
                true_negatives = impostor_attemps[impostor_attemps["score"] < t].count()
                false_acceptances = impostor_attemps[impostor_attemps["score"] >= t].count()
                frr_per_user.append((false_rejections / (false_rejections + true_positives)) * 100)
                far_per_user.append((false_acceptances / (false_acceptances + true_negatives)) * 100)
            result_serie = {}
            result_serie["dataset"] = csv.name
            result_serie["frr"] = np.mean(frr_per_user)
            result_serie["far"] = np.mean(far_per_user)
            result_serie["threshold"] = t
            results_series.append(result_serie)
    
    result = pd.DataFrame(results_series)
    result.to_csv(f"../mcc_results.csv")

if __name__ == "__main__":
    main()
    
