import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.environ.get("APP_ID")
APP_HASH = os.environ.get("APP_HASH")
BOT_TOKEN = os.environ.get('BOT_TOKEN')
