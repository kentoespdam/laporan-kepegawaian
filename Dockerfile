FROM python:3.14.0a5-slim-bookworm AS base
WORKDIR /app

# Install dependencies
FROM base AS builder
WORKDIR /app
RUN apt update && apt install pkg-config build-essential -y
RUN python3 -m venv .venv
ENV PATH=".venv/bin:$PATH"
RUN pip install "fastapi[standard]" openpyxl pymysql pymysql-pool pandas python-dotenv icecream swifter icecream jinja2 

# run app
FROM base AS runner
WORKDIR /app
COPY --from=builder /app/.venv .venv
COPY . .
ENV PATH=".venv/bin:$PATH"
CMD ["fastapi", "run", "main.py", "--port", "80"]