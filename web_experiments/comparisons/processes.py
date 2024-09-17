from multiprocessing import Process
from sync import timeit, cpu_bound, io_bound

@timeit()
def multiprocess(n_processes, func, *args):
    jobs = []
    for i in range(n_processes):
        process = Process(target=func, args=args)
        jobs.append(process)

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()


if __name__ == '__main__':
    a = 7777
    b = 200000
    urls = ['http://www.google.com', 'http://www.bing.com', 'http://www.yahoo.com']
    multiprocess(10, cpu_bound, a, b)
    multiprocess(10, io_bound, urls)