from bs4 import BeautifulSoup
import requests
import re
import sqlite3
from tqdm import tqdm

if __name__ == "__main__":
    conn = sqlite3.connect("./films.sqlite")

    create_table = """CREATE TABLE IF NOT EXISTS Films (
                           title text PRIMARY KEY NOT NULL
                           , year int
                           , description text
                           , platform text
                           , tag text)"""

    conn.execute(create_table)

    # Netflix
    # Need headers to be defined or web server gives 403 response
    headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                   ' Chrome/86.0.4240.193 Safari/537.36'}

    for start_letter in tqdm("abcdefghijklmnopqrstuvwxyz", unit="letters"):
        page = requests.get(f"https://uk.newonnetflix.info/catalogue/a2z/all/{start_letter}", headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        infopop_a_tags = soup.find_all('a', class_="infopop")

        for film in infopop_a_tags:
            # If the a tag has an img tag nested, it's the image not the hyperlink so skip
            if film.find_all('img'):
                continue

            full_description = film["title"]

            # Extract the description and optional tag like [New Episodes]
            desc_regex = re.search(r"(?:\[(.*)\])?(.*)", full_description)

            # If there's no tag, just use empty string
            try:
                tag = desc_regex.group(1).strip()
            except AttributeError:
                tag = ""

            desc = desc_regex.group(2).strip()

            # Title and year are in the actual value of the a tag
            link_text = film.get_text()

            # Extract title and year using regex
            title_year_regex = re.search(r"(.*)?.*\((\d{4})\)", link_text)
            title = title_year_regex.group(1).strip()
            year = title_year_regex.group(2).strip()

            # Insert into database
            insert_film = """INSERT OR REPLACE INTO Films (title, year, description, platform, tag)
             VALUES (?, ?, ?, ?, ?)"""
            conn.cursor().execute(insert_film, (title, year, desc, "Netflix", tag))
        # Commit after each letter is done
        conn.commit()
    conn.close()





