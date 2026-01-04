import os
from dotenv import load_dotenv

load_dotenv(".env.prod")


class Config:
    PORT = int(os.getenv("PORT", 4000))
    TOKEN = os.getenv("TOKEN", None)
    API_LOGIN = os.getenv("API_LOGIN", None)
    API_POST_GAME = os.getenv("API_POST_GAME", None)
    API_EMAIL = os.getenv("API_EMAIL", None)
    API_PASSWORD = os.getenv("API_PASSWORD", None)
    URL_PARSER = os.getenv("URL_PARSER")
    URL_PARSER_SWITCH_2 = os.getenv("URL_PARSER_SWITCH_2", None)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


environments = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

CONFIG = environments[os.getenv("environment")]
