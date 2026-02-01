from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field



class Settings(BaseSettings):
    """
    Imports setttings from .env file
    """
    openai_api_key: str = Field(
        ...,
        alias= "OPENAI_API_KEY"
        )
    google_api_key:str = Field(
        ...,
        alias= "GOOGLE_API_KEY"
        )
    model_name: str = Field(
        default="gpt-4o",
        alias="MODEL_NAME"
        )
    azure_openai_endpoint: str | None = Field(
        default = None,
        alias = "AZURE_OPENAI_ENDPOINT"
    )
    debug: bool = Field(default = False, alias = "DEBUG")
    project_name: str = "GenAI Agent"

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra = "ignore"
    )

settings = Settings()