from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

caminho_atual = Path(__file__).resolve()

pasta_raiz = caminho_atual.parents[3]

root_env = pasta_raiz / ".env"

class Settings(BaseSettings):
    app_name: str = "SapienEx Track"
    database_url: str

    model_config = SettingsConfigDict(
        env_file=root_env,
        extra="ignore",
    )

settings = Settings()

