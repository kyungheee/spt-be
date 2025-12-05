import os
import base64
from typing import Dict, Any, List
import requests
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("CID")
SPOTIFY_CLIENT_URL = os.getenv("SECRET")

TOKEN_URL = ""
RECOMMEND_URL = ""

