import os
import torch
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "5CD-AI/Vietnamese-Sentiment-visobert")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_NEW_TOKENS = 100

# OpenRouter API configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# SQL Server connection string for SQLAlchemy
# Using Windows Authentication
connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=AppBookingTour_Dev;TrustServerCertificate=yes;Trusted_Connection=yes"
CONNECTION_STRING = f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"