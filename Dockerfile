FROM ghcr.io/astral-sh/uv:debian-slim
WORKDIR /app

COPY . .
RUN uv sync --no-cache --frozen --no-dev

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]