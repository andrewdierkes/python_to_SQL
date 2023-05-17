#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pathlib as path
import pandas as pd
import csv
from itertools import zip_longest
import sqlite3
import os


# In[43]:


_path = path.Path.cwd()

for _filepath in _path.iterdir():
    if _filepath.suffix != r'.log':
        continue
    elif _filepath.suffix == r'.log':
    
        
        with open(_filepath, 'r') as file:
            
            #name log file with os spilt, taking only end
            log_head, log_tail = os.path.split(_filepath)
            
            data = [row for row in csv.reader(file)]

            df = pd.DataFrame(
            {i: item for i, item in enumerate(zip_longest(*data, fillvalue=pd.NA))}
            )

            #make column names iterable in SQL
            col_name = []
            for col in df.columns:
                col_name.append('row_'+str(col))

            df.columns = col_name

            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)

            #connect & convert to SQL table
            conn = sqlite3.connect('polymer_stability.db', timeout=10)
            cur = conn.cursor()

            df.to_sql(f'log_file{log_tail}', conn, if_exists='replace')
            
            conn.close()
       


# In[ ]:




