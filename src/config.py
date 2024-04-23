import os

from dotenv import load_dotenv

load_dotenv(".env")

api_url_prefix: str = "/api/v1"


class Config:
    # ENV
    env_name = os.environ.get("ENV_NAME", "development")

    # APIFAIRY
    APIFAIRY_TITLE: str = os.environ.get("FAIRY_TITLE", "Vola PH")
    APIFAIRY_VERSION: str = os.environ.get("FAIRY_VERSION", "1.0")
    APIFAIRY_UI: str = os.environ.get("FAIRY_UI", "swagger_ui")
    APIFAIRY_UI_PATH: str = os.environ.get("FAIRY_UI_PATH", f"{api_url_prefix}/docs")

    # DATABASE
    SQLALCHEMY_DATABASE_URI: str = os.environ.get("DATABASE_URL", "sqlite:///db.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS: str = False

    # SUPABASE
    SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")
    SUPABASE_EMAIL: str = os.environ.get("SUPABASE_EMAIL")
    SUPABASE_PASSWORD: str = os.environ.get("SUPABASE_PASSWORD")
