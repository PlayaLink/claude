#!/usr/bin/env python3
"""
Manual exhibition entry script.

Use this to add exhibitions that couldn't be automatically fetched.
Exhibitions are saved to the cache and can be synced with main.py --sync
"""
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

import config
from fetch_exhibitions import Exhibition, load_cached_exhibitions, save_exhibitions_cache


# ============================================================================
# ADD YOUR EXHIBITIONS HERE
# ============================================================================

MANUAL_EXHIBITIONS = [
    Exhibition(
        title="Late at night, early in the morning, at noon",
        artist="Glenn Ligon",
        gallery="Hauser & Wirth",
        location="Hauser & Wirth, 443 West 18th Street, New York, NY",
        start_date="2026-01-15",
        end_date="2026-04-04",
        description="A two-part exhibition of new and historic works on paper. This presentation extends the artist's longstanding engagement with language and abstraction through richly layered compositions that meditate on the color blue and its emotional, historical and cultural inflections.",
        artist_bio="Glenn Ligon has pursued an incisive exploration of American history, literature and society. In 2011, the Whitney Museum held a mid-career retrospective, 'Glenn Ligon: AMERICA.'",
        exhibition_url="https://www.hauserwirth.com/hauser-wirth-exhibitions/glenn-ligon-late-at-night-early-in-the-morning-at-noon/",
        artist_url="https://www.hauserwirth.com/artists/24240-glenn-ligon/",
        galleriesnow_url="https://www.galleriesnow.net/gallery/hauser-wirth/",
    ),
    Exhibition(
        title="Feedback Loop",
        artist="Alexis Rockman",
        gallery="Jack Shainman Gallery",
        location="Jack Shainman Gallery, 513 West 20th Street, New York, NY",
        start_date="2026-01-15",
        end_date="2026-02-28",
        description="Rockman's first solo presentation with Jack Shainman Gallery. The exhibition highlights humanity's fragile relationship to the natural world through Forest Fire paintings and watercolors.",
        artist_bio="Alexis Rockman is known for large-scale paintings depicting ecological and environmental themes.",
        exhibition_url="https://jackshainman.com/exhibitions/alexis_rockman_feedback_loop",
        artist_url="https://www.alexisrockman.net/",
        galleriesnow_url="https://www.galleriesnow.net/gallery/jack-shainman-gallery/",
    ),
    Exhibition(
        title="Grids",
        artist="Dan Flavin",
        gallery="David Zwirner",
        location="David Zwirner, 525 West 19th Street, New York, NY",
        start_date="2026-01-15",
        end_date="2026-02-21",
        description="Works by the pioneering Minimalist artist Dan Flavin, focusing on his grid-based light installations.",
        artist_bio="Dan Flavin (1933-1996) was an American minimalist artist famous for creating sculptural objects from commercially available fluorescent light fixtures.",
        exhibition_url="https://www.davidzwirner.com/exhibitions/dan-flavin-grids",
        artist_url="https://www.davidzwirner.com/artists/dan-flavin",
        galleriesnow_url="https://www.galleriesnow.net/gallery/david-zwirner/",
    ),
    Exhibition(
        title="Solo Exhibition (Swimmers and Surfers)",
        artist="Gideon Appah",
        gallery="Pace Gallery",
        location="Pace Gallery, 540 West 25th Street, New York, NY",
        start_date="2026-01-16",
        end_date="2026-02-28",
        description="Gideon Appah's first solo show with Pace in New York, focusing on his 'Swimmers and Surfers' series.",
        artist_bio="Gideon Appah is a Ghanaian contemporary artist known for vibrant, large-scale paintings exploring themes of leisure, identity, and the human figure.",
        exhibition_url="https://www.pacegallery.com/exhibitions/gideon-appah-new-york/",
        artist_url="https://www.pacegallery.com/artists/gideon-appah/",
        galleriesnow_url="https://www.galleriesnow.net/gallery/pace-gallery/",
    ),
    Exhibition(
        title="Delayed Gravity",
        artist="Wang Guangle",
        gallery="Pace Gallery",
        location="Pace Gallery, 540 West 25th Street, New York, NY",
        start_date="2026-01-16",
        end_date="2026-02-28",
        description="New works by Chinese contemporary artist Wang Guangle, known for his meditative approach to painting.",
        artist_bio="Wang Guangle (b. 1976) is a Beijing-based artist known for methodical, labor-intensive paintings that explore concepts of time and accumulation.",
        exhibition_url="https://www.pacegallery.com/exhibitions/wang-guangle-delayed-gravity/",
        artist_url="https://www.pacegallery.com/artists/wang-guangle/",
        galleriesnow_url="https://www.galleriesnow.net/gallery/pace-gallery/",
    ),
    Exhibition(
        title="A Moment in Time: Plaster Surrogates, 1991-1993",
        artist="Allan McCollum",
        gallery="Petzel Gallery",
        location="Petzel Gallery, 456 West 18th Street, New York, NY",
        start_date="2026-01-15",
        end_date="2026-02-28",
        description="Allan McCollum's iconic Plaster Surrogates, exploring mass production, uniqueness, and the nature of art objects.",
        artist_bio="Allan McCollum (b. 1944) is a conceptual artist examining systems of production and value placed on uniqueness in art.",
        exhibition_url="https://www.petzel.com/exhibitions/allan-mccollum",
        artist_url="https://allanmccollum.net/",
        galleriesnow_url="https://www.galleriesnow.net/gallery/petzel/",
    ),
    Exhibition(
        title="Thought In Material, Selected Works 1984-2025",
        artist="Andrew Lord",
        gallery="Gladstone Gallery",
        location="Gladstone Gallery, 515 West 24th Street, New York, NY",
        start_date="2026-01-15",
        end_date="2026-02-21",
        description="A survey spanning four decades of Andrew Lord's sculptural practice.",
        artist_bio="Andrew Lord (b. 1950) is a British sculptor known for ceramic works that challenge boundaries between craft and fine art.",
        exhibition_url="https://www.gladstonegallery.com/exhibition/andrew-lord-thought-in-material",
        artist_url="https://www.gladstonegallery.com/artist/andrew-lord",
        galleriesnow_url="https://www.galleriesnow.net/gallery/gladstone-gallery/",
    ),
    Exhibition(
        title="Works from the 1960s",
        artist="Sol LeWitt",
        gallery="Paula Cooper Gallery",
        location="Paula Cooper Gallery, 524 West 26th Street, New York, NY",
        start_date="2026-01-15",
        end_date="2026-02-28",
        description="Foundational works from the 1960s, when Sol LeWitt developed the conceptual art principles that defined his career.",
        artist_bio="Sol LeWitt (1928-2007) was linked to Conceptual art and Minimalism, famous for wall drawings and 'structures.'",
        exhibition_url="https://www.paulacoopergallery.com/exhibitions/sol-lewitt-works-from-the-1960s",
        artist_url="https://www.paulacoopergallery.com/artists/sol-lewitt",
        galleriesnow_url="https://www.galleriesnow.net/gallery/paula-cooper-gallery/",
    ),
    Exhibition(
        title="Between the Clock and the Bed",
        artist="Jasper Johns",
        gallery="Gagosian",
        location="Gagosian, 980 Madison Avenue, New York, NY",
        start_date="2026-01-22",
        end_date="2026-03-14",
        description="Works exploring Jasper Johns' iconic crosshatch motif.",
        artist_bio="Jasper Johns (b. 1930) is one of the most influential American artists of the 20th century, known for flags, targets, and crosshatch paintings.",
        exhibition_url="https://gagosian.com/exhibitions/jasper-johns-between-the-clock-and-the-bed/",
        artist_url="https://gagosian.com/artists/jasper-johns/",
        galleriesnow_url="https://www.galleriesnow.net/shows/jasper-johns-between-the-clock-and-the-bed/",
    ),
    Exhibition(
        title="Gathering Wool",
        artist="Louise Bourgeois",
        gallery="Hauser & Wirth",
        location="Hauser & Wirth, 542 West 22nd Street, New York, NY",
        start_date="2026-01-15",
        end_date="2026-04-18",
        description="Sculptures, reliefs, and works on paper exploring themes of memory, the body, and psychological states.",
        artist_bio="Louise Bourgeois (1911-2010) was a French-American artist best known for large-scale sculpture. She is most famous for her spider sculptures.",
        exhibition_url="https://www.hauserwirth.com/hauser-wirth-exhibitions/louise-bourgeois-gathering-wool/",
        artist_url="https://www.hauserwirth.com/artists/louise-bourgeois/",
        galleriesnow_url="https://www.galleriesnow.net/gallery/hauser-wirth/",
    ),
]

# ============================================================================


def add_manual_exhibitions():
    """Add manual exhibitions to the cache"""
    # Load existing
    existing = load_cached_exhibitions()
    existing_keys = {(e.title.lower(), e.gallery.lower()) for e in existing}

    # Add new ones
    added = 0
    for ex in MANUAL_EXHIBITIONS:
        key = (ex.title.lower(), ex.gallery.lower())
        if key not in existing_keys:
            existing.append(ex)
            existing_keys.add(key)
            added += 1
            print(f"Added: {ex.artist}: {ex.title}")
        else:
            print(f"Skipped (already exists): {ex.artist}: {ex.title}")

    # Save
    save_exhibitions_cache(existing)
    print(f"\nAdded {added} new exhibitions. Total: {len(existing)}")


if __name__ == "__main__":
    add_manual_exhibitions()
