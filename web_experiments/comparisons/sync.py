from urllib.request import urlopen
import time
import functools

class timeit:
    def __call__(self, f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            with self:
                return f(*args, **kwargs)
        return decorated
    
    def __enter__(self):
        self.start = time.time()

    def __exit__(self, *args, **kwargs):
        elapsed = time.time() - self.start
        print(f'Elapsed time: {elapsed}')

def cpu_bound(a, b):
    return a**b

def io_bound(urls):
    data = []
    for url in urls:
        data.append(urlopen(url).read())
    return data

@timeit()
def simple_1(N, a, b):
    for i in range(N):
        cpu_bound(a, b)

@timeit()
def simple_2(N, urls):
    for i in range(N):
        io_bound(urls)



if __name__ == '__main__':
    a = 7777
    b = 200000
    urls = ['http://www.google.com', 'http://www.bing.com', 'http://www.yahoo.com']
    simple_1(10, a, b)
    simple_2(10, urls)