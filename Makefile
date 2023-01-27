PYTHONPATH=./

deps:  ## Install dependencies
	poetry install

lint:  ## Lint and static-check
	flake8 --jobs 8 --statistics --show-source --max-line-length 120
	pylint --jobs 8 $(PYTHONPATH)
	mypy $(PYTHONPATH)

format:  ## Format code
	autoflake --recursive --in-place $(PYTHONPATH)
	black --target-version py311 --skip-string-normalization $(PYTHONPATH)
	isort --apply --recursive $(PYTHONPATH)
	unify --in-place --recursive --quote='"' $(PYTHONPATH)

push:  ## Push code with tags
	git push && git push --tags

run:  ## Run bot
	poetry run python3 main.py

help: ## Show help message
	@IFS=$$'\n' ; \
	help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##/:/'`); \
	printf "%s\n\n" "Usage: make [task]"; \
	printf "%-20s %s\n" "task" "help" ; \
	printf "%-20s %s\n" "------" "----" ; \
	for help_line in $${help_lines[@]}; do \
		IFS=$$':' ; \
		help_split=($$help_line) ; \
		help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		printf '\033[36m'; \
		printf "%-20s %s" $$help_command ; \
		printf '\033[0m'; \
		printf "%s\n" $$help_info; \
	done