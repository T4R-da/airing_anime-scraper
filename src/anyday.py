import requests
import bs4
import os
import subprocess
import msvcrt
from bs4 import BeautifulSoup
from dataclasses import dataclass
from colorama import Fore, Style

WEBSITE = "https://animeschedule.net/"

def clear():
    cmd = "cls" if os.name == "nt" else "clear"
    subprocess.call(cmd, shell=True)

def get_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, features="html.parser")

def get_anime_list(div_day_timetable: bs4.Tag) -> list[tuple[str, str]]:
    seen = {}

    div_anime_body = div_day_timetable.find_all("div", class_=["timetable-column-show", "aired"])

    for item in div_anime_body:
        title = item.find("h2", class_="show-title-bar")
        time = item.find("time")

        if title and time:
            name = title.text.strip()
            hour = time.get("datetime", time.text).strip()
            if name not in seen:
                seen[name] = hour

    return list(seen.items())

from datetime import datetime

def get_anime_list(div_day_timetable: bs4.Tag) -> list[tuple[str, str]]:
    seen = {}

    div_anime_body = div_day_timetable.find_all("div", class_=["timetable-column-show", "aired"])

    for item in div_anime_body:
        title = item.find("h2", class_="show-title-bar")
        time = item.find("time", class_="show-air-time")

        if title and time:
            name = title.text.strip()
            raw = time.get("datetime", "")
            try:
                dt = datetime.fromisoformat(raw)
                hour = dt.strftime("%I:%M %p")
            except ValueError:
                hour = time.text.strip()
            if name not in seen:
                seen[name] = hour

    return list(seen.items())

@dataclass
class DayData:
    name: str
    anime_list: list[tuple[str, str]]

def get_all_days(soup: BeautifulSoup) -> list[DayData]:
    div_timetable_body = soup.find("div", {"id": "timetable"})
    div_timetable_days = div_timetable_body.find_all("div", class_=["timetable-column"])

    days = []
    for div_day in div_timetable_days:
        day = div_day.get("class")[-1]
        day_data = DayData(day, get_anime_list(div_day))
        days.append(day_data)

    return days

def run():
    print("Fetching anime schedule...")
    soup = get_soup(requests.get(WEBSITE).text)
    days = get_all_days(soup)
    clear()

    day_names = [d.name for d in days]
    print("\nAvailable days:")
    for i, name in enumerate(day_names, 1):
        print(f"\n  {i}. {name.capitalize()}")

    while True:
        choice = input("\nEnter the day name or number: ").strip().lower()

        selected = None
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(days):
                selected = days[idx]
        else:
            selected = next((d for d in days if d.name.lower() == choice), None)

        if selected:
            break
        print(f"Invalid choice. Please enter a number (1-{len(days)}) or a valid day name.")

    clear()
    anime = selected.anime_list[:50]
    print(f"\nAnime airing on {selected.name.capitalize()} (showing {len(anime)}):\n")
    for i, (title, hour) in enumerate(anime, 1):
        print(f"\033[92m {i}. {title}   —   {hour} \n\033[0m")
    print("Press any key to continue...")
    msvcrt.getch()

if __name__ == "__main__":
    run()