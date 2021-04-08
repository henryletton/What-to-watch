'''
    File name: data_sourcing_v2.py
    Author: Henry Letton
    Date created: 2021-03-03
    Python Version: 3.8.3
    Desciption: Sourcing Netflix data, not currenly used or fully working
'''

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from src.db_fns import create_engine2, df_to_sql_db, sql_db_to_df
import numpy as np

#%% Loop through site to get full list of film urls
# Define list of all catalogue pages with films on
catalogue_urls_short = [f'/catalogue/a2z/all/{catalogue_page}' for catalogue_page in list('abcdefghijklmnopqrstuvwxyz')]
catalogue_urls_short.insert(0, '/catalogue/a2z/all')

# Empty list to populate 
catalogue_urls_short_compl = []

# Empty list to add film urls to
film_urls_short = []

headers = {'User-Agent':
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
           ' Chrome/86.0.4240.193 Safari/537.36'}

# Loop through catalogue_urls
while catalogue_urls_short:

    catalogue_url_short = catalogue_urls_short[0]
    catalogue_url = f'https://uk.newonnetflix.info{catalogue_url_short}'
    
    response = requests.get(catalogue_url, headers=headers)
    print(f'{catalogue_url_short} - {response.status_code}')
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    
    # Save any film links
    links = [link.get('href') for link in soup.findAll('a', attrs={'href': re.compile('^/info/')})]
    film_urls_short.extend(links)
    
    
    # Check if there are any next pages
    next_page = soup.findAll('a', attrs={'href': re.compile(f'^{catalogue_url_short}\?start')})
    
    # Skip this section if no next pages
    if next_page:
        next_pages = list(set([link.get('href') for link in next_page]))
        
        # If page in neither list, needs to be added to catalogue list
        for page in next_pages:
            if page not in catalogue_urls_short_compl and page not in catalogue_urls_short:
                catalogue_urls_short.append(page)
                
                
    catalogue_urls_short.pop(0)
    catalogue_urls_short_compl.append(catalogue_url_short)

#%% Use film urls and previously stored films to get new and removed Netflix film lists
# Dedup film links
film_urls_short = list(set(film_urls_short))
film_urls_short.sort()
film_ids = [film_url_short.replace('/info/','') for film_url_short in film_urls_short]

# Get currently stored film ids
engine = create_engine2()
W2W_Films = sql_db_to_df(engine, 'W2W_Films')

# Get list of newly added films, and convert to urls
new_film_ids = list(np.setdiff1d(film_ids,list(W2W_Films['film_key'])))
new_film_urls_short = [f'/info/{film_ids}' for film_ids in new_film_ids]

# Get list of removed films and convert to int
rmv_film_ids = list(np.setdiff1d(list(W2W_Films['film_key']),film_ids))
rmv_film_ids_str = [str(film_id) for film_id in rmv_film_ids]

#%% Remove films no longer on Netflix
if len(rmv_film_ids) > 0:
    drop_rmv_films_sql = f'DELETE FROM W2W_Films WHERE film_key in ({",".join(rmv_film_ids_str)});'
    
    with engine.begin() as cnx:
        cnx.execute(drop_rmv_films_sql)

#%% Get new to Netflix film information
# Store past films in this list
film_urls_done = []

# Empty list to store film dictionaries
film_dicts = []

# Loop through films 
count = 1
while new_film_urls_short:

    film_url_short = new_film_urls_short[0]
    
    film_url = f'https://uk.newonnetflix.info{film_url_short}'
    response = requests.get(film_url, headers=headers)
    print(f'{count} {film_url} - {response.status_code}') # Count of films instead
    
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Dictionary to store film info
        film_dict = {}
        
        film_dict['film_key'] = int(film_url_short.split('/')[2])
        
        film_dict['title'] = soup.select('h1 a')[0].text
        
        # Any information stored in p parts, is extracted based on text matching logic (as the webpage can change between films)
        all_p_text = [p.text for p in soup.find_all('p')]
    
        desc_next = False
        for p_text in all_p_text:
            if 'Year: ' in p_text:
                film_dict['year'] = int(p_text[6:10])
            elif 'Duration: ' in p_text:
                film_dict['duration'] = p_text[10:]
            elif desc_next:
                film_dict['description'] = p_text
                desc_next = False
            elif 'Description:' in p_text:
                desc_next = True
        
        film_dict['genres'] = soup.select('h5')[0].text
        
        # Rating information changes betwen films too, and can be in a different form
        ratings = list(set([rating['title'] for rating in soup.select('p > .starrating')]))
        
        for rating in ratings:
            rating2 = rating.split(' rating ')
            if len(rating2) > 1:
                score_type = rating2[0].replace(' ', '_').lower()
                if '/' in rating2[1]:
                    score2 = rating2[1].split('/')
                    score = float(score2[0]) / float(score2[1])
                if '%' in rating2[1]:
                    score2 = rating2[1].split('%')
                    score = float(score2[0]) / 100
                
                film_dict[f'{score_type}_rating'] = score
        
        film_dicts.append(film_dict)
    except:
        print('Issue with this film page')
    
    
    count += 1
    film_urls_done.append(film_url_short)
    new_film_urls_short.pop(0)

# Convert list of dictionaries into a dataframe
film_df = pd.DataFrame(film_dicts)
film_df['platform'] = 'Netflix'


#%% Insert new film data
# Connect to database
engine.connect()
if len(film_dicts) > 0:
    W2W_Films = df_to_sql_db(engine = engine, df_write = film_df, 
                             table_name = 'W2W_Films', replace = True)
