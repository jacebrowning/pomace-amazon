.PHONY: all
all: install

.PHONY: install
install: poetry.lock
	poetry install

poetry.lock: pyproject.toml
	poetry update pomace
	@ touch $@

.PHONY: ci
ci: format

.PHONY: format
format: install
	poetry run isort amazon
	poetry run black amazon
ifdef CI
	git diff --exit-code
endif

.PHONY: run
run: install
	poetry run reload-amazon-balance 0.50 10

.PHONY: test
test: install
	poetry run reload-amazon-balance 0.50 1 --dev
