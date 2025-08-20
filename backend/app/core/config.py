from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  database_url: str
  jwt_secret: str
  access_token_expire_minutes: int = 30
  cors_origins: str
  s3_bucket: str
  iamport_api_key: str

  class Config:
    env_file = '.env'


settings = Settings()
