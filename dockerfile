FROM python:3.10-slim as build
ENV POETRY_VERSION=1.1.14

RUN apt-get -y update && apt-get -y install git

RUN pip install poetry==$POETRY_VERSION
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-dev

WORKDIR /app

COPY ./src ./src
COPY main.py ./

ENV PYTHONPATH=$PYTHONPATH:/app/src
ENTRYPOINT ["poetry", "run", "python", "main.py"]
