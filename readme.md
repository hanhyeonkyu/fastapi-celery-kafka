# FASTAPI-CELERY-KAFKA with k8s

## Contents
- [FASTAPI-CELERY-KAFKA with k8s](#fastapi-celery-kafka-with-k8s)
  - [Contents](#contents)
  - [Overview](#overview)
  - [Flow](#flow)
  - [Make Cluster](#make-cluster)
  - [Make FastAPI App](#make-fastapi-app)
    - [Configure All Infra \& App](#configure-all-infra--app)
  - [Confirmation](#confirmation)
    - [Kafka](#kafka)
    - [Redis](#redis)


## Overview

앱은 FastAPI를 통해 HTTP 요청을 받아서, Celery를 통해 백그라운드 작업을 처리하며, Kafka는 메시지 브로커로 사용됩니다. Celery는 Kafka를 이용해 작업 큐를 처리하고, Kubernetes는 전체 애플리케이션을 컨테이너로 관리합니다.

- Python: 주 언어
- FastAPI: API 서버
- Celery: 백그라운드 작업 처리
- Kafka: 메시지 브로커
- Redis/Database: Celery의 백엔드 (결과 저장소)
- Kubernetes: 컨테이너 관리
- Docker: 컨테이너화

## Flow

- FastAPI 엔드포인트 호출: /process 엔드포인트를 호출하여 Celery 작업을 트리거합니다.
- Kafka 메시지 전송: Celery는 Kafka에 메시지를 보내고, 이 메시지는 default 토픽에 저장됩니다.
- Kafka Consumer: Kafka Consumer를 통해 이 메시지를 확인합니다.
- Celery 작업 실행: Celery Worker가 Kafka 메시지를 소비하여 작업을 처리합니다.
- 작업 결과 저장: Celery는 작업 결과를 Redis에 저장합니다.
- Redis 결과 확인: Redis CLI 또는 GUI 도구를 통해 작업 결과를 확인합니다.

## Make Cluster

`kind create cluster -n local-cluster`

## Make FastAPI App

- See the main.py file.

### Configure All Infra & App

Just run `make apply`

## Confirmation

1. Port-forwarding with script: `kubectl port-forward svc/fastapi-service 8000:8000` for access easily.
2. Request GET/POST with curl

### Kafka

1. Check kafka pod name `kubectl get pods`
2. Message check with kafka-cli `kubectl exec -it <kafka_pod_name> -- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic default --from-beginning`

### Redis

1. Check redis pod name `kubectl get pods`
2. Check redis-cli `kubectl exec -it <redis_pod_name> -- redis-cli`