.PHONY: setup run clean vscode-setup run log-run readme install help

setup:
	PIPENV_VENV_IN_PROJECT=1 pipenv install pycoingecko pandas

run:
	pipenv run python main.py $(COIN) --currency=$(CURRENCY) --days=$(DAYS)

clean:
	pipenv --rm

vscode-setup:
	mkdir -p .vscode
	echo '{\n    "python.defaultInterpreterPath": "$${workspaceFolder}/.venv/bin/python",\n    "python.analysis.extraPaths": ["$${workspaceFolder}/.venv/lib/python3.9/site-packages"]\n}' > .vscode/settings.json

# Default parameters
COIN ?= xxx
CURRENCY ?= usd
DAYS ?= 7
DESC ?= "TWAP calculation for $(COIN)"

# Run with logging
log-run:
	pipenv run python main.py $(COIN) --currency=$(CURRENCY) --days=$(DAYS) --log --description="$(DESC)"

# Only regenerate README from existing runs.json
readme:
	pipenv run python utils.py --generate

# Help text
help:
	@echo "Available commands:"
	@echo "  make run COIN=xxx CURRENCY=usd DAYS=7     - Run without logging"
	@echo "  make log-run COIN=xxx DESC='Description'  - Run and log results"
	@echo "  make readme                                   - Regenerate README from runs.json"
	@echo "  make install                                  - Install dependencies"

all: setup vscode-setup run 
