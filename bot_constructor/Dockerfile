FROM python:3.12-slim-bullseye

ENV POETRY_VERSION=1.8.2
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION}

WORKDIR /app

COPY ../pyproject.toml ../poetry.lock ./
RUN poetry install --no-root --only main

COPY */ /
RUN poetry install --only main

ENTRYPOINT ["mycli"]
