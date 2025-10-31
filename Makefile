.PHONY: launch

# Default interpreter; override with `make PYTHON=python` if needed.
PYTHON ?= python3

launch:
	$(PYTHON) -m analytics_mcp.server
