import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "chave_secreta")
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@localhost:5432/RP3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
