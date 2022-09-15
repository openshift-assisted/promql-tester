"""Evaluates conditions"""

import time
from .condition import FailedCondition


EVALUATOR_DEFAULT_TICK = 5


class Evaluator:  # pylint: disable=too-few-public-methods
    """This class handles the logic how and when to evaluate a list of conditions."""
    def __init__(self, conditions, prom, logger, tick=EVALUATOR_DEFAULT_TICK):
        """Initializes needed parameters and dependencies"""
        self._conditions = conditions
        self._executions = {}
        self._prom = prom
        self._tick = tick
        self._logger = logger
        self._start_time = None

    def evaluate_conditions(self):
        """Evaluate each condition in the condition list each tick time (by default 5s)"""
        self._logger.info(f"Start evaluating conditions: {self._conditions}")
        self._start_time = time.time()

        try:
            while len(self._conditions) > 0:
                for condition in self._conditions:
                    # Raise FailedCondition if condition fails
                    self._evaluate(condition)
                    time.sleep(self._tick)
        except FailedCondition:
            return False
        return True

    def _evaluate(self, condition):
        """
        Evaluates the condition if necessary. If the condition has run for more
        than `for_seconds` time, it will be removed from evaluation.
        Raises `FailedCondition` exception if a condition fails
        """
        execution_time = time.time()

        if self._is_condition_expired(condition, execution_time):
            self._conditions.remove(condition)
            return None  # Condition expired and not failed so far, thus passed
        self._logger.debug(f"Evaluating condition {condition}")

        if not self._skip_condition(condition, execution_time):
            expr = condition.expression
            res = self._prom.custom_query(query=expr)
            self._logger.debug(f"Query for condition {condition.id} returned: {res}")

            if not _is_valid_result(condition, res):
                self._logger.error(f"Failed condition: {condition}")
                raise FailedCondition(f"Condition {condition} failed")

            self._logger.info(f"Successful condition: {condition}")
            self._mark_as_executed(condition.id, execution_time)
        return None

    def _skip_condition(self, condition, execution_time):
        """Returns True if the condition is not to be evaluated at this time"""
        last_execution = self._get_last_execution(condition.id)
        if not last_execution:
            return False
        if last_execution + condition.interval_seconds <= execution_time:
            return False
        self._logger.debug(f"Skipping condition {condition.id}")

        return True

    def _get_last_execution(self, condition_id):
        """Get last execution time for the given condition. None if it never executed"""
        if condition_id in self._executions:
            return self._executions[condition_id]
        return None

    def _mark_as_executed(self, condition_id, execution_time):
        """Mark as executed the given condition at the given execution time"""
        self._executions[condition_id] = execution_time

    def _is_condition_expired(self, condition, execution_time):
        """Checks whether a condition has "expired" (run for `for_seconds` seconds)"""
        expiration_time = self._start_time + condition.for_seconds
        return expiration_time < execution_time


def _is_valid_result(condition, result):
    """Checks if result for given condition is valid
    Example raw result:
    [{'metric': {}, 'value': [1662570142.4, '1.1111111111111112']}]
    """
    if len(result) < 1:
        return False
    if "value" not in result[0]:
        return False
    if len(result[0]["value"]) < 2:
        return False
    value = float(result[0]["value"][1])
    return condition.is_within_threshold(value)
