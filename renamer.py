import os
import sys


def find_all_files(starting_dir, match_str):
    results = list()
    for root, dirs, files in os.walk(starting_dir):
        for f in files:
            if match_str in f:
                results.append(os.path.join(root, f))
    return results


def rename(file_list, find_str, replace_str):
    for f_old in file_list:
        f_new = f_old.replace(find_str, replace_str)
        os.rename(f_old, f_new)
    return


def main():
    starting_dir = sys.argv[1]
    match_str = ".tsv"
    file_list = find_all_files(starting_dir, match_str)
    rename(file_list, "_ET.tsv", "_raw_export.tsv")
    return


if __name__ == "__main__":
    main()
