"""Promql-tester evaluates a list of conditions. Each condition is composed by a promql expression
(expression), a time duration that it needs to be evaluated for (for_seconds) and it will be
evaluated each interval (interval-seconds).
Promql-tester will fail as soon as a condition will fail, or will succeed if all conditions succeed
during the evaluation time.
"""

from .condition import Condition, MalformedConfigException, \
    ConditionConfigException, load_conditions_from_yaml
from .evaluator import Evaluator

__all__ = [
    "Condition",
    "Evaluator",
    "load_conditions_from_yaml",
    "MalformedConfigException",
    "ConditionConfigException",
]
