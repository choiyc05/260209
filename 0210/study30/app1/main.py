from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import httpx
from settings import settings

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

KAKAO_REST_API_KEY = settings.kakao_rest_api_key
KAKAO_CLIENT_SECRET = settings.kakao_client_secret
KAKAO_REDIRECT_URI = settings.kakao_redirect_uri
KAKAO_AUTHORIZE_URL = settings.kakao_authorize_url
KAKAO_TOKEN_URL = settings.kakao_token_url
KAKAO_USER_INFO_URL = settings.kakao_user_info_url

async def getToken(client, code: str):
  return await client.post(
    KAKAO_TOKEN_URL,
    data={
      "grant_type": "authorization_code",
      "client_id": KAKAO_REST_API_KEY,
      "redirect_uri": KAKAO_REDIRECT_URI,
      "code": code,
      "client_secret": KAKAO_CLIENT_SECRET,
    },
    headers={"Content-Type": "application/x-www-form-urlencoded"}
  )

async def getUserInfo(client, access_token: str):
  return await client.get(
    KAKAO_USER_INFO_URL,
    headers={"Authorization": f"Bearer {access_token}"}
  )

@app.get("/login/kakao")
async def kakaoLogin():
  kakaoAuthUrl = (
    # https://kauth.kakao.com/oauth/authorize?client_id=&redirect_uri=&response_type=code
    f"{KAKAO_AUTHORIZE_URL}?"
    f"client_id={KAKAO_REST_API_KEY}&"
    f"redirect_uri={KAKAO_REDIRECT_URI}&"
    f"response_type=code"
  )
  return RedirectResponse(kakaoAuthUrl)

@app.get("/oauth/callback/kakao")
async def kakaoCallback(code: str):
  print(code)
  async with httpx.AsyncClient() as client:
    tokenResponse = await getToken(client, code)
    tokens = tokenResponse.json()
    token_type = tokens.get("token_type")
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    return {"status": True, "token_type": token_type, "access_token": access_token, "refresh_token": refresh_token}
  return {"status": False}

@app.get("/me")
async def kakaoUserInfo(access_token: str):
  async with httpx.AsyncClient() as client:
    print(access_token)
    userResponse = await getUserInfo(client, access_token)
    userInfo = userResponse.json()
    properties = userInfo.get("properties")
    nickname = properties.get("nickname")
    profile_image = properties.get("profile_image")
    return {"status": True, "nickname":nickname, "profile_image":profile_image}
  return {"status": False}