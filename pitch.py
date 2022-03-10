import numpy as np
import csv
import matplotlib.pyplot as plt


def pvq(filename):
    arr = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for line in reader:
            arr.append(line)

    data = np.array(arr[1:])
    data = np.delete(data, obj=0, axis=1)
    data = data.astype(float)
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    pvq = std[2]/mean[2]
    return pvq

#time = [float(row[1]) for row in arr[1:500]]
#pitch = [float(row[2]) for row in arr[1:500]]
#loud = [float(row[4]) for row in arr[1:500]]

#plt.plot(time, pitch)
# plt.savefig("pitch.png")
