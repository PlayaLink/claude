"""
Configuration for Art Exhibits Calendar Sync
"""
import os
from pathlib import Path

# Google Calendar Settings
GOOGLE_EMAIL = "jordan.england.nelson@gmail.com"
CALENDAR_ID = "5b207484d80fb8ae6e9b05aa847850cf15f8dccedb1b4a9695217ba23cd49690@group.calendar.google.com"

# Credentials path (reuse existing Google Workspace MCP credentials)
CREDENTIALS_DIR = Path.home() / ".google_workspace_mcp" / "credentials"
TOKEN_PATH = CREDENTIALS_DIR / f"{GOOGLE_EMAIL}.json"
CREDENTIALS_PATH = Path(__file__).parent / "credentials.json"

# Search Settings
LOCATIONS = ["new-york"]  # Can add more cities: "london", "los-angeles", etc.
NEIGHBORHOODS = ["chelsea", "upper-east-side", "lower-east-side", "tribeca", "soho"]

# Gallery websites to check for exhibition details
GALLERY_DOMAINS = {
    "hauser-wirth": "hauserwirth.com",
    "david-zwirner": "davidzwirner.com",
    "gagosian": "gagosian.com",
    "pace-gallery": "pacegallery.com",
    "jack-shainman": "jackshainman.com",
    "petzel": "petzel.com",
    "gladstone": "gladstonegallery.com",
    "paula-cooper": "paulacoopergallery.com",
    "marian-goodman": "mariangoodman.com",
    "matthew-marks": "matthewmarks.com",
    "lisson": "lissongallery.com",
    "white-cube": "whitecube.com",
}

# Data storage
DATA_DIR = Path(__file__).parent / "data"
EXHIBITIONS_CACHE = DATA_DIR / "exhibitions.json"

# Logging
LOG_DIR = Path(__file__).parent / "logs"
LOG_FILE = LOG_DIR / "sync.log"
