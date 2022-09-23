"""
Tests about conditions and related tools.
"""
# pylint: disable=no-self-use

import os
import pytest

from promql_tester import Condition, load_conditions_from_yaml, \
    MalformedConfigException, ConditionConfigException

missing_fields_conditions_configs = [
    {
        # missing `expression`
        "for_seconds": 300,
        "interval_seconds": 30,
        "threshold": {
            "upper": 10,
            "lower": 2,
        }
    },
    {
        "expression": 'avg(mymetric{mylabel="myvalue"})',
        # missing `for_seconds`
        "interval_seconds": 30,
        "threshold": {
            "upper": 10,
            "lower": 2,
        }
    },
    {
        "expression": 'avg(mymetric{mylabel="myvalue"})',
        "for_seconds": 300,
        # missing `interval_seconds`
        "threshold": {
            "upper": 10,
            "lower": 2,
        }
    },
]


class TestConditions:
    """Test conditions"""
    def test_load_malformed_conditions(self):
        """Test when conditions file is malformed"""
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "./fixtures/malformed_conditions.yaml")

        with pytest.raises(MalformedConfigException):
            _ = load_conditions_from_yaml(filename)

    def test_load_missing_file(self):
        """Test when conditions file is missing"""
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "./fixtures/notafile.yaml")

        with pytest.raises(FileNotFoundError):
            _ = load_conditions_from_yaml(filename)

    def test_load_conditions(self):
        """Test when conditions file is read from file"""
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "./fixtures/conditions.yaml")

        conditions = load_conditions_from_yaml(filename)
        expected_conditions_count = 1
        assert len(conditions) == expected_conditions_count

        for condition in conditions:
            assert isinstance(condition, Condition)

    def test_default_threshold(self):
        """Test when conditions has default threshold"""
        raw_config = {
            "expression": 'avg(mymetric{mylabel="myvalue"})',
            "for_seconds": 300,
            "interval_seconds": 30,
        }
        condition = Condition(raw_config)
        assert not condition.is_within_threshold(1)
        assert not condition.is_within_threshold(-1)
        assert condition.is_within_threshold(0)

    def test_declared_threshold(self):
        """Test when conditions has declared a threshold"""
        raw_config = {
            "expression": 'avg(mymetric{mylabel="myvalue"})',
            "for_seconds": 300,
            "interval_seconds": 30,
            "threshold": {
                "upper": 10,
                "lower": 2,
            }
        }
        condition = Condition(raw_config)
        assert not condition.is_within_threshold(1)
        assert not condition.is_within_threshold(11)
        assert condition.is_within_threshold(8)
        assert condition.is_within_threshold(10)
        assert condition.is_within_threshold(2)

    @pytest.mark.parametrize("missing_fields_conditions_config", missing_fields_conditions_configs)
    def test_missing_fields(self, missing_fields_conditions_config):
        """
        Test when conditions is trying to be initialized
        with config with missing fields
        """
        with pytest.raises(ConditionConfigException):
            _ = Condition(missing_fields_conditions_config)

# pylint: enable=no-self-use
