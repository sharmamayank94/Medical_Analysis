 # -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 20:56:42 2020

@author: LENOVO
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pandas import DataFrame
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import calendar as calendar
from datetime import date
from datetime import datetime
from datetime import timedelta
import mysql.connector
import pandas as pd 
import numpy as np
import datetime as d;



class ProfitPerDayAnalysis():
    
    def __init__(self, username):
        self.username = username
        db = mysql.connector.connect(host='localhost',database='medical',user='root',passwd='test')
        self.dbcursor = db.cursor()
        #self.dbcursor.execute("select distinct(Name) from medicine")
        #self.result = self.dbcursor.fetchall()
        #self.medicines = list(self.result)
        #self.dbcursor.execute("select distinct(Category) from medicine")
        #self.result = self.dbcursor.fetchall()
        #self.category = list(self.result)
        #self.med_name = "Chlorpheniramine"
        #self.cat_name = "Capsule"
        self.sale_in = "Last month"
        self.month = date.today().month - 1
        self.fromday="1"
        self.interval = 7
        self.year = str(d.datetime.now().year)
        self.totalBars = 4
    
        self.init_components()
        self.showGraph1()
        self.showGraph2()
        self.showGraph3()
        self.configure_components()
        self.pack_components()
        self.run()
        
    def init_components(self):
        self.window = tk.Tk()
        
        #self.selected_med = StringVar()
        #self.selected_cat = StringVar()
        self.selected_sale_in = StringVar()
        self.heading_label = tk.Label(self.window, text="Profit Analysis",font="Verdana 18 bold", fg="white")
        
        self.sale_in_label = tk.Label(self.window, text="Profit in : ", font="Verdana 12 ", anchor=E)
        #self.from_label = tk.Label(self.window, text="From : ", font="Verdana 12 ", anchor=E)
        self.to_label = tk.Label(self.window, text="To : ", font="Verdana 12 ")
        self.sale_in_combo = ttk.Combobox(self.window, values=["Last Year","Last month","Last week"], width="25", textvariable = self.selected_sale_in)
        self.From_Cal = DateEntry(self.window, width=15, background='darkblue',
    foreground='white', borderwidth=2)
        self.To_Cal = DateEntry(self.window, background='darkblue',
    foreground='white', borderwidth=2, width=15)
        
        #self.backbtn = tk.Button(self.window, text="Back", bg="#63D792", fg="white", activebackground="#63D7CC")
        self.homebtn = tk.Button(self.window, text="Home", bg="#D76386", fg="white", activebackground="#D763C2", command = self.home)
        self.logoutbtn = tk.Button(self.window, text="Log Out", bg="#D79F63", fg="white", activebackground="#D77D63", command = self.logout)
        
        
        #graph3
        self.figure1 = plt.Figure(figsize=(4.5,5.6), dpi=100)
        self.ax1 = self.figure1.add_subplot(111)
        self.bar1 = FigureCanvasTkAgg(self.figure1, self.window)
        
        #graph1
        self.figure2 = plt.Figure(figsize=(4.5,5.6), dpi=100)
        self.ax2 = self.figure2.add_subplot(111)
        self.bar2 = FigureCanvasTkAgg(self.figure2, self.window)
        
        self.profit_on_label = tk.Label(self.window, text="Profit on : ", font="Verdana 12 ", anchor=E)
        self.profit_on_Cal = DateEntry(self.window, background='darkblue',
    foreground='white', borderwidth=2, width=15)
        
        #graph2
        self.figure3 = plt.Figure(figsize=(5,5.6), dpi=100)
        self.ax3 = self.figure3.add_subplot(111)
        self.bar3 = FigureCanvasTkAgg(self.figure3, self.window)
        
    def configure_components(self):
        self.window.configure(bg="#d7eaf5")
        self.heading_label.configure(bg="#0064de")                      
        self.sale_in_label.configure(bg="#d7eaf5")
        #self.from_label.configure(bg="#d7eaf5")
        self.to_label.configure(bg="#d7eaf5")
        self.profit_on_label.configure(bg="#d7eaf5")
       
        self.ax1.patch.set_facecolor("#d7eaf5")
        self.ax2.patch.set_facecolor("#d7eaf5")
        self.ax2.patch.set_facecolor("#d7eaf5")
     
    def showGraph1(self):

        #------------#
        self.df = pd.DataFrame()
        if self.sale_in=="Last month":
            self.month = date.today().month - 1
            self.fromday="1"
            self.interval = 7
            self.year = str(d.datetime.now().year)
            self.totalBars = 4
            self.startdate= self.year+"-"+str(self.month)+"-"+self.fromday
            self.startdate = datetime.strptime(self.startdate, '%Y-%m-%d')
            self.toDate = self.startdate + timedelta(days=self.interval)
            self.bar=1
        
            while(self.bar<=self.totalBars): 
                self.dbcursor.execute("select medicine.Name, medicine.Tax, medicine.Cost_Price/medicine.No_Of_Medicines_Per_Strip as cp, bill.Amount, bill.Rate, bill.Bill_Quantity,bill.Date from medicine inner join bill on bill.Medicine_Name = medicine.Name and bill.Batch_No = medicine.Batch_No  AND Date BETWEEN '" + str(self.startdate) + "' AND '" + str(self.toDate) + "'")
                
                #self.dbcursor.execute("select count(Bill_Quantity) from bill where Medicine_Name = '" + self.med_name + "' and Category='" + self.cat_name + "' AND Date BETWEEN '" + str(self.startdate) + "' AND '" + str(self.toDate) + "'")
                self.result = self.dbcursor.fetchall()
                self.resultlen = self.dbcursor.rowcount
                self.df2 = pd.DataFrame(self.result)
                
                if self.resultlen==0:
                    self.df2['Profit']=0
                else:
                    self.df2['Profit'] = (self.df2[3]-(self.df2[4]*self.df2[5]*0.02*self.df2[1]))-(self.df2[2]*self.df2[5])
                
                self.df = self.df.append({'Week':'week'+str(self.bar),'Profit':self.df2['Profit'].sum()}, ignore_index=True)
                self.bar = self.bar+1
                self.startdate = self.toDate + timedelta(days=1)
                self.toDate = self.startdate + timedelta(days=self.interval)
            
        elif self.sale_in=="Last Year":
            self.month = date.today().month
            self.fromday = "1"
            self.year = str(d.datetime.now().year - 1)
            self.totalBars = 12
            self.bar = 1
            self.startdate = self.year+"-"+str(self.month)+"-"+self.fromday
            self.startdate = datetime.strptime(self.startdate, '%Y-%m-%d')
            
            while(self.bar<=self.totalBars):
                self.month = self.startdate.month
                self.year = self.startdate.year
                self.interval = calendar.monthrange(self.year,self.month)[1]
                self.toDate = self.startdate + timedelta(days=self.interval)
               
                self.dbcursor.execute("select medicine.Name, medicine.Tax, medicine.Cost_Price/medicine.No_Of_Medicines_Per_Strip as cp, bill.Amount, bill.Rate, bill.Bill_Quantity,bill.Date from medicine inner join bill on bill.Medicine_Name = medicine.Name and bill.Batch_No = medicine.Batch_No  AND Date BETWEEN '" + str(self.startdate) + "' AND '" + str(self.toDate) + "'")
                self.result = self.dbcursor.fetchall()
                self.len = self.dbcursor.rowcount
                self.df2 = pd.DataFrame(self.result)
                if self.len==0:
                    self.df2['Profit']=0
                else:
                    self.df2['Profit'] = (self.df2[3]-(self.df2[4]*self.df2[5]*0.02*self.df2[1]))-(self.df2[2]*self.df2[5])
                
                #self.dbcursor.execute("select count(Bill_Quantity) from bill where Medicine_Name = '" + self.med_name + "' and Category='" + self.cat_name + "' AND Date BETWEEN '" + str(self.startdate) + "' AND '" + str(self.toDate) + "'")
                
                self.xaxis = str(calendar.month_name[self.month])[:3]
               
                self.df = self.df.append({'Week':self.xaxis + str(self.year),'Profit':self.df2['Profit'].sum()}, ignore_index=True, sort=None)
                self.bar = self.bar+1
                self.startdate = self.toDate
                
        else:
            self.startdate = date.today() - timedelta(days=7)
            self.bar=1
            self.totalBars=7
            while(self.bar<=self.totalBars):
                self.dbcursor.execute("select medicine.Name, medicine.Tax, medicine.Cost_Price/medicine.No_Of_Medicines_Per_Strip as cp, bill.Amount, bill.Rate, bill.Bill_Quantity,bill.Date from medicine inner join bill on bill.Medicine_Name = medicine.Name and bill.Batch_No = medicine.Batch_No  AND Date = '" + str(self.startdate) + "'")
                self.result = self.dbcursor.fetchall()
                self.len = self.dbcursor.rowcount
                self.df2 = pd.DataFrame(self.result)
                if self.len==0:
                    self.df2['Profit']=0
                else:
                    self.df2['Profit'] = (self.df2[3]-(self.df2[4]*self.df2[5]*0.02*self.df2[1]))-(self.df2[2]*self.df2[5])
               
                self.bar = self.bar + 1
                self.df = self.df.append({'Week':self.startdate,'Profit':self.df2['Profit'].sum()}, ignore_index=True, sort=None)
                self.startdate = self.startdate + timedelta(days=1)
           
        
        self.bar2.get_tk_widget().grid(row=4, column=0, columnspan=3)
        self.ax2.patch.set_facecolor("#d7eaf5")
        self.df=self.df[['Week','Profit']].groupby('Week', sort=False).sum()
        self.df.plot(kind='bar', legend=True, ax=self.ax2, rot=30)
        self.ax2.set_title("Profit in " + self.sale_in)
        
        
    def showGraph2(self):
        self.startdate = self.From_Cal.get_date()
        self.toDate = self.To_Cal.get_date()
        
        self.dbcursor.execute("select medicine.Name, medicine.Tax, medicine.Cost_Price/medicine.No_Of_Medicines_Per_Strip as cp, bill.Amount, bill.Rate, bill.Bill_Quantity,bill.Date from medicine inner join bill on bill.Medicine_Name = medicine.Name and bill.Batch_No = medicine.Batch_No  AND Date BETWEEN '" + str(self.startdate) + "' AND '" + str(self.toDate) + "'")
        self.result = self.dbcursor.fetchall()
        self.resultlen = self.dbcursor.rowcount
        
        self.df2 = pd.DataFrame(self.result)
        self.x = 0
        self.df1 = pd.DataFrame()
        if self.resultlen==0:
            self.df2['Profit']=0
            self.df1 = self.df1.append({'Date': '', 'Profit' : 0}, ignore_index=True)
        else:
            self.df2['Profit'] = (self.df2[3]-(self.df2[4]*self.df2[5]*0.02*self.df2[1]))-(self.df2[2]*self.df2[5])
            
            self.df2['Date'] = self.df2[6]
    
            
            self.df1 = self.df2.groupby('Date')['Profit'].sum()
            #self.df1 = DataFrame({'profit':self.df2.groupby(['Date']).sum()['Profit']}).reset_index()
           
        #for row in self.result:
         #   self.df1 = self.df1.append({'Date':self.result[1][self.x], 'Sale' : self.result[0][self.x]}, ignore_index=True)
        #if(self.resultlen==0):
         #   self.df1 = self.df1.append({'Date': '', 'Profit' : 0}, ignore_index=True)
        #else:
         #   while(self.x<self.resultlen):
          #      self.df1 = self.df1.append({'Date':self.result[self.x][1], 'Sale' : self.result[self.x][0]}, ignore_index=True)
           #     self.x = self.x+1
        #print(self.df1)
        self.bar1.get_tk_widget().grid(row=4, column=6, columnspan=3, sticky='W')
        
        self.ax1.patch.set_facecolor("#d7eaf5")
        #self.df1 = self.df1[['Date','Profit']].groupby('Date').sum()
        self.df1.plot(legend=True, ax=self.ax1, rot=30, marker="*")
        #self.ax1.plot(self.df1['Date'], self.df1['profit'], color='red')
        self.ax1.set_title(str(self.startdate) + " to " + str(self.toDate))
      
    def showGraph3(self):
        self.profit_on = self.profit_on_Cal.get_date()
        #self.dbcursor.execute("select Medicine_Name, sum(Bill_Quantity) from bill where Date = '" + str(self.profit_on) + "' group by Medicine_Name")
        #self.result = self.dbcursor.fetchall()
        self.profit = 0
        self.dbcursor.execute("select medicine.Name, medicine.Tax, medicine.Cost_Price/medicine.No_Of_Medicines_Per_Strip as cp, bill.Amount, bill.Rate, bill.Bill_Quantity,bill.Date from medicine inner join bill on bill.Medicine_Name = medicine.Name and bill.Batch_No = medicine.Batch_No  AND Date = '" + str(self.profit_on) + "'")
        self.result = self.dbcursor.fetchall()
        self.resultlen = self.dbcursor.rowcount
        self.df1 = pd.DataFrame(self.result)
        
        if self.resultlen==0:
            self.df1 = self.df1.append({'Item' : '', 'Profit' : 0}, ignore_index=True)
        else:
            
            self.df1['Item'] = self.df1[0]
            self.df1['profit'] = (self.df1[4]-self.df1[2])*self.df1[5]
            
            self.profit = self.df1['profit'].sum()
            self.df1 = self.df1.groupby('Item')['profit'].sum()
           
        self.bar3.get_tk_widget().grid(row=4, column=3, columnspan=3)
        self.ax3.patch.set_facecolor("#d7eaf5")
        self.df1.plot(kind='bar', legend=True, ax=self.ax3, rot=30)
        self.ax3.set_title("total profit : " + str(self.profit))
        
    def pack_components(self):
        self.heading_label.grid(row = 0, column = 0,  sticky='ew',columnspan = 10, ipady=20, ipadx = 20, pady=(0, 20))
        #self.backbtn.grid(row = 0, column = 6, ipadx = 15)
        self.homebtn.grid(row = 0, column = 7, ipadx = 13)
        self.logoutbtn.grid(row = 0, column = 8, ipadx = 10)
        
        self.sale_in_label.grid(row = 3, column = 1, sticky=W+E, ipady = 5, pady=5)
        self.sale_in_combo.grid(row = 3, column = 2, pady = 5, padx = 30)
        self.sale_in_combo.current(1)  
        self.sale_in_combo.bind("<<ComboboxSelected>>" , self.graph1Changed)
        self.profit_on_label.grid(row = 3, column=3, sticky=W+E, ipady = 5, pady = 10)
        self.profit_on_Cal.grid(row = 3, column=4, sticky=W)
        self.profit_on_Cal.bind("<<DateEntrySelected>>", self.graph3Changed)
        #self.from_label.grid(row = 3, column = 6, ipady = 5, padx = 0, pady=5)
        self.From_Cal.grid(row = 3, column = 6, pady = 5, sticky=E)
        self.From_Cal.bind("<<DateEntrySelected>>", self.graph1Changed)
        self.to_label.grid(row = 3, column = 7, ipady = 5, padx = 0, pady=5)
        self.To_Cal.grid(row = 3, column = 8, pady = 0, sticky=W)
        self.To_Cal.bind("<<DateEntrySelected>>", self.graph1Changed)
    
    def logout(self):
        self.window.destroy()
        LoginWindow()
    
    def home(self):
        self.window.destroy()
        from Admin_Panel import AdminPanel
        AdminPanel(self.username)
    


    def graph1Changed(self,eventObject):
      
        self.sale_in = str(self.selected_sale_in.get())
        #self.bar2.get_tk_widget().destroy()
        self.ax2.clear()
        
        self.figure2 = plt.Figure(figsize=(4.5,5.6), dpi=100)
        self.ax2 = self.figure2.add_subplot(111)
        self.bar2 = FigureCanvasTkAgg(self.figure2, self.window)
        
        self.ax1.clear()
        self.figure1 = plt.Figure(figsize=(4.5,5.6), dpi=100)
        self.ax1 = self.figure1.add_subplot(111)
        self.bar1 = FigureCanvasTkAgg(self.figure1, self.window)
        
        
        self.showGraph1()
        self.showGraph2()
    
    def graph2Changed(self,eventObject):
        
        self.med_name = str(self.selected_med.get())
        self.cat_name = str(self.selected_cat.get())
        
        
        #self.bar1.get_tk_widget().destroy()
        self.ax1.clear()
        self.figure1 = plt.Figure(figsize=(6,5), dpi=100)
        self.ax1 = self.figure1.add_subplot(111)
        self.bar1 = FigureCanvasTkAgg(self.figure1, self.window)
        self.showGraph2()
        
    def graph3Changed(self, eventObject):
        self.ax3.clear()
        self.figure3 = plt.Figure(figsize=(5,5.6), dpi=100)
        self.ax3 = self.figure3.add_subplot(111)
        self.bar3 = FigureCanvasTkAgg(self.figure3, self.window)
        self.showGraph3()
        
    
    def run(self):
        self.window.geometry("1400x720")
        self.window.mainloop()
        
#ProfitPerDayAnalysis = ProfitPerDayAnalysis()