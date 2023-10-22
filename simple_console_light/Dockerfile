FROM python:3.11.6-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.6.1 \
  PYTHONPATH=/app \
  DEPENDENCYGROUP=simple_console_light

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

# Project initialization:
COPY pyproject.toml .
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --only=$DEPENDENCYGROUP

# Creating folders, and files for a project:
COPY simple_console_light /app

CMD python main.py