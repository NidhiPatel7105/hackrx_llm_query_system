# app/config.py
import os

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "your-pinecone-key")
PINECONE_ENV = os.getenv("PINECONE_ENV", "your-pinecone-env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key")
AUTHORIZED_TOKEN = os.getenv("AUTH_TOKEN", "c61acf6dfe00a39f662ac0e4c9dbebf0700f169710c2e07dd95e56636418ab65")
