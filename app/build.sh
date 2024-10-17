#!/bin/bash

# DockerHub username
DOCKERHUB_USERNAME="alexhkhan"

# FastAPI 이미지 빌드
docker build -f Dockerfile.fastapi -t $DOCKERHUB_USERNAME/fastapi:latest .

# Celery 이미지 빌드
docker build -f Dockerfile.celery -t $DOCKERHUB_USERNAME/celery:latest .

# DockerHub에 로그인 (이미 로그인되어 있다면 생략 가능)
# docker login

# FastAPI 이미지 푸시
docker push $DOCKERHUB_USERNAME/fastapi:latest

# Celery 이미지 푸시
docker push $DOCKERHUB_USERNAME/celery:latest
