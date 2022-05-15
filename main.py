import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import spotifyutil
from datetime import datetime


def get_recently_played():
    # Get song details from page
    # Use requests to get the page details
    global recently_played
    kexp_url = 'https://www.kexp.org/playlist/'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.get(kexp_url)
    time.sleep(1)

    # Find all relevant tags and save them as a dictionary
    soup = BeautifulSoup(driver.page_source, 'html.parser').find_all("div", class_="PlaylistItem u-mb1")
    driver.quit()

    # Build the recently played list
    recently_played = []
    for item in soup:
        try:
            track = str(item.find('h3', class_='u-mb0', text=True).string)
            artist = str(item.find('div', class_='u-h3 u-mb1 u-lightWeight', text=True).string)
            recently_played.append({'artist': artist, 'track': track})
        except AttributeError as e:
            pass

    return recently_played


def main():
    # I was quite tired when I wrote this bit. It basically checks if any new songs have been added
    previously_played = []
    while True:
        current = []
        recent = get_recently_played()
        for item in recent:
            if item in previously_played:
                pass
            else:
                current.append(item)
        previously_played = recent
        for item in reversed(current):
            print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " " + item['track'] + ' - ' + item['artist'])

        for item in reversed(current):
            spotifyutil.add_to_playlist([spotifyutil.find_track_id(track=item['track'], artist=item['artist'])])

        time.sleep(5)


if __name__ == "__main__":
    main()
