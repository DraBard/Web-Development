import gevent.monkey
from sync import timeit, cpu_bound, io_bound


gevent.monkey.patch_all()


@timeit()
def green_threaded(n_threads, func, *args):
    jobs = []
    for i in range(n_threads):
        jobs.append(gevent.spawn(func, *args))

    gevent.joinall(jobs)


if __name__ == "__main__":
    a = 7777
    b = 200000
    urls = ["http://www.google.com", "http://www.bing.com", "http://www.yahoo.com"]
    green_threaded(10, cpu_bound, a, b)
    green_threaded(10, io_bound, urls)
