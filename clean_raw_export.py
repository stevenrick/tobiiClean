import os
import pandas as pd
import csv
import sys
import Tkinter as tk
import tkFileDialog
from decimal import Decimal
from io import BytesIO


def tsv_to_csv(in_file):	
    f_path = in_file
    par_dir = os.path.dirname(in_file)
    f_name = os.path.split(in_file)[1]

    out_name = os.path.splitext(os.path.join(par_dir, f_name))[0] + "_out.csv"
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
            
    out_gaze = os.path.splitext(os.path.join(csv_dir, csv_name))[0] + "_eye-gaze.csv"
    out_accel = os.path.splitext(os.path.join(csv_dir, csv_name))[0] + "_eye-accel.csv"
    out_gyro = os.path.splitext(os.path.join(csv_dir, csv_name))[0] + "_eye-gyro.csv"
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
    for arg in sys.argv:
        if os.path.splitext(arg)[1] == ".tsv":
            csv_f = tsv_to_csv(arg)
            csv_reduce(csv_f)
    return


main()

