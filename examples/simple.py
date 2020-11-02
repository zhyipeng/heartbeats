import time

from heartbeats import SortedSet, heartbeat


def offline_callback(key):
    print(key, ' offline...')

hb = heartbeat(key=lambda x: x, 
               container=SortedSet(), 
               offline_callback=offline_callback)

@hb
def foo(x):
    print(x, ' called...')


def call(x, sleep_time=0):
    time.sleep(sleep_time)
    foo(x)


if __name__ == "__main__":
    import threading

    foo('a')
    threading.Thread(target=call, args=['a', 1])
    threading.Thread(target=call, args=['a', 4])

    hb.check(interval=3, check_interval=1)
