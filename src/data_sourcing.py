'''
    File name: data_sourcing.py
    Author: Henry Letton
    Date created: 2021-01-26
    Python Version: 3.8.3
    Desciption: Any functions relataing to sourcing data
'''

#%% Import any modules or functions required
from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm
from src.db_fns import create_engine2, insert_film_db

#%% Connect to My SQL database
engine = create_engine2()

#%% Netflix
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
        
        
        
        # Insert film into database
        insert_film_db(engine = engine,
                       details = (title, year, desc, "Netflix", tag),
                       update = True)
         



