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
import seaborn as sb
#from login import LoginWindow
#from Admin_Panel import AdminPanel

class ProfitAnalysis():
    
    def __init__(self, username):
        self.username = username
        db = mysql.connector.connect(host='localhost',database='medical',user='root',passwd='test')
        self.dbcursor = db.cursor()
        self.dbcursor.execute("select distinct(Name) from medicine")
        self.result = self.dbcursor.fetchall()
        self.medicines = list(self.result)
        self.dbcursor.execute("select distinct(Category) from medicine where Name = 'paracetamol'")
        self.result = self.dbcursor.fetchall()
        self.category = list(self.result)
        self.med_name = "Paracetamol"
        self.cat_name = "Capsule"
        self.sale_in = "Last month"
        self.month = date.today().month - 1
        self.fromday="1"
        self.interval = 7
        self.year = str(d.datetime.now().year)
        self.totalBars = 4
    
        self.init_components()
        self.showGraph1()
        self.showGraph2()
        self.configure_components()
        self.pack_components()
        self.run()
        
    def init_components(self):
        self.window = tk.Tk()
        self.selected_med = StringVar()
        self.selected_cat = StringVar()
        self.selected_sale_in = StringVar()
        self.heading_label = tk.Label(self.window, text="Item Sale Analysis",font="Verdana 18 bold", fg="white")
        self.medicine_name_label = tk.Label(self.window, text="Name", font="Verdana 12 ")
        self.medicine_category_label = tk.Label(self.window, text="Category", font="Verdana 12 ")
        self.choose_item_label = tk.Label(self.window, text="Choose item : ", font="Verdana 12 ", anchor=E)
        self.med_name_combo = ttk.Combobox(self.window, values=self.medicines, width="27", textvariable=self.selected_med)
        self.cat_name_combo = ttk.Combobox(self.window, values=self.category, width="25", textvariable=self.selected_cat)
        self.sale_in_label = tk.Label(self.window, text="Sale in : ", font="Verdana 12 ", anchor=E)
        self.from_label = tk.Label(self.window, text="From : ", font="Verdana 12 ", anchor=E)
        self.to_label = tk.Label(self.window, text="To : ", font="Verdana 12 ")
        self.sale_in_combo = ttk.Combobox(self.window, values=["Last Year","Last month","Last week"], width="25", textvariable = self.selected_sale_in)
        self.From_Cal = DateEntry(self.window, width=20, background='darkblue',
    foreground='white', borderwidth=2)
        self.To_Cal = DateEntry(self.window, background='darkblue',
    foreground='white', borderwidth=2, width=20)
        
        #self.backbtn = tk.Button(self.window, text="Back", bg="#63D792", fg="white", activebackground="#63D7CC")
        self.homebtn = tk.Button(self.window, text="Home", bg="#D76386", fg="white", activebackground="#D763C2", command = self.home)
        self.logoutbtn = tk.Button(self.window, text="Log Out", bg="#D79F63", fg="white", activebackground="#D77D63", command = self.logout)
        
        #graph2
        self.figure1 = plt.Figure(figsize=(6,5), dpi=100)
        self.ax1 = self.figure1.add_subplot(111)
        self.bar1 = FigureCanvasTkAgg(self.figure1, self.window)
        
        #graph1
        self.figure2 = plt.Figure(figsize=(6,5), dpi=100)
        self.ax2 = self.figure2.add_subplot(111)
        self.bar2 = FigureCanvasTkAgg(self.figure2, self.window)
        
    def configure_components(self):
        self.window.configure(bg="#d7eaf5")
        self.heading_label.configure(bg="#0064de")                      
        self.sale_in_label.configure(bg="#d7eaf5")
        self.from_label.configure(bg="#d7eaf5")
        self.to_label.configure(bg="#d7eaf5")
        self.choose_item_label.configure(bg="#d7eaf5")
        self.medicine_name_label.configure(bg="#d7eaf5")
        self.medicine_category_label.configure(bg="#d7eaf5")
        self.ax1.patch.set_facecolor("#d7eaf5")
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
                self.dbcursor.execute("select count(Bill_Quantity) from bill where Medicine_Name = '" + self.med_name + "' and Category='" + self.cat_name + "' AND Date BETWEEN '" + str(self.startdate) + "' AND '" + str(self.toDate) + "'")
                self.result = self.dbcursor.fetchall()
                self.df = self.df.append({'Week':'week'+str(self.bar),'Sale':self.result[0][0]}, ignore_index=True)
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
                print(str(self.startdate) + " " + str(self.toDate))
                self.dbcursor.execute("select count(Bill_Quantity) from bill where Medicine_Name = '" + self.med_name + "' and Category='" + self.cat_name + "' AND Date BETWEEN '" + str(self.startdate) + "' AND '" + str(self.toDate) + "'")
                self.result = self.dbcursor.fetchall()
                self.xaxis = str(calendar.month_name[self.month])[:3]
                print(self.xaxis)
                self.df = self.df.append({'Week':self.xaxis + str(self.year),'Sale':self.result[0][0]}, ignore_index=True, sort=None)
                self.bar = self.bar+1
                self.startdate = self.toDate
                
        else:
            self.startdate = date.today() - timedelta(days=7)
            self.bar=1
            self.totalBars=7
            while(self.bar<=self.totalBars):
                self.dbcursor.execute("select count(Bill_Quantity) from bill where Medicine_Name = '" + self.med_name + "' and Category='" + self.cat_name + "' AND Date = '" + str(self.startdate) + "'")
                self.result = self.dbcursor.fetchall()
                self.bar = self.bar + 1
                self.df = self.df.append({'Week':self.startdate,'Sale':self.result[0][0]}, ignore_index=True, sort=None)
                self.startdate = self.startdate + timedelta(days=1)
                 
        self.bar2.get_tk_widget().grid(row=4, column=0, columnspan=4)
        self.ax2.patch.set_facecolor("#d7eaf5")
        self.df=self.df[['Week','Sale']].groupby('Week', sort=False).sum()
        self.df.plot(kind='bar', legend=True, ax=self.ax2, rot=30)
        self.ax2.set_title(self.med_name)
        
    def showGraph2(self):
        self.startdate = self.From_Cal.get_date()
        self.toDate = self.To_Cal.get_date()
        
        self.dbcursor.execute("select count(Bill_Quantity) as Sale,Date as Date from bill where Medicine_Name = '" + self.med_name + "' and Category='" + self.cat_name + "' AND Date BETWEEN '" + str(self.startdate) + "' AND '" + str(self.toDate) + "' group by date")
        self.result = self.dbcursor.fetchall()
        self.resultlen = self.dbcursor.rowcount
        
        self.df1 = pd.DataFrame()
        self.x = 0
       
        print(self.result)
        #for row in self.result:
         #   self.df1 = self.df1.append({'Date':self.result[1][self.x], 'Sale' : self.result[0][self.x]}, ignore_index=True)
        if(self.resultlen==0):
            self.df1 = self.df1.append({'Date': '', 'Sale' : 0}, ignore_index=True)
        else:
            while(self.x<self.resultlen):
                self.df1 = self.df1.append({'Date':self.result[self.x][1], 'Sale' : self.result[self.x][0]}, ignore_index=True)
                self.x = self.x+1
        
        self.bar1.get_tk_widget().grid(row=4, column=5, columnspan=4, sticky='W')
       
        self.ax1.patch.set_facecolor("#d7eaf5")
        self.df1 = self.df1[['Date','Sale']].groupby('Date').sum()
        self.df1.plot(legend=True, ax=self.ax1, rot=30)
        self.ax1.set_title(str(self.startdate) + " to " + str(self.toDate))
      

    def pack_components(self):
        self.heading_label.grid(row = 0, column = 0,  sticky='ew',columnspan = 10, ipady=20, ipadx = 20, pady=(0, 20))
        
        #self.backbtn.grid(row = 0, column = 6, ipadx = 15)
        self.homebtn.grid(row = 0, column = 7, ipadx = 13)
        self.logoutbtn.grid(row = 0, column = 8, ipadx = 10)
        
        self.medicine_name_label.grid(row = 1, column = 3,pady = 0, padx = 30)
        self.medicine_category_label.grid(row=1, column = 5, pady = 0, padx = 30)
        
        self.choose_item_label.grid(row=2, column=2, sticky=W+E, pady = 10)
        self.med_name_combo.grid(row=2, column=3,pady = 10)
        self.med_name_combo.current(0)
        self.med_name_combo.bind("<<ComboboxSelected>>" , self.graph1Changed)
        self.cat_name_combo.grid(row=2, column = 5, pady = 10, padx = 30) 
        self.cat_name_combo.current(0)
        self.cat_name_combo.bind("<<ComboboxSelected>>" , self.graph1Changed)
        
        self.sale_in_label.grid(row = 3, column = 1, sticky=W+E, ipady = 5, pady=5)
        self.sale_in_combo.grid(row = 3, column = 2, pady = 5, padx = 30)
        self.sale_in_combo.current(1)  
        self.sale_in_combo.bind("<<ComboboxSelected>>" , self.graph1Changed)
      
        self.from_label.grid(row = 3, column = 5, ipady = 5, padx = 0, pady=5)
        self.From_Cal.grid(row = 3, column = 6, pady = 5, sticky=W)
        self.From_Cal .bind("<<DateEntrySelected>>", self.graph1Changed)
        self.to_label.grid(row = 3, column = 7, ipady = 5, padx = 0, pady=5)
        self.To_Cal.grid(row = 3, column = 8, pady = 0, sticky=W)
        self.To_Cal .bind("<<DateEntrySelected>>", self.graph1Changed)
        
    def graph1Changed(self,eventObject):
        self.med_name = str(self.selected_med.get())
        
        if(self.med_name[0]=='{'):
            self.med_name = self.med_name[1:-1]
        self.dbcursor.execute("select distinct(Category) from medicine where Name = '" + self.med_name +"'")
        self.result = self.dbcursor.fetchall()
        self.category = list(self.result)
        self.cat_name_combo['values'] = self.category
        self.cat_name_combo.current(0)
        
        self.cat_name = str(self.selected_cat.get())
        self.sale_in = str(self.selected_sale_in.get())
        #self.bar2.get_tk_widget().destroy()
        self.ax2.clear()
        
        self.figure2 = plt.Figure(figsize=(6,5), dpi=100)
        self.ax2 = self.figure2.add_subplot(111)
        self.bar2 = FigureCanvasTkAgg(self.figure2, self.window)
        
        self.ax1.clear()
        self.figure1 = plt.Figure(figsize=(6,5), dpi=100)
        self.ax1 = self.figure1.add_subplot(111)
        self.bar1 = FigureCanvasTkAgg(self.figure1, self.window)
        
        self.showGraph1()
        self.showGraph2()
    
    def graph2Changed(self,eventObject):
        
        self.med_name = str(self.selected_med.get())
        self.cat_name = str(self.selected_cat.get())
        print(self.From_Cal.get_date())
        
        #self.bar1.get_tk_widget().destroy()
        self.ax1.clear()
        self.figure1 = plt.Figure(figsize=(6,5), dpi=100)
        self.ax1 = self.figure1.add_subplot(111)
        self.bar1 = FigureCanvasTkAgg(self.figure1, self.window)
        self.showGraph2()
    
    def logout(self):
        self.window.destroy()
        from login import LoginWindow
        LoginWindow()
    
    def home(self):
        from Admin_Panel import AdminPanel
        self.window.destroy()
        AdminPanel(self.username)
    
    def run(self):
        self.window.geometry("1200x720+0+-10")
        self.window.resizable(0,0)
        self.window.mainloop()
        
#ProfitAnalysis = ProfitAnalysis()