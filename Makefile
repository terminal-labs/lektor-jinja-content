test:
	@echo "---> running python tests"
	py.test . --tb=long -svv --cov=lektor_jinja_content
	black . --check

coverage: test
	coverage xml
