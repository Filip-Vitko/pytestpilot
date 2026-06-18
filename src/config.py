import os 

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
MODEL_NAME = os.getenv("MODEL_NAME", "gwen2.5-coder")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
API_KEY = os.getenv("API_KEY", "")