#!/usr/bin/env python3

import subprocess
import sys
import os
from itertools import combinations
from pathlib import Path


def usage():
    print("Usage: python3 compare_all.py <folder> [-o <output_file>] [MCC options]")
    print()
    print("  Compares all pairs of .xyt files in <folder> using the mcc binary.")
    print()
    print("Options:")
    print("  -o FILE      Write results to FILE (default: stdout)")
    print()
    print("MCC options:")
    print("  -N {8|16}    Numero de celulas por lado (default: 8)")
    print("  -C STRATEGY  Consolidacao: LSS, LSSR, LSA, LSAR, LGS, NHS (default: LSA)")
    print("  -H           Ativa convex hull")
    print("  -B           Ativa operacoes bit-a-bit")
    print()
    print("Examples:")
    print("  python3 compare_all.py ./impressoes")
    print("  python3 compare_all.py ./impressoes -o resultados.csv")
    print("  python3 compare_all.py ./impressoes -o results.csv -N 16 -C LSSR -B")
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        usage()

    folder = Path(sys.argv[1])
    args = sys.argv[2:]

    output_file = None
    mcc_args = []
    i = 0
    while i < len(args):
        if args[i] == "-o" and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        else:
            mcc_args.append(args[i])
            i += 1

    if not folder.is_dir():
        print(f"Error: '{folder}' is not a directory", file=sys.stderr)
        sys.exit(1)

    xyt_files = sorted(folder.glob("*.xyt"))
    if len(xyt_files) < 2:
        print(f"Error: need at least 2 .xyt files in '{folder}' (found {len(xyt_files)})",
              file=sys.stderr)
        sys.exit(1)

    mcc_bin = str(Path(__file__).resolve().parent / "mcc")
    num_pairs = len(xyt_files) * (len(xyt_files) - 1) // 2

    print(f"=== MCC pairwise comparison ===", file=sys.stderr)
    print(f"Folder : {folder.resolve()}", file=sys.stderr)
    print(f"Files  : {len(xyt_files)}", file=sys.stderr)
    print(f"Binary : {mcc_bin}", file=sys.stderr)
    if mcc_args:
        print(f"Args   : {' '.join(mcc_args)}", file=sys.stderr)
    else:
        print("Args   : (defaults)", file=sys.stderr)
    print(f"Pairs  : {num_pairs}", file=sys.stderr)
    if output_file:
        print(f"Output : {output_file}", file=sys.stderr)
    print(file=sys.stderr)

    fh = open(output_file, "w") if output_file else sys.stdout

    fh.write("file1,file2,score\n")

    for f1, f2 in combinations(xyt_files, 2):
        cmd = [mcc_bin, str(f1), str(f2)] + mcc_args
        proc = subprocess.run(cmd, capture_output=True, text=True)

        if proc.returncode != 0:
            score = "ERROR"
        else:
            score = proc.stdout.strip()

        fh.write(f"{f1.name},{f2.name},{score}\n")

    if output_file:
        fh.close()
        print(f"Results written to {output_file}", file=sys.stderr)


if __name__ == "__main__":
    main()
