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
import glob
import connection

#%%
# 1) Convert image key (in unix epoch time) to gregorian calander timestamp
et = time.time()
print(et)
ct = time.ctime(et)
print(ct)

#%%
# 2) Create table in seriscixi db to store image data, use sp


#connect to the database
connection = connection.getConnection()
cursor = connection.cursor()
#cursor.callproc('sp_create_tbl_skycamera')

connection.commit()
    
#%%
# 3) Load image data into table
#load the text file (first with \r\n line terminators
root = "/data/skycamera/sky01/Data"
filelist = glob.glob("%s/*.txt" % root)
filename = max(filelist)
print("Loading image data files")
load_sql = "LOAD DATA LOCAL INFILE %s \
INTO TABLE SKY402 \
FIELDS TERMINATED BY '\t' \
LINES TERMINATED BY '\n' \
IGNORE 1 LINES;" #header
cursor.execute(load_sql, (filename))    
connection.commit()
connection.close()