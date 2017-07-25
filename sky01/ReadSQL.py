# -*- coding: utf-8 -*-
"""
Created on Fri May 26 12:48:23 2017

@author: SERNMO

Sky Camera Project

Read data from a regularly updated MySQL database and
output to a Python dashboard.

Database query part - defines function for retrieving data associated 
with the current image. Direct run will return one row of data.
"""

#%% Import packages
from connection import getConnection

#%% Read data associated to the current image
def read_sql(ImageID, VarName):
    try:
        conn = getConnection()
        cur = conn.cursor()
        args = [ImageID]
        cur.callproc("sp_join_skyghi", args)
        result = cur.fetchall()[0]
        result = result[VarName]
        conn.close()
        return result
    except:
        print('Have you mispelled the variable name?')
