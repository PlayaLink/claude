"""
Sync exhibitions to Google Calendar
"""
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import config
from fetch_exhibitions import Exhibition, load_cached_exhibitions

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_credentials():
    """Get or refresh Google Calendar credentials"""
    creds = None

    # Check for existing token (reuse MCP credentials)
    if config.TOKEN_PATH.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(config.TOKEN_PATH), SCOPES)
            logger.info(f"Loaded credentials from {config.TOKEN_PATH}")
        except Exception as e:
            logger.warning(f"Failed to load existing credentials: {e}")

    # Refresh if expired
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            logger.info("Refreshed expired credentials")
            # Save refreshed token
            with open(config.TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())
        except Exception as e:
            logger.error(f"Failed to refresh credentials: {e}")
            creds = None

    # If no valid credentials, need to authenticate
    if not creds or not creds.valid:
        if not config.CREDENTIALS_PATH.exists():
            raise FileNotFoundError(
                f"No valid credentials found.\n"
                f"Expected token at: {config.TOKEN_PATH}\n"
                f"Or credentials.json at: {config.CREDENTIALS_PATH}\n\n"
                "Options:\n"
                "1. Run the Google Workspace MCP to authenticate first\n"
                "2. Download OAuth credentials from Google Cloud Console"
            )

        flow = InstalledAppFlow.from_client_secrets_file(
            str(config.CREDENTIALS_PATH), SCOPES
        )
        creds = flow.run_local_server(port=0)

        # Save the credentials
        config.CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
        with open(config.TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return creds


def get_calendar_service():
    """Build and return the Google Calendar service"""
    creds = get_credentials()
    return build('calendar', 'v3', credentials=creds)


def get_existing_events(service, time_min: str, time_max: str) -> dict[str, dict]:
    """
    Get existing events from the calendar.
    Returns dict keyed by event summary for deduplication.
    """
    try:
        events_result = service.events().list(
            calendarId=config.CALENDAR_ID,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=100,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        return {e['summary']: e for e in events}

    except HttpError as e:
        logger.error(f"Failed to fetch existing events: {e}")
        return {}


def create_event_body(exhibition: Exhibition) -> dict:
    """Create a Google Calendar event body from an Exhibition"""

    description = f"""EXHIBITION: {exhibition.title}

ARTIST: {exhibition.artist}

ABOUT THE EXHIBITION:
{exhibition.description}

ABOUT THE ARTIST:
{exhibition.artist_bio}

LINKS:
Exhibition: {exhibition.exhibition_url}
Artist: {exhibition.artist_url}
GalleriesNow: {exhibition.galleriesnow_url}
"""

    # For all-day events, end date should be the day after
    end_date = datetime.fromisoformat(exhibition.end_date) + timedelta(days=1)

    return {
        'summary': f"{exhibition.artist}: {exhibition.title}",
        'location': exhibition.location,
        'description': description,
        'start': {
            'date': exhibition.start_date,
            'timeZone': 'America/New_York',
        },
        'end': {
            'date': end_date.strftime('%Y-%m-%d'),
            'timeZone': 'America/New_York',
        },
        'transparency': 'transparent',  # Show as "free"
    }


def sync_exhibition_to_calendar(service, exhibition: Exhibition, existing_events: dict) -> bool:
    """
    Sync a single exhibition to Google Calendar.
    Returns True if created/updated, False if skipped.
    """
    event_title = f"{exhibition.artist}: {exhibition.title}"

    # Check if event already exists
    if event_title in existing_events:
        logger.info(f"Event already exists: {event_title}")
        return False

    try:
        event_body = create_event_body(exhibition)

        event = service.events().insert(
            calendarId=config.CALENDAR_ID,
            body=event_body
        ).execute()

        logger.info(f"Created event: {event_title}")
        return True

    except HttpError as e:
        logger.error(f"Failed to create event '{event_title}': {e}")
        return False


def sync_all_exhibitions(exhibitions: list[Exhibition]) -> tuple[int, int]:
    """
    Sync all exhibitions to Google Calendar.
    Returns (created_count, skipped_count)
    """
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger.info(f"Starting sync of {len(exhibitions)} exhibitions...")

    service = get_calendar_service()

    # Get date range for checking existing events
    today = datetime.now()
    time_min = today.strftime('%Y-%m-%dT00:00:00Z')
    time_max = (today + timedelta(days=365)).strftime('%Y-%m-%dT00:00:00Z')

    existing = get_existing_events(service, time_min, time_max)
    logger.info(f"Found {len(existing)} existing events in calendar")

    created = 0
    skipped = 0

    for exhibition in exhibitions:
        if sync_exhibition_to_calendar(service, exhibition, existing):
            created += 1
        else:
            skipped += 1

    logger.info(f"Sync complete: {created} created, {skipped} skipped")
    return created, skipped


def delete_past_events(days_past: int = 30):
    """Delete events that ended more than N days ago"""
    service = get_calendar_service()

    cutoff = datetime.now() - timedelta(days=days_past)
    time_min = (cutoff - timedelta(days=365)).strftime('%Y-%m-%dT00:00:00Z')
    time_max = cutoff.strftime('%Y-%m-%dT00:00:00Z')

    existing = get_existing_events(service, time_min, time_max)

    deleted = 0
    for event in existing.values():
        try:
            service.events().delete(
                calendarId=config.CALENDAR_ID,
                eventId=event['id']
            ).execute()
            deleted += 1
            logger.info(f"Deleted past event: {event['summary']}")
        except HttpError as e:
            logger.error(f"Failed to delete event: {e}")

    logger.info(f"Deleted {deleted} past events")
    return deleted


if __name__ == "__main__":
    # Test the calendar sync
    exhibitions = load_cached_exhibitions()
    if exhibitions:
        created, skipped = sync_all_exhibitions(exhibitions)
        print(f"Created: {created}, Skipped: {skipped}")
    else:
        print("No cached exhibitions found. Run fetch_exhibitions.py first.")
