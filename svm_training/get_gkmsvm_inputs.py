import os
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def main():
    setup_pool()


def setup_pool():
    pool_inputs = []
    for cluster in range(1, 25):
        for fold in range(10):
            pool_inputs.append((cluster, fold))
    with ProcessPoolExecutor(max_workers=40) as pool:
        merge=pool.map(run_seqdata, pool_inputs)


def run_seqdata(inputs):
    print('Cluster: ' + str(inputs[0]) + '; Fold: ' + str(inputs[1]))
    os.system('python run_seqdataloader.py ' + str(inputs[0]) + ' ' + str(inputs[1]))


if __name__ == "__main__":
    main()
