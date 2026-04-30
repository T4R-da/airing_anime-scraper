import requests
import bs4
from bs4 import BeautifulSoup
from dataclasses import dataclass

WEBSITE = "https://animeschedule.net/"


def get_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, features="html.parser")

def get_anime_list(div_day_timetable: bs4.Tag) -> set:    
    anime_list = set()
    
    div_anime_body = div_day_timetable.find_all("div", class_=["timetable-column-show", "aired"])

    # title - h2 show-title-bar
    for item in div_anime_body:
        title = item.find("h2", class_={"show-title-bar"})

        anime_list.add(title.text)

    return anime_list

@dataclass
class DayData:
    name: str
    anime_list: set

def run():
    soup = get_soup(requests.get(WEBSITE).text)

    # Get timetable body
    div_timetable_body = soup.find("div", {"id": "timetable"})

    # Get monday niggerday
    div_timetable_days = div_timetable_body.find_all("div",  class_=["timetable-column"])    

    days = []

    for div_day in div_timetable_days:
        day = div_day.get("class")[-1] # type: ignore
        print(f"DAY: {day}")

        day_data = DayData(day, get_anime_list(div_day))

        print(day_data)



if __name__ == "__main__":
    run()