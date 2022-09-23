unit-test:
	pytest ./tests/unit
lint:
	flake8 ./promql_tester ./tests
	pylint ./promql_tester ./tests
