# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 15:14:37 2017

@author: SERNMO
"""
#%% Import packages
import glob
import connection

#%% connect to the database
connection = connection.getConnection()
cursor = connection.cursor()
    
#%% Load image data into table
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
