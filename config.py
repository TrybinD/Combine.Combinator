import os


SYNC_CONNECTION_STRING = os.environ.get("SYNC_CONNECTION_STRING", "sqlite:///data/sqlite.db")
BOT_URL = os.environ.get("COMBINATOR_URL", "http://127.0.0.1:8000")
