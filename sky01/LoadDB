# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 15:14:37 2017

@author: SERNMO
"""
#%% Import packages
import time
import os
import pymysql
from datetime import datetime
import pandas as pd

#%%
# 1) Convert image key (in unix epoch time) to gregorian calander timestamp
et = time.time()
print(et)
ct = time.ctime(et)
print(ct)

#%%
# 2) Create table in seriscixi db to store image data, use sp

def getConnection():
    connection = pymysql.connect(host='localhost',
                                 user='sernmo',
                                 password='mysqlpwd01',
                                 db='stationdata',
                                 charset='utf8mb4',
                                 local_infile=True,
                                 cursorclass=pymysql.cursors.DictCursor)
    return(connection)

#connect to the database
connection = getConnection()
cursor = connection.cursor()
#cursor.callproc('sp_create_tbl_skycamera')

connection.commit()
    
#%%
# 3) Load image data into table
#load the text file (first with \r\n line terminators
root = "/data/skycamera/sky01/Data"
ed = str(int(round(et/86400))) #current epoch day
filename = '%s.txt' % ed
filename = os.path.join(root, filename)
print("Loading image data files")
load_sql = "LOAD DATA LOCAL INFILE %s \
INTO TABLE SKY402 \
FIELDS TERMINATED BY '\t' \
LINES TERMINATED BY '\n' \
IGNORE 1 LINES;" #header
cursor.execute(load_sql, (filename))    
connection.commit()
connection.close()
