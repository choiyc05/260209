from fastapi import FastAPI
from kafka import KafkaConsumer
import threading
import json

kafka_server="kafka:9092"
kafka_topic="test"

app = FastAPI(title="Consumer")

def consumer():
  cs = KafkaConsumer(
    kafka_topic, 
    bootstrap_servers=kafka_server, 
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
  )
  for msg in cs:
    print(msg.value)

@app.on_event("startup")
def startConsumer():
  thread = threading.Thread(target=consumer, daemon=True)
  thread.start()

@app.get("/")
def read_root():
  return {"status": True}