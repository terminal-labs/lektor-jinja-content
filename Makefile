test:
	@echo "---> running python tests"
	py.test . --tb=long -svv --cov=lektor_jinja_content
	if command -v black; then black . --check; fi;

coverage: test
	coverage xml
