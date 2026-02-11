from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from pathlib import Path
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import shutil
import uuid
from settings import settings
from db import findOne, findAll, save, add_key

class FileItem(BaseModel):
  filename: str
  content_type: str
  content_base64: str

class FileModel(BaseModel):
  txt: str
  files: List[str]

origins = [ "http://localhost", "http://app2", "http://app2:5173" ]

app = FastAPI(title="FileUpload")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_FILE_SIZE = 10 * 1024

db = []

def checkDir():
  UPLOAD_DIR.mkdir(exist_ok=True)

def saveFile(file):
  print(file.filename, file.size, file.content_type)
  checkDir()    # 최초 파일 저장될 위치 생성
  origin = file.filename
  ext = origin.split(".")[-1].lower()
  id = uuid.uuid4().hex
  newName = f"{uuid.uuid4().hex}.{ext}"
  # data = { "id": id, "origin": origin, "ext": ext, "newName": newName }
  # db.append(data)
  sql = f"""
    insert into edu.`file` (`origin`, `ext`, `fileName`, `contentType`)
    value ('{origin}', '{ext}', '{newName}', '{file.content_type}')
    """
  result = add_key(sql)
  if result[0]:
    path = UPLOAD_DIR / newName
    with path.open("wb") as f:
      shutil.copyfileobj(file.file, f) # file.file(원본)을 f에 복제
    return result[1]
  return 0    

@app.get("/")
def root():
  return {"status": True}

@app.post("/upload")
def upload(files: List[UploadFile] = File(None), txt: str = Form(None)):
  print(txt)
  arr = []
  for file in files:
    arr.append(saveFile(file))
  return {"status": True, "result": arr}

@app.post("/upload2")
def upload(model: FileModel):
  print(model)
  return {"status": True}

@app.get("/images")
def images():
  return {"status": True, "result": db}

@app.get("/download")
def download(id: str):
#   for row in db:
#     if row["id"] == id:
#         newName = row["newName"]
#         origin = row["origin"]
#         break
  sql = f"select `origin`, `fileName` from edu.`file` where 'no' = {id}"
  result = findOne(sql)
  if result:
    print(result)
    origin = result["origin"]
    newName = result["fileName"]
    path = UPLOAD_DIR / newName
    return FileResponse(path=path, filename=origin) # filename=origin 추가하면 업로드한 이름 그대로 다운로드 가능
  return {"status": False}