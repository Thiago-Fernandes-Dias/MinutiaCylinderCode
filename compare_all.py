#!/usr/bin/env python3

import functools
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import sys

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
    ("/Datasets/FingerNet_Artifacts/CrossMatch_Sample_DB/xyt", "CrossMatch_Sample_DB"),
    ("/Datasets/FingerNet_Artifacts/UareU_sample_DB/xyt", "UareU_sample_DB"),
]

OUTPUT_DIR = "/Scores"
GALLERY_IMPRESSIONS = [1, 2, 3, 4]
QUERY_IMPRESSIONS = [5, 6, 7, 8]


def compare_pair(pair, mcc_binary):
    file_1, file_2 = pair
    command = [mcc_binary, str(file_1), str(file_2), "-N", str(CELLS_PER_SIDE), "-C", STRATEGY]
    if USE_CONVEX_HULL:
        command.append("-H")
    if USE_BIT_OPERATIONS:
        command.append("-B")

    process = subprocess.run(command, capture_output=True, text=True)
    if process.returncode != 0:
        score = -1
    else:
        score = process.stdout.strip()

    user_1, impression_1 = file_1.stem.split('_')
    user_2, impression_2 = file_2.stem.split('_')
    return f"{user_1},{impression_1},{user_2},{impression_2},{score}\n"


def main():
    mcc_binary = str(Path(__file__).resolve().parent / "mcc")
    max_workers = int(os.environ.get("NUM_WORKERS", os.cpu_count() or 4))
    compare_worker = functools.partial(compare_pair, mcc_binary=mcc_binary)

    target_dir = os.environ.get("OUTPUT_DIR")
    if target_dir:
        output_dir = Path(target_dir)
    elif Path(OUTPUT_DIR).exists():
        output_dir = Path(OUTPUT_DIR)
    elif Path("/Output").exists():
        output_dir = Path("/Output")
    else:
        output_dir = Path(__file__).resolve().parent.parent / "scores" / "MCC"

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        output_dir = Path(__file__).resolve().parent / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

    datasets_roots = []
    env_datasets = os.environ.get("DATASETS")
    if env_datasets:
        p_env = Path(env_datasets)
        datasets_roots.append(p_env)
        if not p_env.exists() and Path(f"{env_datasets}s").exists():
            datasets_roots.append(Path(f"{env_datasets}s"))
    datasets_roots.extend([
        Path("/Datasets"),
        Path("/media/thiago-dias/BACKUP/Datasets"),
        Path("/media/thiago-dias/BACKUP/Dataset"),
    ])

    for db_name, results_file_name in DATASETS:
        candidates = [
            Path(db_name),
            Path(db_name.replace("FingerNet_Artifacts", "FVC_FingerNet_Artifacts")),
        ]
        for root in datasets_roots:
            candidates.extend([
                root / "FVC_FingerNet_Artifacts" / results_file_name / "xyt",
                root / "FingerNet_Artifacts" / results_file_name / "xyt",
                root / results_file_name / "xyt",
            ])

        path = next((c for c in candidates if c.exists()), Path(db_name))
        xyt_files = sorted(path.glob("*.xyt"))
        if len(xyt_files) < 2:
            continue

        files_by_sample = {}
        for f in xyt_files:
            parts = f.stem.split('_')
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                files_by_sample[(int(parts[0]), int(parts[1]))] = f

        available_subjects = sorted({subject for subject, _ in files_by_sample.keys()})
        if results_file_name.endswith("_B") and 110 in available_subjects and 102 in available_subjects:
            subjects = [s for s in range(102, 111) if s in available_subjects]
        else:
            subjects = available_subjects

        mated_pairs = [
            (files_by_sample[(s, q)], files_by_sample[(s, g)])
            for s in subjects
            for q in QUERY_IMPRESSIONS
            for g in GALLERY_IMPRESSIONS
            if (s, q) in files_by_sample and (s, g) in files_by_sample
        ]
        non_mated_pairs = [
            (files_by_sample[(s1, q)], files_by_sample[(s2, g)])
            for s1 in subjects
            for q in QUERY_IMPRESSIONS
            for s2 in subjects if s2 != s1
            for g in GALLERY_IMPRESSIONS
            if (s1, q) in files_by_sample and (s2, g) in files_by_sample
        ]
        pairs = mated_pairs + non_mated_pairs
        print(f"Processing {results_file_name} ({len(pairs)} comparisons) from {path}...", flush=True)

        with open(output_dir / f"{results_file_name}.csv", "w") as file_handle:
            file_handle.write("user_1,impression_1,user_2,impression_2,score\n")
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                file_handle.writelines(executor.map(compare_worker, pairs))


if __name__ == "__main__":
    main()
