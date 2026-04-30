import requests
from bs4 import BeautifulSoup

WEBSITE = "https://animeschedule.net/"

# 1. Fetch the site data
html = requests.get(WEBSITE).text
soup = BeautifulSoup(html, features="html.parser")

# 2. Find the column for the current day
div_daily_timetable = soup.find("div", class_="expanded")

if div_daily_timetable:
    # 3. Find all shows where the data-type attribute is exactly "TV"
    # This ignores Movies, OVAs, and Specials
    tv_anime_list = div_daily_timetable.find_all("div", attrs={"data-type": "TV"})

if tv_anime_list: 
    print(f"--- TV Anime Airing Today ---")
    
    for anime in tv_anime_list:
        # 4. Extract the title
        title_tag = anime.find("h2", class_="show-title-bar")
        if title_tag:
            # Using strip() to clean up any extra whitespace
            print(title_tag.text.strip())
else:
    print("There aren't any airing anime at this time!")
