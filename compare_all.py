#!/usr/bin/env python3

import subprocess
import sys
import os
from itertools import combinations, permutations
from pathlib import Path

CELLS_PER_SIDE = 16
STRATEGY = "LSA"
USE_CONVEX_HULL = False
USE_BIT_OPERATIONS = False

DATASETS = [
    ("/Datasets/FingerNet_Artifacts/FVC2000_DB1_A/xyt", "FVC2000_DB1_A"),
    ("/Datasets/FingerNet_Artifacts/FVC2000_DB1_B/xyt", "FVC2000_DB1_B"),
    ("/Datasets/FingerNet_Artifacts/FVC2000_DB2_A/xyt", "FVC2000_DB2_A"),
    ("/Datasets/FingerNet_Artifacts/FVC2000_DB2_B/xyt", "FVC2000_DB2_B"),
    ("/Datasets/FingerNet_Artifacts/FVC2000_DB3_A/xyt", "FVC2000_DB3_A"),
    ("/Datasets/FingerNet_Artifacts/FVC2000_DB3_B/xyt", "FVC2000_DB3_B"),
    ("/Datasets/FingerNet_Artifacts/FVC2000_DB4_A/xyt", "FVC2000_DB4_A"),
    ("/Datasets/FingerNet_Artifacts/FVC2000_DB4_B/xyt", "FVC2000_DB4_B"),
    ("/Datasets/FingerNet_Artifacts/FVC2002_DB1_A/xyt", "FVC2002_DB1_A"),
    ("/Datasets/FingerNet_Artifacts/FVC2002_DB1_B/xyt", "FVC2002_DB1_B"),
    ("/Datasets/FingerNet_Artifacts/FVC2002_DB2_A/xyt", "FVC2002_DB2_A"),
    ("/Datasets/FingerNet_Artifacts/FVC2002_DB2_B/xyt", "FVC2002_DB2_B"),
    ("/Datasets/FingerNet_Artifacts/FVC2002_DB3_A/xyt", "FVC2002_DB3_A"),
    ("/Datasets/FingerNet_Artifacts/FVC2002_DB3_B/xyt", "FVC2002_DB3_B"),
    ("/Datasets/FingerNet_Artifacts/FVC2002_DB4_A/xyt", "FVC2002_DB4_A"),
    ("/Datasets/FingerNet_Artifacts/FVC2002_DB4_B/xyt", "FVC2002_DB4_B"),
    ("/Datasets/FingerNet_Artifacts/FVC2004_DB1_A/xyt", "FVC2004_DB1_A"),
    ("/Datasets/FingerNet_Artifacts/FVC2004_DB1_B/xyt", "FVC2004_DB1_B"),
    ("/Datasets/FingerNet_Artifacts/FVC2004_DB2_A/xyt", "FVC2004_DB2_A"),
    ("/Datasets/FingerNet_Artifacts/FVC2004_DB2_B/xyt", "FVC2004_DB2_B"),
    ("/Datasets/FingerNet_Artifacts/FVC2004_DB3_A/xyt", "FVC2004_DB3_A"),
    ("/Datasets/FingerNet_Artifacts/FVC2004_DB3_B/xyt", "FVC2004_DB3_B"),
    ("/Datasets/FingerNet_Artifacts/FVC2004_DB4_A/xyt", "FVC2004_DB4_A"),
    ("/Datasets/FingerNet_Artifacts/FVC2004_DB4_B/xyt", "FVC2004_DB4_B"),
]

OUTPUT_DIR = "/Output"


def main():
    mcc_bin = str(Path(__file__).resolve().parent / "mcc")

    for db_name, results_file_name in DATASETS:
        path = Path(db_name)
        xyt_files = sorted(path.glob("*.xyt"))
        if len(xyt_files) < 2:
            continue
        with open(f"/Output/{results_file_name}.csv", "w") as fh:
            fh.write("user_1,impression_1,user_2,impression_2,score\n")
            for f1, f2 in permutations(xyt_files, 2):
                cmd = [mcc_bin, str(f1), str(f2), "-N", f"{CELLS_PER_SIDE}", "-C", f"{STRATEGY}"]
                if USE_CONVEX_HULL:
                    cmd.append("-H")
                if USE_BIT_OPERATIONS:
                    cmd.append("-B")
                proc = subprocess.run(cmd, capture_output=True, text=True)
                if proc.returncode != 0:
                    score = -1
                else:
                    score = proc.stdout.strip()
                user_1, impression_1 = f1.name.replace(".xyt", "").split('_')
                user_2, impression_2 = f2.name.replace(".xyt", "").split('_')
                fh.write(f"{user_1},{impression_1},{user_2},{impression_2},{score}\n")


if __name__ == "__main__":
    main()
