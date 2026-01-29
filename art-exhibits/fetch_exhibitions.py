"""
Fetch art exhibition data from various sources
"""
import json
import re
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Optional
from pathlib import Path

import requests
from bs4 import BeautifulSoup

import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class Exhibition:
    """Represents an art exhibition"""
    title: str
    artist: str
    gallery: str
    location: str
    start_date: str  # ISO format YYYY-MM-DD
    end_date: str    # ISO format YYYY-MM-DD
    description: str
    artist_bio: str
    exhibition_url: str
    artist_url: str
    galleriesnow_url: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


def search_exhibitions_via_web(query: str) -> list[dict]:
    """
    Search for exhibitions using web search.
    Returns raw search results.
    """
    # Using DuckDuckGo HTML search (no API key needed)
    url = "https://html.duckduckgo.com/html/"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

    try:
        response = requests.post(url, data=params, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        results = []

        for result in soup.select('.result'):
            title_elem = result.select_one('.result__title')
            snippet_elem = result.select_one('.result__snippet')
            url_elem = result.select_one('.result__url')

            if title_elem and url_elem:
                results.append({
                    'title': title_elem.get_text(strip=True),
                    'snippet': snippet_elem.get_text(strip=True) if snippet_elem else '',
                    'url': url_elem.get_text(strip=True)
                })

        return results
    except Exception as e:
        logger.error(f"Search failed for query '{query}': {e}")
        return []


def fetch_gallery_exhibitions(gallery_url: str) -> list[dict]:
    """
    Fetch current exhibitions from a gallery's website.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

    try:
        response = requests.get(gallery_url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Generic extraction - galleries have different structures
        # This is a starting point that can be customized per gallery
        exhibitions = []

        # Look for common exhibition patterns
        for article in soup.find_all(['article', 'div'], class_=re.compile(r'exhibition|show|event', re.I)):
            title = article.find(['h1', 'h2', 'h3', 'h4'])
            if title:
                exhibitions.append({
                    'title': title.get_text(strip=True),
                    'html': str(article)[:500]
                })

        return exhibitions
    except Exception as e:
        logger.error(f"Failed to fetch {gallery_url}: {e}")
        return []


def parse_date_range(date_str: str) -> tuple[Optional[str], Optional[str]]:
    """
    Parse exhibition date strings like "January 15 - April 4, 2026"
    Returns (start_date, end_date) in ISO format
    """
    # Common patterns
    patterns = [
        # "January 15 - April 4, 2026"
        r'(\w+ \d+)\s*[-–]\s*(\w+ \d+),?\s*(\d{4})',
        # "15 Jan - 4 Apr 2026"
        r'(\d+ \w+)\s*[-–]\s*(\d+ \w+)\s*(\d{4})',
        # "Jan 15, 2026 - Apr 4, 2026"
        r'(\w+ \d+),?\s*(\d{4})\s*[-–]\s*(\w+ \d+),?\s*(\d{4})',
    ]

    months = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12,
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
        'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }

    date_str_lower = date_str.lower()

    for pattern in patterns:
        match = re.search(pattern, date_str_lower)
        if match:
            groups = match.groups()
            try:
                if len(groups) == 3:
                    # Pattern 1 or 2
                    start_str, end_str, year = groups
                    year = int(year)

                    # Parse start date
                    for month_name, month_num in months.items():
                        if month_name in start_str:
                            day = int(re.search(r'\d+', start_str).group())
                            start_date = f"{year}-{month_num:02d}-{day:02d}"
                            break

                    # Parse end date
                    for month_name, month_num in months.items():
                        if month_name in end_str:
                            day = int(re.search(r'\d+', end_str).group())
                            end_date = f"{year}-{month_num:02d}-{day:02d}"
                            break

                    return start_date, end_date

            except Exception as e:
                logger.warning(f"Failed to parse date '{date_str}': {e}")
                continue

    return None, None


def fetch_galleriesnow_listings() -> list[Exhibition]:
    """
    Fetch exhibition listings from GalleriesNow.
    Note: The site uses JavaScript, so we search for specific exhibitions.
    """
    exhibitions = []
    current_year = datetime.now().year

    for location in config.LOCATIONS:
        for neighborhood in config.NEIGHBORHOODS:
            query = f"site:galleriesnow.net {location} {neighborhood} art exhibition {current_year}"
            results = search_exhibitions_via_web(query)

            for result in results:
                # Extract exhibition info from search results
                if 'galleriesnow.net/shows/' in result.get('url', ''):
                    logger.info(f"Found exhibition: {result['title']}")
                    # Would need to fetch individual pages for full details

    return exhibitions


def fetch_from_gallery_websites() -> list[Exhibition]:
    """
    Fetch exhibitions directly from major gallery websites.
    """
    exhibitions = []

    gallery_exhibition_urls = {
        "Hauser & Wirth": "https://www.hauserwirth.com/hauser-wirth-exhibitions/",
        "David Zwirner": "https://www.davidzwirner.com/exhibitions",
        "Gagosian": "https://gagosian.com/exhibitions/",
        "Pace Gallery": "https://www.pacegallery.com/exhibitions/",
    }

    for gallery, url in gallery_exhibition_urls.items():
        logger.info(f"Fetching exhibitions from {gallery}...")
        raw_exhibitions = fetch_gallery_exhibitions(url)

        for raw in raw_exhibitions:
            logger.info(f"  Found: {raw.get('title', 'Unknown')}")

    return exhibitions


def load_cached_exhibitions() -> list[Exhibition]:
    """Load exhibitions from cache file"""
    if config.EXHIBITIONS_CACHE.exists():
        try:
            with open(config.EXHIBITIONS_CACHE) as f:
                data = json.load(f)
                return [Exhibition.from_dict(e) for e in data]
        except Exception as e:
            logger.error(f"Failed to load cache: {e}")
    return []


def save_exhibitions_cache(exhibitions: list[Exhibition]):
    """Save exhibitions to cache file"""
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(config.EXHIBITIONS_CACHE, 'w') as f:
        json.dump([e.to_dict() for e in exhibitions], f, indent=2)

    logger.info(f"Saved {len(exhibitions)} exhibitions to cache")


def get_exhibitions() -> list[Exhibition]:
    """
    Main function to get all current exhibitions.
    Combines multiple sources.
    """
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("Fetching exhibition listings...")

    all_exhibitions = []

    # Try GalleriesNow
    gn_exhibitions = fetch_galleriesnow_listings()
    all_exhibitions.extend(gn_exhibitions)

    # Try gallery websites directly
    gallery_exhibitions = fetch_from_gallery_websites()
    all_exhibitions.extend(gallery_exhibitions)

    # Deduplicate by title + gallery
    seen = set()
    unique = []
    for ex in all_exhibitions:
        key = (ex.title.lower(), ex.gallery.lower())
        if key not in seen:
            seen.add(key)
            unique.append(ex)

    logger.info(f"Found {len(unique)} unique exhibitions")

    # Cache results
    if unique:
        save_exhibitions_cache(unique)

    return unique


if __name__ == "__main__":
    exhibitions = get_exhibitions()
    for ex in exhibitions:
        print(f"- {ex.title} by {ex.artist} at {ex.gallery}")
        print(f"  {ex.start_date} - {ex.end_date}")
        print()
