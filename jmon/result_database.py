
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
        """Increment count for success/failure for run"""
        result_database.connection.hincrby(self._get_name(), self._get_key(run.check, run.success))

    def read(self, result_database, check):
        """Get success rate fraction"""
        # Get average successes/failures
        successes = int(result_database.connection.hget(self._get_name(), self._get_key(check, True)) or 0)
        failures = int(result_database.connection.hget(self._get_name(), self._get_key(check, False)) or 0)

        # Handle no checks
        if (successes + failures) == 0:
            return None
        return successes / (successes + failures)


class ResultMetricLatestStatus(ResultMetric):
    """Metric for latest result status"""

    def _get_name(self):
        """Get name of metric"""
        return "jmon_result_metric_latest_status"

    def _get_key(self, check):
        """Get key from check"""
        return check.name

    def write(self, result_database, run):
        """Write result to redis"""
        result_database.connection.hset(self._get_name(), self._get_key(run.check), 1 if run.success else 0)

    def read(self, result_database, check):
        """Get latest check result status"""
        # Get average successes/failures
        result = result_database.connection.hget(self._get_name(), self._get_key(check))
        if result is None:
            return None

        result = int(result.decode('utf-8'))

        # Return True/False based on 1 or 2
        if result == 1:
            return True
        elif result == 0:
            return False
        # Default to None (not run), assuming the metric doesn't exist
        return None


class ResultRegisterResult(ResultMetric):
    """Value to register check with result for reference in UI"""

    def _get_name(self, run):
        """Get name of metric"""
        return f"{run.check.get_result_key()}{run.get_run_key()}"

    def write(self, result_database, run):
        """Write result to redis"""
        result_database.connection.set(
            self._get_name(run),
            1 if run.success else 0
        )

        # Add expiration to key
        result_database.connection.expire(
            self._get_name(run),
            jmon.config.Config.get().UI_RESULT_EXPIRE
        )

    def read(self, result_database, run):
        """Get latest check result status"""
        return result_database.connection.get(self._get_name(run))

    def get_all_runs_by_check(self, result_database, check):
        """Get all runs for check"""
        result_key = check.get_result_key()
        return sorted([
            key.decode('utf-8').replace(result_key, '')
            for key in result_database.connection.scan_iter(f"{result_key}*")
        ])

    def get_latest_run(self, result_database, check):
        """Get latest run for check"""
        runs = self.get_all_runs_by_check(result_database=result_database, run=check)
        if runs:
            return runs[-1]
        return None


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
