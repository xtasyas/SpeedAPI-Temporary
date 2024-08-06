from pprint import pprint

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        encoding='UTF-8',
    )
    DATABASE_URL: str


settings = Settings()
DATABASE_URL = settings.DATABASE_URL


if __name__ == '__main__':
    print('Settings from .env file: \n')
    pprint(settings.model_dump())
