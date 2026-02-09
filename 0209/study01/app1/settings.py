from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    kafka_topic : str = "test"
    kafka_server : str = "localhost:9092"
    mariadb_user: str
    mariadb_password: str
    mariadb_host: str
    mariadb_database: str 
    mariadb_port: int

    model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore"
  )

settings = Settings()