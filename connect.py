import os


from dotenv import load_dotenv

load_dotenv()

db = os.getenv('MONGO_DB')
host = os.getenv('MONGO_URL')
bs4_url = os.getenv('BS4_MAIN_URL')

