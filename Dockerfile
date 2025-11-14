FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    ANALYTICS_MCP_ALLOW_ADC=false

WORKDIR /app

COPY pyproject.toml README.md ./
COPY analytics_mcp analytics_mcp

RUN pip install --upgrade pip && \
    pip install .

EXPOSE 8000

ENTRYPOINT ["python", "-m", "analytics_mcp.server"]
