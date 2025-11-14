.PHONY: launch launch-local docker-build docker-run codex-config

PYTHON ?= python3
DOCKER_IMAGE ?= analytics-mcp:latest
DOCKER_BUILD_CONTEXT ?= .
DOCKER_RUN_FLAGS ?=
CODEX ?= codex
MCP_SERVER_NAME ?= analytics-ga

launch: docker-build codex-config docker-run

docker-build:
	docker build --pull --tag $(DOCKER_IMAGE) $(DOCKER_BUILD_CONTEXT)

docker-run:
	docker run --rm -it $(DOCKER_RUN_FLAGS) $(DOCKER_IMAGE)

codex-config:
	@if command -v $(CODEX) >/dev/null 2>&1; then \
		echo "Configuring Codex MCP server '$(MCP_SERVER_NAME)'..."; \
		$(CODEX) mcp remove $(MCP_SERVER_NAME) >/dev/null 2>&1 || true; \
		$(CODEX) mcp add $(MCP_SERVER_NAME) -- docker run --rm -i $(DOCKER_RUN_FLAGS) $(DOCKER_IMAGE); \
	else \
		echo "Codex CLI '$(CODEX)' not found. Skipping Codex configuration."; \
	fi

launch-local:
	$(PYTHON) -m analytics_mcp.server
