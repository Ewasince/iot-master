FROM python:3.11.6-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.6.1 \
  PYTHONPATH=/app \
  DEPENDENCYGROUP=tg_bot

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

RUN apt-get update && \
    apt-get install libasound-dev portaudio19-dev ffmpeg gcc -y && \
    apt-get clean autoclean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Project initialization:
COPY pyproject.toml .
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --only=$DEPENDENCYGROUP

# Creating folders, and files for a project:
COPY tg_bot /app

CMD python main.py
