from dotenv import load_dotenv
import os

load_dotenv()

URL_PRODUCTION = os.getenv("URL_PRODUCTION")
URL_DEVELOPMENT = os.getenv("URL_DEVELOPMENT")
