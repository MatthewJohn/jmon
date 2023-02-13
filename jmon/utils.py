

from time import sleep

from jmon.logger import logger


def retry(count, interval):
    def wrapper(func):
        def execute_attempt(*args, **kwargs):
            throw_exception = None
            for itx in range(count):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    throw_exception = exc

                    sleep(interval)
                    logger.error(f"Error during step ({itx + 1}/{count}): {exc}")
            else:
                raise throw_exception

        return execute_attempt
    return wrapper
