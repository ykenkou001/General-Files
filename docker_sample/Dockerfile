# 3.7.13-slim-bullseye, 3.7-slim-bullseye, 3.7.13-slim, 3.7-slim
FROM python:3.7.13-slim-bullseye

# github, docker_build_and_push.shにて設定
ARG DEPLOY_KEY

RUN apt-get update && apt-get install -y git
# githubとssh接続するためにopenssh-server, openssh-clientをインストール
# -yは--yesオプション
# RUN apt-get install -y openssh-server \
# && apt-get install -y openssh-clients

COPY ./ ./home/

WORKDIR /root/.ssh

RUN echo $DEPLOY_KEY | base64 --decode > ./id_rsa \
    && ssh-keyscan github.com >> ./known_hosts \
    && chmod 600 ./*

RUN pip install poetry

WORKDIR /home

RUN poetry config virtualenvs.create false \
    # 開発用の依存関係をインストールしない
    && poetry install --no-dev

# CMD ["table_area_detection_analysis.handler"]