import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import subprocess
import msvcrt

WEBSITE = "https://animeschedule.net/"

def clear():
    cmd = "cls" if os.name == "nt" else "clear"
    subprocess.call(cmd, shell=True)

# 1. Fetch and parse first
html = requests.get(WEBSITE).text
soup = BeautifulSoup(html, features="html.parser")

# 2. Get today's name
today = datetime.now().strftime("%A").lower()

# 3. Find today's column using the reliable approach
div_timetable = soup.find("div", {"id": "timetable"})
all_days = div_timetable.find_all("div", class_="timetable-column")

div_daily_timetable = next(
    (d for d in all_days if d.get("class", [])[-1].lower() == today), None
)

if div_daily_timetable:
    all_shows = div_daily_timetable.find_all("div", class_="timetable-column-show")

    if all_shows:
        seen = {}
        for show in all_shows:
            title_tag = show.find("h2", class_="show-title-bar")
            time_tag = show.find("time", class_="show-air-time")
            if title_tag:
                name = title_tag.text.strip()
                if name not in seen:
                    if time_tag:
                        raw = time_tag.get("datetime", "")
                        try:
                            hour = datetime.fromisoformat(raw).strftime("%I:%M %p")
                        except ValueError:
                            hour = time_tag.text.strip()
                    else:
                        hour = "Unknown"
                    seen[name] = hour

        anime_list = list(seen.items())
        clear()
        print(f"\n--- Anime Airing Today ({today.capitalize()}) — {len(anime_list)} shows ---\n")
        for i, (title, hour) in enumerate(anime_list, 1):
            print(f"\033[92m {i}. {title}   —   {hour} \n\033[0m")
        print("Press any key to continue...")
        msvcrt.getch()
    else:
        print("There aren't any airing anime at this time!")
        msvcrt.getch()
else:
    print(f"Couldn't find schedule for {today.capitalize()}.")
    msvcrt.getch()