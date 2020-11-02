import logging
import time
from functools import wraps
from typing import Callable

from .containers import SortedSetInterface

logger = logging.getLogger()


class heartbeat:

    def __init__(self,
                 key: Callable[..., str],
                 container: SortedSetInterface,
                 enabled=True,
                 offline_callback: Callable[[str], None] = None):
        self.container = container
        self.key = key
        self.enabled = enabled
        self.offline_callback = offline_callback

    def __call__(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            self.refresh(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper
    
    def refresh(self, *args, **kwargs):
        if self.enabled:
            key = str(self.key(*args, **kwargs))
            if key:
                self.container.set(key, time.time())
    
    def check(self, interval: int = 30, check_interval: int = 3):
        logger.info('start checking heart beat...')
        while 1:
            end = time.time() - interval
            keys = self.container.range_by_score(0, end)
            print(keys)
            for key in keys:
                logger.info(f'{key} offline...')
                if self.offline_callback:
                    try:
                        self.offline_callback(key)
                    except:
                        pass

            self.container.delete_by_score_range(0, end)
            time.sleep(check_interval)
