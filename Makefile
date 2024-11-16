.PHONY: all
all: install

.PHONY: install
install: .venv/.flag

.venv/.flag: poetry.lock
	@ poetry config virtualenvs.in-project true
	poetry install
	@ touch $@

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
	poetry run reload-amazon-balance 5.00 10

.PHONY: test
test: install
	poetry run reload-amazon-balance 5.00 2 --dev

.PHONY: clean
clean:
	rm -rf .venv
