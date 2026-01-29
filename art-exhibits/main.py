#!/usr/bin/env python3
"""
Art Exhibits Calendar Sync - Main Entry Point

This script fetches current art exhibitions from various sources
and syncs them to a Google Calendar.

Usage:
    python main.py              # Full sync (fetch + calendar update)
    python main.py --fetch      # Only fetch exhibitions
    python main.py --sync       # Only sync cached exhibitions to calendar
    python main.py --cleanup    # Remove past events from calendar
"""
import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

# Ensure the script's directory is in the path
sys.path.insert(0, str(Path(__file__).parent))

import config
from fetch_exhibitions import get_exhibitions, load_cached_exhibitions
from calendar_sync import sync_all_exhibitions, delete_past_events

# Set up logging
config.LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description='Sync art exhibitions to Google Calendar'
    )
    parser.add_argument(
        '--fetch',
        action='store_true',
        help='Only fetch exhibitions (no calendar sync)'
    )
    parser.add_argument(
        '--sync',
        action='store_true',
        help='Only sync cached exhibitions to calendar'
    )
    parser.add_argument(
        '--cleanup',
        action='store_true',
        help='Remove past events from calendar'
    )
    parser.add_argument(
        '--days-past',
        type=int,
        default=30,
        help='Days past to keep events (for cleanup, default: 30)'
    )

    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info(f"Art Exhibits Sync - {datetime.now().isoformat()}")
    logger.info("=" * 60)

    try:
        if args.cleanup:
            logger.info("Cleaning up past events...")
            deleted = delete_past_events(args.days_past)
            logger.info(f"Cleanup complete: {deleted} events deleted")
            return

        if args.fetch or (not args.fetch and not args.sync):
            # Fetch exhibitions
            logger.info("Fetching exhibitions...")
            exhibitions = get_exhibitions()
            logger.info(f"Fetched {len(exhibitions)} exhibitions")

        if args.sync or (not args.fetch and not args.sync):
            # Sync to calendar
            logger.info("Syncing to calendar...")
            exhibitions = load_cached_exhibitions()

            if not exhibitions:
                logger.warning("No exhibitions to sync. Run with --fetch first.")
                return

            created, skipped = sync_all_exhibitions(exhibitions)
            logger.info(f"Sync complete: {created} created, {skipped} skipped")

        logger.info("Done!")

    except Exception as e:
        logger.exception(f"Error during sync: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
