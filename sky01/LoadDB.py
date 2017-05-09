# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 15:14:37 2017

@author: SERNMO
"""
#%% Import packages
import glob
import connection

#%% Connect to DB
connection = connection.getConnection()
cursor = connection.cursor()
    
#%% Load image data into DB
root = "/data/skycamera/sky01/Data"
filelist = glob.glob("%s/*.txt" % root)
filename = max(filelist)
tablename = 'SIN402'
print("Loading image data files")
load_sql = ("LOAD DATA LOCAL INFILE '%s' "
            "REPLACE INTO TABLE %s " 
            "FIELDS TERMINATED BY '\t' " 
            "LINES TERMINATED BY '\n' "
            "IGNORE 1 LINES; ")
cursor.execute(load_sql % (filename, tablename))    
connection.commit()
connection.close()

