from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_name: str = "SchoolRun Shared Backend"
    app_env: str = "development"
    app_version: str = "1.0.0"
    api_v1_prefix: str = "/api"
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    auto_create_tables: bool = True
    sql_echo: bool = False

    cors_allow_origins_raw: str = Field(default="*", alias="CORS_ALLOW_ORIGINS")

    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3306
    mysql_database: str = "schoolrun_shared"
    mysql_user: str = "schoolrun_app"
    mysql_password: str = "change_me"
    mysql_charset: str = "utf8mb4"

    admin_username: str = "admin"
    admin_password: str = "change_me_admin"
    admin_session_secret: str = "change_me_session_secret"

    @property
    def cors_allow_origins(self) -> list[str]:
        if self.cors_allow_origins_raw.strip() == "*":
            return ["*"]
        return [item.strip() for item in self.cors_allow_origins_raw.split(",") if item.strip()]

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
            f"?charset={self.mysql_charset}"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
