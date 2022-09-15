"""CLI entrypoint for executing promql-tester"""

import os
import sys
import logging
from prometheus_api_client import PrometheusConnect
from pythonjsonlogger import jsonlogger
from .evaluator import Evaluator
from .condition import load_conditions_from_yaml


def get_custom_format() -> str:
    """
    Return custom format for log formatter.
    """
    log_fields = [
        "asctime",
        "name",
        "levelname",
        "thread",
        "message",
        "pathname",
        "lineno",
    ]
    return " ".join([f"%({field})s" for field in log_fields])


def get_logger():
    """
    Initialize logger with json formatter and specific fields
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = jsonlogger.JsonFormatter(get_custom_format())
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def cli():
    """
    Entrypoint for executing promql-tester.
    Uses PROMETHEUS_URL env var to query prometheus instance, CONDITIONS_PATH to read
    conditions from a configuration yaml file.
    """
    logger = get_logger()

    prom_url = os.environ['PROMETHEUS_URL']
    conditions_path = os.environ['CONDITIONS_PATH']

    conditions = load_conditions_from_yaml(conditions_path)

    prom = PrometheusConnect(url=prom_url, disable_ssl=True)
    evaluator = Evaluator(conditions, prom, logger)
    result = evaluator.evaluate_conditions()
    if result:
        sys.exit(0)
    sys.exit(1)
