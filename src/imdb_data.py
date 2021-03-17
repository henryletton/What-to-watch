'''
    File name: imdb_data.py
    Author: Henry Letton
    Date created: 2021-03-09
    Python Version: 3.8.3
    Desciption: Getting data from imdb source
    NOTE: Could add date filter to only add recent films and cutdown run time
'''

import requests
import gzip
import shutil
import pandas as pd
from src.db_fns import create_engine2, df_to_sql_db, sql_db_to_df
import numpy as np
import hashlib

# Move to correct folder
import os
os.getcwd()
os.chdir('C:/Users/henry/OneDrive/Documents/AXA Insurance/Henry and Max Projects/What-to-watch')

# Download .gz files
files = ['title.basics','title.ratings']
dfs = [file.replace('.','_') for file in files]

# Loop through files
for file, df in zip(files,dfs):
    # Download .gz file
    url = f'https://datasets.imdbws.com/{file}.tsv.gz'
    r = requests.get(url, allow_redirects=True)
    with open(f'data/{file}.tsv.gz', 'wb') as f_out:
        f_out.write(r.content)
    
    # Conver to .tsv
    with gzip.open(f'data/{file}.tsv.gz', 'rb') as f_in:
        with open(f'data/{file}.tsv', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    # Read into python
    temp = pd.read_csv(f'C:/Users/henry/Downloads/{file}.tsv', sep='\t', header=0)     
    exec(f'{df} = temp')
    del(temp)

title_basics['startYear2'] = [re.sub('[^0-9]', '', val) for val in list(title_basics['startYear'][0:10])]

title_basics2 = title_basics.copy()

#title_basics2 = title_basics2.replace('\\N', '')
title_basics2['startYear'] = pd.to_numeric(title_basics2['startYear'], errors='coerce')
title_basics2['endYear'] = pd.to_numeric(title_basics2['endYear'], errors='coerce')
title_basics2['runtimeMinutes'] = pd.to_numeric(title_basics2['runtimeMinutes'], errors='coerce')

title_all = pd.merge(title_basics2, title_ratings, how='outer')

str_to_hash_list = title_all['primaryTitle'].map(str) + title_all['startYear'].map(str)
film_key = [hashlib.md5(str_to_hash.encode()).hexdigest() for str_to_hash in str_to_hash_list]
title_all['film_key'] = film_key

#%% Connect to My SQL database
engine = create_engine2()

#%%
W2W_Films = sql_db_to_df(engine, 'W2W_Films')

title_fil = pd.merge(title_all, W2W_Films, left_on = ['primaryTitle','startYear'],
                     right_on = ['title','year'])

title_fil2 = pd.merge(title_all, W2W_Films, left_on = ['originalTitle','startYear'],
                     right_on = ['title','year'])

len(list(set(title_fil['film_key_y'])))
len(list(set(title_fil2['film_key_y'])))
len(list(set(title_fil['film_key_y'] + title_fil2['film_key_y'])))

#%% Write dataframes to tables in database (in smaller chunks to avoid sql errors)
insert_size = 100000
for idx in np.arange(0, 7684053, insert_size).tolist():
    print(f'{idx} to {idx+insert_size}')
    df_to_sql_db(engine = engine,
                 df_write = title_all.iloc[idx:idx+insert_size],
                 table_name = 'imdb_films',
                 replace = True)




test = title_all[7000000:7000010]

