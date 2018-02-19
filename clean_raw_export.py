import os
import pandas as pd
import csv
import sys
from decimal import Decimal
from io import BytesIO


def find_all_files(starting_dir, match_str):
    results = list()
    for root, dirs, files in os.walk(starting_dir):
        for f in files:
            if match_str in f:
                results.append(os.path.join(root, f))
    return results


def tsv_to_csv(in_file):	
    f_path = in_file
    par_dir = os.path.dirname(in_file)
    f_name = os.path.split(in_file)[1]

    f_name_new = f_name.replace("_raw_export", "")

    out_name = os.path.splitext(os.path.join(par_dir, f_name_new))[0] + "_out.csv"
    f_out = os.path.join(par_dir, out_name)
    with open(f_path, 'rb') as tsv_in, open(f_out, 'wb') as csv_out:
        c = tsv_in.read().decode('utf-16').encode('utf-8')
        csv_write = csv.writer(csv_out)
        rowcount = 0
        for row in csv.reader(BytesIO(c), delimiter='\t'):
            rowcount += 1
            tempOut = list()
            for el in row:
                tempOut.append(el)
            csv_write.writerow(tempOut)
    return out_name


def csv_reduce(csv_in):
    csv_path = csv_in
    csv_dir = os.path.dirname(csv_in)
    csv_name = os.path.split(csv_in)[1]

    csv_name_new = csv_name.replace("_out", "")

    out_gaze = os.path.splitext(os.path.join(csv_dir, csv_name_new))[0] + "_eye-gaze.csv"
    out_accel = os.path.splitext(os.path.join(csv_dir, csv_name_new))[0] + "_accel.csv"
    out_gyro = os.path.splitext(os.path.join(csv_dir, csv_name_new))[0] + "_gyro.csv"
    f_out_gaze = os.path.join(csv_dir, out_gaze)
    f_out_accel = os.path.join(csv_dir, out_accel)
    f_out_gyro = os.path.join(csv_dir, out_gyro)
    data = pd.read_csv(csv_path, header=0)
    selection = data[["Recording timestamp", "Gaze point X", "Gaze point Y",
                        "Gaze 3D position combined X", "Gaze 3D position combined Y",
                        "Gaze 3D position combined Z", "Pupil diameter left", "Pupil diameter right", "Gyro X",
                        "Gyro Y", "Gyro Z", "Accelerometer X", "Accelerometer Y", "Accelerometer Z"]]
    del(data)
    milliToSec = lambda x: Decimal(x) / Decimal(1000.0)
    selection["Recording timestamp"] = selection["Recording timestamp"].apply(milliToSec)
    # save gaze data
    selection[["Recording timestamp", "Gaze point X", "Gaze point Y",
                "Gaze 3D position combined X", "Gaze 3D position combined Y", "Gaze 3D position combined Z",
                "Pupil diameter left", "Pupil diameter right"]].dropna().to_csv(f_out_gaze, index=False)
    # save gyro data
    selection[["Recording timestamp", "Gyro X", "Gyro Y", "Gyro Z"]].dropna().to_csv(f_out_gyro, index=False)
    # save accel data
    selection[["Recording timestamp", "Accelerometer X", "Accelerometer Y",
                "Accelerometer Z"]].dropna().to_csv(f_out_accel, index=False)
    os.remove(csv_path)
    return


def main():
    starting_dir = sys.argv[1]
    match_str = "_raw_export.tsv"
    file_list = find_all_files(starting_dir, match_str)
    for f in file_list:
        csv_f = tsv_to_csv(f)
        csv_reduce(csv_f)
    return


if __name__ == "__main__":
    main()
