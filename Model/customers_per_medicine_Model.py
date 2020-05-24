# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 19:56:09 2020

@author: MAYANK
"""
import mysql.connector
import pandas as pd
database = mysql.connector.connect(database="medical", user="root", passwd="test", host="localhost")

def customers_per_medicine():
    db = database.cursor()
    db.execute("select count(distinct(customer)),medicine_name from bill group by medicine_name" )
    data = db.fetchall()
    df = pd.DataFrame(data)
    return df

  