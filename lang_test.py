from dotenv import load_dotenv
import os

load_dotenv()

from langchain.chat_models import init_chat_model

model = init_chat_model("claude-sonnet-4.6")

