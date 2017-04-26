# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 13:46:38 2017

@author: SERNMO
"""

#%% Import packages
import pymysql

#%% Create local connection to MySQL DB
def getConnection():
    connection = pymysql.connect(host='localhost',
                                 user='sernmo',
                                 password='mysqlpwd01',
                                 db='stationdata',
                                 charset='utf8mb4',
                                 local_infile=True,
                                 cursorclass=pymysql.cursors.DictCursor)
    return(connection)