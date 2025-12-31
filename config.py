import os
from dotenv import load_dotenv

load_dotenv(".env.dev")

env = os.getenv("environment")

if env == "production":
	load_dotenv(".env.prod", override=True)

class Config:
	PORT = int(os.getenv("PORT", 4000))
	API_URL = os.getenv("API_URL")
	API_EMAIL = os.getenv("API_EMAIL")
	API_PASSWORD = os.getenv("API_PASSWORD")

class DevelopmentConfig(Config):
	DEBUG = True
	
class ProductionConfig(Config):
	DEBUG = False
	
environments = {
	"development": DevelopmentConfig,
	"production": ProductionConfig,
}

CONFIG = environments[os.getenv("environment")]

