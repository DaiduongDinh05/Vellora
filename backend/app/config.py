from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class OAuthProviderConfig(BaseModel):
    client_id: str | None = None
    client_secret: str | None = None
    redirect_uri: str | None = None
    scopes: list[str] = Field(default_factory=list)


class OAuthProviders(BaseModel):
    google: OAuthProviderConfig = OAuthProviderConfig(scopes=["openid", "email", "profile"])
    microsoft: OAuthProviderConfig = OAuthProviderConfig(scopes=["openid", "email", "profile"])


class Settings(BaseSettings):
    DATABASE_URL: str
    FERNET_KEY: str | None = None
    JWT_SECRET_KEY: str = Field(
        default="__change_me_in_prod_please_1234567890abcd",
        min_length=32,
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    OAUTH_STATE_TTL_SECONDS: int = 600
    OAUTH_PROVIDERS: OAuthProviders = OAuthProviders()

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_nested_delimiter="__",
    )

settings = Settings()


def get_settings() -> Settings:
    return settings
