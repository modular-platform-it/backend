FROM python:3.12-slim

ENV POETRY_VERSION=1.8.2

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="$POETRY_HOME/bin:$PATH"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install --no-install-recommends -y curl \
	&& curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION} \
	&& apt-get purge --auto-remove -y curl \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install --no-install-recommends -y build-essential  \
	&& poetry install --no-root --only main \
	&& apt-get purge --auto-remove -y build-essential \
	&& rm -rf /var/lib/apt/lists/*

CMD ["python", "db.py"]
CMD ["uvicorn", "api:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
