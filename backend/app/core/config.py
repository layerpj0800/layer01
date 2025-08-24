from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  database_url: str
  jwt_secret: str
  access_token_expire_minutes: int = 30
  s3_bucket: str
  iamport_api_key: str
  iamport_api_secret: str
  iamport_webhook_secret: str

  class Config:
    env_file = '.env'


settings = Settings()
