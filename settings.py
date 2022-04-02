from dotenv import load_dotenv
import os

load_dotenv()

prefix = os.getenv("prefix")
token = os.getenv("token")
activity = os.getenv("activity")

unsplash_client_id = os.getenv("unsplash_client_id")