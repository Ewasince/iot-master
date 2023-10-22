FROM python:3.11

ENV PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.6.1 \
  PYTHONPATH=/app \
  DEPENDENCY_GROUP=tg_bot

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

# Project initialization:
COPY ../simple_console_light/pyproject.toml .
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi --only=$DEPENDENCY_GROUP

# Creating folders, and files for a project:
COPY ./tg_bot /app

CMD python main.py