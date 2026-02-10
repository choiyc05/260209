from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  kakao_rest_api_key: str
  kakao_client_secret: str
  kakao_redirect_uri: str
  kakao_authorize_url: str
  kakao_token_url: str
  kakao_user_info_url: str

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore"
  )

settings = Settings()
