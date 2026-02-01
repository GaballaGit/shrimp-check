
SOURCE_DIR = "src"

.PHONY: run lint

run:
	@echo "Running main"
	@printf '\033[34m%s\033[0m\n' '------------------------------'
	@python3 ${SOURCE_DIR}/main.py 

lint:
	ruff check src --fix
