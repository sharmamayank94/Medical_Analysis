# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 14:28:12 2020

@author: MAYANK
"""
import pandas as pd
import mysql.connector
import datetime
from datetime import timedelta
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import time
database = mysql.connector.connect(host="localhost", database="medical", 
                                   passwd="test", user = 'root')

db = database.cursor()
while True:
    db.execute("select max(s_no) from bill")
    s_no = db.fetchall()
    print(s_no)
    while True:
        database = mysql.connector.connect(host="localhost", database="medical", 
                                   passwd="test", user = 'root')
        db = database.cursor()
        time.sleep(2)
        db = database.cursor()
        db.execute("select max(s_no) from bill")
        s_no_temp = db.fetchall()
        print(s_no_temp)
        if(s_no_temp != s_no):
            break
        
    db.execute("select medicine_name,category from bill where bill_no = "+
               "(select bill_no from bill where s_no = (select max(s_no) from bill))")
    data = db.fetchall()
    print(data, "This is data")
    print(len(data))
    regressor = LinearRegression()
    
    while len(data)>0:
        print("here")
        nameandcategory = data.pop()
        med_name, category = nameandcategory[0], nameandcategory[1]
        startdate= datetime.date.today() + timedelta(days=-60)
            
        db.execute("select sum(bill_quantity),date from bill where medicine_name='"
                   +med_name+"'and category='"+category+"' and date>='"
                   +str(startdate)+"' group by date ")
        
        
        df = pd.DataFrame(db.fetchall())
        print(df)
        if(df.empty): continue
        parsedate = startdate
        while parsedate<=datetime.date.today():
            if parsedate not in df[1].values:
                df=df.append({0:0, 1:parsedate}, ignore_index=True)
            parsedate += timedelta(days=1)
        
        df=df.sort_values(1)
        
        samples = [10, 7, 3]
        need = []
        while len(samples)>0:
            
            df3=df[df[1]>datetime.date.today()+timedelta(days=-samples.pop())]
               
            regressor.fit(pd.to_datetime(df3[1]).values.reshape(-1,1), df3[0])
           
            today = datetime.date.today()
            upcoming_dates = pd.to_datetime(np.asarray([today, today+timedelta(days=1), 
                                                        today+timedelta(days=2),
                                                        today+timedelta(days=3), 
                                                        today+timedelta(days=4), 
                                                        today+timedelta(days=5), 
                                                        today+timedelta(days=6), 
                                                        today+timedelta(days=7),
                                                        today+timedelta(days=8),
                                                        today+timedelta(days=9),
                                                        today+timedelta(days=10)]))
            
            
            upcoming_dates_prediction = regressor.predict(upcoming_dates.values.astype(float).reshape(-1,1))
            plt.figure(figsize=(10,6))
            plt.plot(df3[1], df3[0], color='red')
            
           
            plt.plot(df3[1], regressor.predict(pd.to_datetime(df3[1]).values.astype(float).reshape(-1,1)))     
            plt.plot(upcoming_dates, upcoming_dates_prediction)
            plt.xticks(df3[1], rotation="70")
            
                
            upcoming_dates_prediction = [max(x,0) for x in upcoming_dates_prediction]
            
            need.append(sum(upcoming_dates_prediction))
            print(max(need), " need")
       
        db.execute("Select sum(total_quantity) from medicine where name = '"+
                   med_name+"' and category='"+category+"'") 
        quantity_left = db.fetchall()[0][0]
        print(quantity_left)
        if(quantity_left<max(need)):
            db.execute("update medicine set X_Factor = 0 where name = '"+med_name+
                       "' and category = '"+category+"'")
        
        else:
            db.execute("update medicine set X_Factor = 1 where name = '"+med_name+
                       "' and category = '"+category+"'")
        
        database.commit()