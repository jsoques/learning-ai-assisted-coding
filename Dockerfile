FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/
COPY alembic.ini .
COPY alembic/ alembic/

RUN pip install --no-cache-dir -e ".[dev]"

EXPOSE 5566

CMD ["uvicorn", "src.framework.main:app", "--host", "0.0.0.0", "--port", "5566"]
