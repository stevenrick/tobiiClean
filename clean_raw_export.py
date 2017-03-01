import os
import pandas as pd
import csv
import Tkinter as tk
from Tkinter import filedialog
from decimal import Decimal
from io import BytesIO


def tsv_to_csv(parDir):
    print("Convert TSV to CSV")
    for f in os.listdir(parDir):
        if ".tsv" in f:
            f_path = os.path.join(parDir, f)
            out_name = os.path.splitext(os.path.join(parDir, f))[0] + "_out.csv"
            f_out = os.path.join(parDir, out_name)
            with open(f_path, 'rb') as tsv_in, open(f_out, 'wb') as csv_out:
                c = tsv_in.read().decode('utf-16').encode('utf-8')
                csv_write = csv.writer(csv_out)
                rowcount = 0
                for row in csv.reader(BytesIO(c), delimiter='\t'):
                    # print rowcount, row
                    rowcount += 1
                    tempOut = list()
                    for el in row:
                        # print el
                        tempOut.append(el)
                    # print tempOut
                    csv_write.writerow(tempOut)
    print("Convert Done")
    return


def csv_reduce(parDir):
    print("Reduce / Split CSV")
    for f in os.listdir(parDir):
        if "_out.csv" in f:
            f_path = os.path.join(parDir, f)
            out_gaze = os.path.splitext(os.path.join(parDir, f))[0] + "_eye-gaze.csv"
            out_accel = os.path.splitext(os.path.join(parDir, f))[0] + "_eye-accel.csv"
            out_gyro = os.path.splitext(os.path.join(parDir, f))[0] + "_eye-gyro.csv"
            f_out_gaze = os.path.join(parDir, out_gaze)
            f_out_accel = os.path.join(parDir, out_accel)
            f_out_gyro = os.path.join(parDir, out_gyro)
            data = pd.read_csv(f_path, header=0)
            # print list(data.columns.values)
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
    print("Reduce / Split Done")
    return


def main():
    root = tk.Tk()
    root.withdraw()
    parDir = filedialog.askdirectory()
    tsv_to_csv(parDir)
    csv_reduce(parDir)
    return


main()

