# 0210

  ## kafka 만들기
```bash
docker run -d  \
  --name kafka \
  -e KAFKA_NODE_ID=1 \
  -e KAFKA_PROCESS_ROLES=broker,controller \ 
  -e KAFKA_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092 \
  -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER \
  -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT \
  -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@kafka:9093 \
  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
  -e KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1 \
  -e KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1 \
  -e KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS=0 \
  -e KAFKA_NUM_PARTITIONS=3 \
  apache/kafka:4.0.1
```
```bash
docker run -d -p 9092:9092 --network my-net --name kafka -e KAFKA_NODE_ID=1 -e KAFKA_PROCESS_ROLES=broker,controller -e KAFKA_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092 -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@kafka:9093 -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 -e KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1 -e KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1 -e KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS=0 -e KAFKA_NUM_PARTITIONS=3 apache/kafka:4.0.1
```

```bash
docker network inspect (네트워크이름)
```
- IP : `172.17.0.2` ***kafka IP***

  ## 1. App1 설정

```bash
uv init .
uv add fastapi --extra standard
uv add kafka-python
```

  ## UV 이미지 생성 `dockerfile`
```bash
FROM python:3.12.9

RUN apt-get update
RUN apt-get upgrade -y
RUN curl -LsSf http://astral.sh/uv/install.sh | sh
RUN pip install uv

WORKDIR /workspace

EXPOSE 8000
```

```bash
docker build -t uv:1
```

  ## App1 Container 생성
```bash
docker run -d -it -p 8001:8000 -v ./app1:/workspace --name app1 uv:1
docker run -d -it --network my-net -p 8001:8000 -v ./app1:/workspace --name app1 uv:1
```
- IP : `172.17.0.3` ***app1 IP***

## Docker Container 접속 하기

```bash
docker exec -it kafka /bin/bash
```

## Kafka 설치 위치
```bash
cd /opt/kafka/bin/
```

## 메시지 확인 
```bash
./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test
```


