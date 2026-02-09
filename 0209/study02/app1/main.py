from fastapi import FastAPI, Depends, HTTPException, status
from kafka import KafkaProducer
from settings import settings
from pydantic import EmailStr, BaseModel
import json
import redis
import uuid
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from db import findOne
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from logger import log
from fastapi.middleware.cors import CORSMiddleware

origins = [ settings.react_url, "http://localhost:80", "http://192.168.0.235", "http://192.168.0.235:80" ]

security = HTTPBearer() # docs 페이지 상단에 표시됨(Authorize)

class EmailModel(BaseModel):
  email: EmailStr

class CodeModel(BaseModel):
  id: str

def set_token(email: str):
  try:
    sql = f"select `no`, `name` from test.user where `email` = '{email}'"
    data = findOne(sql)
    if data:
      iat = datetime.now(timezone.utc)
      exp = iat + (timedelta(minutes=settings.access_token_expire_minutes))
      data = {
        "name": data["name"],
        "iss": "EDU",
        "sub": str(data["no"]),
        "iat": iat,
        "exp": exp
      }
      return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)
  except JWTError as e:
    print(f"JWT ERROR : {e}")
  return None

def get_payload(credentials: HTTPAuthorizationCredentials = Depends(security)):
  log().info(credentials)              # HTTPAuthorizationCredentials
  log().info(credentials.scheme)       # Bearer
  log().info(credentials.credentials)  # token
  if credentials.scheme == "Bearer":
    try:
      payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=settings.algorithm)
      exp = payload.get("exp")

      if datetime.now(timezone.utc).timestamp() > exp:
        log().info("Token 유효 시간이 지났습니다.")
      else:
        now = datetime.now(timezone.utc).timestamp()
        minutes, remaining_seconds = divmod(int(exp - now), 60)
        log().info(f"Token 유효 시간 : {minutes} 분 {remaining_seconds} 초")
      return payload
    except ExpiredSignatureError as e:
      log().info(f"JWT EXPIRED : {e}")
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token expired",
      )
    except JWTError as e:
      log().info(f"JWT ERROR : {e}")
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
      )
  return None

app = FastAPI(title="Producer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pd = KafkaProducer(
  bootstrap_servers=settings.kafka_server,
  value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

client = redis.Redis(
  host=settings.redis_host,
  port=settings.redis_port,
  db=settings.redis_db,
  decode_responses=True
)

@app.get("/")
def root():
  return {"msg": "Producer"}

@app.post("/login")
def producer(model: EmailModel):
  pd.send(settings.kafka_topic, dict(model))
  pd.flush()
  return {"status": True}

@app.post("/code")
def code(codemodel: CodeModel):
  print(codemodel.id)
  result = client.get(codemodel.id)
  if result:
    access_token = set_token(result)
    if access_token:
      client.delete(codemodel.id)
      return {"status": True, "access_token": access_token}
  return {"status": False}

@app.post("/me")
def me(payload = Depends(get_payload)):
  if payload:
    return {"status": True, "name": payload["name"]}
  return {"status": False}
