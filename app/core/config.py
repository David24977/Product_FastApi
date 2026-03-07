from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    app_env: str

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    ai_api_key: str
    ai_base_url: str
    ai_model: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
