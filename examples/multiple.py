from heartbeats import RedisSortedSet, heartbeat


def offline_callback(key):
    print(key, ' offline...')

hb = heartbeat(key=lambda x: x, 
               container=RedisSortedSet(), 
               offline_callback=offline_callback)

@hb
def foo(x):
    print(x, ' called...')


# worker
if __name__ == "__main__":
    '''
    Use shell or other progress to call foo()
    '''
    hb.check()
