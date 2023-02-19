

from time import sleep

from jmon.logger import logger


def retry(count, interval):
    def wrapper(func):
        def execute_attempt(*args, **kwargs):
            throw_exception = None
            for itx in range(count):
                res = func(*args, **kwargs)
                if res is not None:
                    return res
                else:
                    sleep(interval)
                    logger.error(f"Retrying step ({itx + 1}/{count})")
            else:
                return False

        return execute_attempt
    return wrapper
