import os
# import torch
from urllib.parse import quote_plus
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    print("Could not load .env file")
    pass

# MODEL_NAME = os.getenv("MODEL_NAME", "5CD-AI/Vietnamese-Sentiment-visobert")
# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_NEW_TOKENS = 100

def _build_sqlalchemy_url_from_odbc(odbc_conn: str) -> str:
    return f"mssql+pyodbc:///?odbc_connect={quote_plus(odbc_conn)}"

_database_url: Optional[str] = os.getenv("DATABASE_URL")
_odbc_conn: Optional[str] = os.getenv("ODBC_CONNECTION_STRING")

if _database_url:
    CONNECTION_STRING = _database_url
elif _odbc_conn:
    CONNECTION_STRING = _build_sqlalchemy_url_from_odbc(_odbc_conn)
else:
    print("Warning: No database connection string provided. Set DATABASE_URL or ODBC_CONNECTION_STRING in environment variables.")
    CONNECTION_STRING = ""
CONNECTION_STRING = ""
print("DATABASE_URL:", _database_url)
print("ODBC_CONNECTION_STRING:", _odbc_conn)