import os
from dotenv import load_dotenv

load_dotenv()


class AppSettings:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")


settings = AppSettings()
