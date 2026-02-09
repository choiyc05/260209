from fastapi import FastAPI
from settings import settings
from kafka import KafkaProducer
from pydantic import EmailStr, BaseModel
import json
import redis
from jose import jwt, JWTError
import uuid
from db import findOne, findAll, save

class EmailModel(BaseModel):
    email: EmailStr

client = redis.Redis(
    host="localhost",
    port=6379,
    db=0
  )

SECRET_KEY = "your-extremely-secure-random-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3

app = FastAPI()

pd = KafkaProducer(
    bootstrap_servers=settings.kafka_server,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"))

def set_token(email :str, id :int):
  try:
    iat = datetime.now(timezone.utc) + (timedelta(hours=7))
    exp = iat + (timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    data = {
      "name": email,
      "iss": "EDU", 
      "sub": int(id), 
      "iat": iat,
      "exp": exp
    }
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    id = uuid.uuid4().hex
    
  except JWTError as e:
    print(f"JWT ERROR : {e}")
  return {"status": True}

@app.get("/")
def read_root():
    return {"status":"Producer"}

@app.post("/login")
def producer(model: EmailModel):
  pd.send(settings.kafka_topic, dict(model))
  pd.flush()
  return {"status": True}

@app.post("/code")
def code(id: str):
   print(id)
   result = client.get(id)
   if result:
      client.delete(id)
      return {"status":True}
   return {"status":False}
