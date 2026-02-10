from fastapi import FastAPI
from kafka import KafkaProducer
import json

app = FastAPI(title="Producer")

kafka_server="kafka:9092"
kafka_topic="test"

pd = KafkaProducer(
    bootstrap_servers=kafka_server,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

@app.get("/")
def read_root():
    return {"msg":"Producer"}

@app.post("/msg")
def producer(msg: str):
  pd.send(kafka_topic, {"msg":msg})
  pd.flush()
  return {"status": True}