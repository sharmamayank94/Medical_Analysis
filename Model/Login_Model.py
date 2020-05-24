# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 19:07:09 2020

@author: MAYANK
"""
import mysql.connector

connection = mysql.connector.connect(database='medical', user = 'root', passwd='test', host='localhost')
mycursor = connection.cursor()
def login(username, password):
    
    mycursor.execute("select 1 from users where user_name = '"+username+"' and password = '"+password+"'")
    db = mycursor.fetchall()
    
    if(len(db)==1):
        return True
    else:
        return False

