FROM python:3.8-alpine

RUN apk update && \
    apk add make \
            curl \
            gcc \
            musl-dev

# Setup Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.2.0 python3
ENV PATH ${PATH}:/root/.local/bin
RUN poetry config virtualenvs.create false

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Add all code
COPY ./ .

# Install deps
RUN poetry install -E all

EXPOSE 5001

ENTRYPOINT [ "make", "docs-serve" ]
