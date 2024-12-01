
LIBRARY = tamal
TESTS = tests

.PHONY: test typecheck coverage lint format pretty check build publish

test: TEST="$(TESTS)"
test:
	poetry run pytest "$(TEST)"

typecheck:
	poetry run mypy "$(LIBRARY)" --strict

coverage:
		poetry run pytest --cov="$(LIBRARY)" "$(TESTS)" --cov-branch

lint:
	poetry run ruff check --fix "$(TESTS)"
	poetry run ruff check --fix "$(LIBRARY)"

format:
	poetry run isort "$(TESTS)"
	poetry run isort "$(LIBRARY)"
	poetry run black "$(TESTS)"
	poetry run black "$(LIBRARY)"

check: lint typecheck coverage

publish: VERSION=$(shell poetry version -s)
publish:
	git add .
	git commit --allow-empty -m "v${VERSION}"
	git tag -a "v${VERSION}" -m "v${VERSION}"
	git push --follow-tags
	poetry publish --build
