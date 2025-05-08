# FROM python:3.14.0a5-slim-bookworm AS base
# WORKDIR /app

# # Install dependencies
# FROM base AS builder
# WORKDIR /app
# RUN apt update && apt install pkg-config build-essential -y
# RUN python -m venv .venv
# ENV PATH=".venv/bin:$PATH"
# COPY requirement.txt .
# RUN pip install -r requirement.txt
# # RUN "fastapi[standard]" openpyxl pymysql pymysql-pool pandas python-dotenv icecream swifter icecream jinja2 

# # run app
# FROM base AS runner
# WORKDIR /app
# COPY --from=builder /app/.venv .venv
# COPY . .
# ENV PATH=".venv/bin:$PATH"
# CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "80"]


FROM python:3.12.3-slim-bookworm
WORKDIR /app
COPY . .
ENV PATH=".venv/bin:$PATH"
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "80"]