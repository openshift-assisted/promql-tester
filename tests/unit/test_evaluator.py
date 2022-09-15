"""
Test evaluator engine.
"""
from unittest import mock
from promql_tester import Evaluator, Condition

# pylint: disable=no-self-use


class TestEvaluator:
    """
    Test evaluator logic.
    """
    def test_execution_once(self):
        """
        Test when condition should only be evaluated once
        """
        mock_time()

        mock_prom = mock.Mock()
        mock_prom.custom_query = mock.Mock(
            return_value=[{'metric': {}, 'value': [1662570142.4, '0']}]
        )

        conditions = [
            Condition({
                "for_seconds": 30,
                "interval_seconds": 30,
                "expression": 'mymock{expression="true"}'
            })
        ]
        evaluator = get_evaluator(conditions, mock_prom)
        assert evaluator.evaluate_conditions() is True

        mock_prom.custom_query.assert_has_calls([
            mock.call(query='mymock{expression="true"}'),
        ])
        assert mock_prom.custom_query.call_count == 1

    def test_execution_multiple_times(self):
        """
        Test when condition is evaluated multiple times.
        """
        mock_time()

        mock_prom = mock.Mock()
        mock_prom.custom_query = mock.Mock(
            return_value=[{'metric': {}, 'value': [1662570142.4, '0']}]
        )

        conditions = [
            Condition({
                "for_seconds": 30,
                "interval_seconds": 10,
                "expression": 'mymock{expression="true"}'
            })
        ]
        evaluator = get_evaluator(conditions, mock_prom)
        assert evaluator.evaluate_conditions() is True

        mock_prom.custom_query.assert_has_calls([
            mock.call(query='mymock{expression="true"}'),
        ])
        assert mock_prom.custom_query.call_count == 3

    def test_execution_failed_condition(self):
        """
        Test when one of the condition fails.
        """
        mock_time()

        mock_prom = mock.Mock()
        mock_prom.custom_query = mock.Mock(
            return_value=[{'metric': {}, 'value': [1662570142.4, '1.1111']}]
        )

        conditions = [
            Condition({
                "for_seconds": 60,
                "interval_seconds": 15,
                "expression": 'mymock{expression="true"}'
            })
        ]
        evaluator = get_evaluator(conditions, mock_prom)
        assert evaluator.evaluate_conditions() is False

        mock_prom.custom_query.assert_has_calls([
            mock.call(query='mymock{expression="true"}'),
        ])
        assert mock_prom.custom_query.call_count == 1


def mock_time():
    """
    Mocks time functions sleep() and time().
    """
    sleeper = mock.patch('time.sleep', return_value=None)
    sleeper.start()

    # mocks starting time and successive tick times
    times = (0, 1, 6, 11, 16, 21, 26, 31)

    timer = mock.Mock()
    timer.side_effect = times

    timer = mock.patch('time.time', timer)
    timer.start()


def get_evaluator(conditions, mock_prom):
    """
    Helper to initialize evaluator.
    """
    mock_logger = mock.Mock()
    return Evaluator(conditions, mock_prom, mock_logger)

# pylint: enable=no-self-use
