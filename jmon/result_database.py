
import redis

import jmon.config


class ResultMetric:

    def write(self, connection):
        """Base method to write result to redis"""
        raise NotImplementedError

    def read(self, connection):
        """Base method to read result from redis"""
        raise NotImplementedError


class ResultMetricAverageSuccessRate(ResultMetric):
    """Metric for average success rate"""

    def _get_name(self):
        """Get name of metric"""
        return "jmon_result_metric_average_availability"

    def _get_key(self, check, success):
        """Get key from check"""
        success_key_part = "success" if success else "failure"
        return f"{check.name}_{success_key_part}"

    def write(self, result_database, run):
        """Base method to write result to redis"""
        result_database.connection.hincrby(self._get_name(), self._get_key(run.check, run.success))

    def read(self, result_database, check):
        """Base method to read result from redis"""
        # Get average successes/failures
        successes = int(result_database.connection.hget(self._get_name(), self._get_key(check, True)) or 0)
        failures = int(result_database.connection.hget(self._get_name(), self._get_key(check, False)) or 0)

        # Handle no checks
        if (successes + failures) == 0:
            return None
        return successes / (successes + failures)


class ResultDatabase:

    def __init__(self):
        """Create connection to redis"""
        config = jmon.config.Config.get()

        self._connection = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT, 
            password=config.REDIS_PASSWORD
        )

    @property
    def connection(self):
        """Return connection"""
        return self._connection
