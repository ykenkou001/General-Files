# FROM python:3.8
ARG VARIANT=3.7
# ARG DEPLOY_KEY

FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

ENV PYTHONUNBUFFERED=1

COPY poetry.lock pyproject.toml ./

RUN apt-get update && apt-get -y install git \
    libgl1-mesa-dev \
    poppler-utils \
    poppler-data

# WORKDIR /root/.ssh
# RUN echo $DEPLOY_KEY | base64 --decode > ./id_rsa \
#     && ssh-keyscan github.com >> ./known_hosts \
#     && chmod 600 ./*

RUN pip install poetry
RUN poetry config virtualenvs.create true \
    && poetry config virtualenvs.in-project true \
    # && poetry install --no-dev \
    && poetry install
