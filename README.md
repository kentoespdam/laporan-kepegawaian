# 1. Clone atau buat folder
```shell
mkdir laporan-kepegawaian
cd laporan-kepegawaian
```
# 2. Buat struktur folder
```shell
mkdir -p laporan_kepegawaian/{_config,core,models,routes,services,repositories,utils}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p templates docs scripts logs
```

# 3. Buat file __init__.py di setiap package
```shell
find laporan_kepegawaian tests -type d -exec touch {}/__init__.py \;
```

---

# Environment
```cp env.example .env```

```dotenv
DB_HOST=localhost
DB_PORT=3306
DB_NAME=kepegawaian
DB_USER=root
DB_PASS=

LOKASI='Kantor Pusat PDAM TIRTA SATRIA'
```

---

# Installation
```shell
# Install semua dependencies
uv sync --no-cache --frozen 

# Install tanpa dev dependencies
uv sync --no-cache --frozen --no-dev

# install group dev dependencies
uv sync --group dev

```

# Running App
```shell
# dev 
uv run uvicorn app.main:app --reload --port 8080

# start 
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

#prod 
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```