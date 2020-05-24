# -*- coding: utf-8 -*-
"""
Created on Sun May 10 19:52:17 2020

@author: MAYANK
"""

import mysql.connector
import pandas as pd

connection = mysql.connector.connect(database="medical", host = "localhost", user="root", passwd = "test")



def get_Medicines_Expiry_Dates(startdate, enddate):
    db = connection.cursor()
    db.execute("select name, total_quantity, expiry from medicine "+
               "where expiry>'{0}' and expiry<'{1}' order by expiry;".format(startdate, enddate)) 
    
    data = db.fetchall()
    df = pd.DataFrame(data)
    return df;
    

