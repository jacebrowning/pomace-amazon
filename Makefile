.PHONY: all
all: install

.PHONY: install
install: poetry.lock
	poetry install

poetry.lock: pyproject.toml
	poetry lock --no-update
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
