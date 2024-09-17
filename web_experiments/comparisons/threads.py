from threading import Thread
from sync import timeit, cpu_bound, io_bound


@timeit()
def threaded(n_threads, func, *args):
    jobs = []
    for i in range(n_threads):
        thread = Thread(target=func, args=args)
        jobs.append(thread)

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()


if __name__ == '__main__':
    a = 7777
    b = 200000
    urls = ['http://www.google.com', 'http://www.bing.com', 'http://www.yahoo.com']
    threaded(10, cpu_bound, a, b)
    threaded(10, io_bound, urls)