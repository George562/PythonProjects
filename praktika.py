from dask.distributed import LocalCluster, Client
import dask
import dask.dataframe as dd
import numpy as np
from time import time
import matplotlib.pyplot as plt

max_workers = 10; max_thread = 8

dask.config.set({"optimization.fuse.active": True})
data = np.zeros((max_thread, max_workers), float)

for j in range(1, max_thread + 1):
    for i in range(1, max_workers + 1):
        with LocalCluster(processes=False, n_workers=i, threads_per_worker=j) as cluster:
            with Client(cluster) as client:
                start = time()
                df = dd.read_csv('5m Sales Records.csv')
                count = df.Unit_Price.count()
                sum = df.Unit_Price.sum()

                (sum / count).compute()
                data[j - 1][i - 1] = time() - start
                # print("threads_per_worker: %d;\tn_workers: %d;\ttime: %.4f" % (j, i, data[j - 1][i - 1]))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("threads"); ax.set_ylabel("workers"); ax.set_zlabel("time")

best_worker = 0; best_thread = 0; best_time = 10e6

print("workers:\t" + "\t".join([str(i) for i in range(1, max_workers + 1)]))

for j in range(1, max_thread + 1):
    print(f"threads: {j}\t", end="")
    for i in range(1, max_workers + 1):
        ax.plot(j, i, data[j - 1][i - 1], color='orange', marker = 'o')
        if best_time > data[j - 1][i - 1]:
            best_worker = i
            best_thread = j
            best_time = data[j - 1][i - 1]
        print("%.4f\t" % data[j - 1][i - 1], end="")
    print()

print("best_worker = %d\nbest_thread = %d\nbest_time = %.4f" % (best_worker, best_thread, best_time))

plt.show()