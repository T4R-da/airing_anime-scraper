# Anime Schedule Scraper

A Python web scraper that fetches the weekly anime airing schedule from [animeschedule.net](https://animeschedule.net/).

## Features

- Scrapes the full weekly timetable and lets you browse anime by day
- Displays airing times in a human-readable format (e.g. `09:30 AM`)
- Filters out duplicate entries
- Quick-view mode for today's TV anime only (excludes Movies, OVAs, and Specials)

## Files

| File | Description |
|------|-------------|
| `main.py` | Early prototype — fetches the schedule and prints all days with their anime lists |
| `anyday.py` | Interactive CLI — prompts you to pick a day and shows the top 5 airing anime |
| `current_day.py` | Minimal script — prints all TV anime airing on the current day |

## Requirements

- Python 3.10+
- `requests`
- `beautifulsoup4`

Install dependencies with:

```bash
pip install requests beautifulsoup4
```

## Usage

**Browse anime by day (interactive):**

```bash
python anyday.py
```

You'll be shown a numbered list of days and prompted to pick one. The script will then display up to 5 anime airing on that day along with their air times.

**See what's airing today:**

```bash
python current_day.py
```

Prints all TV anime airing on the current day, sourced from the site's highlighted "today" column.

## Example Output

```
Fetching anime schedule...

Available days:
  1. Monday
  2. Tuesday
  3. Wednesday
  ...

Enter the day name or number: 3

Anime airing on Wednesday (showing 5):
  1. My Hero Academia  —  05:30 AM
  2. Demon Slayer      —  11:15 PM
  ...
```

## Notes

- Air times are parsed from ISO 8601 datetime strings and converted to local 12-hour format.
- Only `TV` type entries are shown in `current_day.py`; `anyday.py` includes all aired show types.
- The site structure may change over time — if scraping breaks, inspect the CSS classes used in the `find`/`find_all` calls.