# Art Exhibits Calendar Sync

Automatically fetches art exhibition listings and syncs them to Google Calendar.

## Setup

### 1. Create Python virtual environment

```bash
cd /Users/jordan/jordan-os/art-exhibits
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Set up Google Calendar API credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable the Google Calendar API
4. Go to **APIs & Services > Credentials**
5. Click **Create Credentials > OAuth 2.0 Client ID**
6. Select **Desktop app**
7. Download the JSON file
8. Save it as `credentials.json` in this directory

### 3. First run (authenticate)

```bash
source .venv/bin/activate
python main.py
```

This will open a browser for Google OAuth. After authenticating, tokens are saved for future runs.

## Usage

### Full sync (fetch + calendar update)
```bash
python main.py
```

### Only fetch exhibitions (no calendar sync)
```bash
python main.py --fetch
```

### Only sync cached exhibitions to calendar
```bash
python main.py --sync
```

### Clean up past events
```bash
python main.py --cleanup --days-past 30
```

### Add exhibitions manually
Edit `manual_exhibitions.py` to add exhibitions, then:
```bash
python manual_exhibitions.py
python main.py --sync
```

## Schedule Monthly Runs (macOS)

### Install the launchd job

```bash
# Copy the plist to LaunchAgents
cp com.jordan.art-exhibits-sync.plist ~/Library/LaunchAgents/

# Load the job
launchctl load ~/Library/LaunchAgents/com.jordan.art-exhibits-sync.plist

# Verify it's loaded
launchctl list | grep art-exhibits
```

### Manage the scheduled job

```bash
# Unload (disable)
launchctl unload ~/Library/LaunchAgents/com.jordan.art-exhibits-sync.plist

# Run immediately (for testing)
launchctl start com.jordan.art-exhibits-sync

# Check logs
tail -f logs/launchd-stdout.log
tail -f logs/launchd-stderr.log
```

## Configuration

Edit `config.py` to customize:

- `GOOGLE_EMAIL` - Your Google account email
- `CALENDAR_ID` - Target calendar ID
- `LOCATIONS` - Cities to search (e.g., "new-york", "london")
- `NEIGHBORHOODS` - Specific areas within cities

## File Structure

```
art-exhibits/
├── main.py                 # Main entry point
├── config.py               # Configuration settings
├── fetch_exhibitions.py    # Fetches exhibition data
├── calendar_sync.py        # Google Calendar sync logic
├── manual_exhibitions.py   # Add exhibitions manually
├── requirements.txt        # Python dependencies
├── credentials.json        # Google OAuth credentials (you create)
├── com.jordan.art-exhibits-sync.plist  # macOS scheduled task
├── data/
│   └── exhibitions.json    # Cached exhibition data
└── logs/
    └── sync.log            # Sync logs
```

## Troubleshooting

### "credentials.json not found"
Download OAuth credentials from Google Cloud Console (see Setup step 2).

### "Calendar not found"
Make sure the `CALENDAR_ID` in `config.py` matches your calendar. Get the ID from Google Calendar settings.

### Authentication expired
Delete `~/.google_workspace_mcp/credentials/token.json` and run again.

### Scheduled job not running
Check logs in `logs/` directory. Make sure the plist is loaded:
```bash
launchctl list | grep art-exhibits
```
