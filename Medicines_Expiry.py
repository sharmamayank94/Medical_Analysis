# -*- coding: utf-8 -*-
"""
Created on Sun May 10 19:35:47 2020

@author: MAYANK
"""
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from Model.Medicines_Expiry_Model import get_Medicines_Expiry_Dates
from tkcalendar import Calendar 
import datetime
#from Admin_Panel import AdminPanel

class Medicines_Expiry:
    def __init__(self, username):
        self.username = username
        self.init_components()
        self.configure_components()
        self.pack_components()
        self.run()
    
    def show_calendar(self, parameter):
        self.date_Picker = Calendar(self.frame,
                   font="Arial 14", selectmode='day',
                   cursor="hand1", year=2018, month=2, day=5)
    
    def show_annotations(self, rects, j):
        for i in range(len(self.dfn[0])):              
            self.ax.annotate('{}'.format(self.dfn[j][i]), 
                                 xy = (rects[i].get_x()+0.05, (rects[i].get_height()/2 +self.bottom[i]-1.5)), size=12, color = "white")
           
       
            
    def plot_data(self):
        startdate = datetime.date(int(self.from_date.get()[0:4]), int(self.from_date.get()[5:7]), int(self.from_date.get()[8:]))
        enddate = datetime.date(int(self.to_date.get()[0:4]), int(self.to_date.get()[5:7]), int(self.to_date.get()[8:]))
        
        self.data = get_Medicines_Expiry_Dates(startdate, enddate)
        
        framecount = self.data[2].value_counts().max()
        self.dfn = []
        dfs = []
        copy = False
        
        start = 0
        for i in range(framecount):
            if copy==False: 
                temp = [self.data[1][i]]    
                temp2 = [self.data[0][i]]
            else:
                temp = [0]
                temp2 = [""]
                
            self.dfn.append(temp2)
            dfs.append(temp)
            
            if i+1==framecount:
                break
            
            elif(copy==False and self.data[2][i]!=self.data[2][i+1]):
                start = i+1
                copy = True  
        
        
        
        i=start
       
        while (i < len(self.data[1])):
            
          
            z = 0
            copy = True
            while(z<framecount):
                temp = dfs[z]
                temp2 = self.dfn[z]
                if copy==False:
                    temp.append(0)
                    temp2.append("")
                    z+=1
                    continue
                
                
                if i+z+1<len(self.data[1]) and self.data[2][i+z]==self.data[2][i+z+1]:
                    temp.append(self.data[1][i+z])
                    temp2.append(self.data[0][i+z])
                
                else:    
                   
                    temp.append(self.data[1][i+z])
                    temp2.append(self.data[0][i+z])
                    i += z+1
                    copy = False
                
               
                z+=1
           
     
        self.data = self.data.drop_duplicates(2, keep = "first")
       
        columnlen = len(self.data[0])
        self.bottom = [0 for i in range(columnlen)]
        
        self.bar = self.ax.bar(self.data[2].astype(str).values, dfs[0], zorder = 3)
        self.show_annotations(self.bar, 0)
        for j in range(columnlen):
            self.bottom[j]+=dfs[0][j]
        
        
        for i in range(1, framecount):
            self.bar = self.ax.bar(self.data[2].astype(str).values, dfs[i], bottom = self.bottom, zorder = 3)
            self.show_annotations(self.bar, i)
            for j in range(columnlen):
                self.bottom[j]+=dfs[i][j]
            
        
        
        
        
        '''self.data2 = self.data.copy(deep = True)
        for key, col in enumerate(self.data[1]):
            self.data2.loc[key, 1] = col+25;
        
        self.ax.bar(self.data2[2].astype(str).values, self.data2[1], bottom = self.data[1])
        self.ax.set_xticks(self.data[2].astype(str).values)'''
        self.ax.set_xlim(0, 8)
        self.ax.set_xbound(lower = -0.5, upper = 7.5)
        self.ax.set_facecolor("white")
        self.ax.grid("green",  zorder = 0)
        self.ax.set_ylabel('Medicines left (Cumulative)')
        self.ax.set_xlabel('Expiry Dates')
        self.ax.tick_params(axis='x', rotation=75)
       
        self.canvas.draw()
        
    
    def init_date_placeholder(self):
        self.from_date.set("yyyy-mm-dd")
        self.to_date.set("yyyy-mm-dd")
    
    def remove_placeholder(self, evt):
        if str(evt.widget)== '.!frame.!entry':
            self.from_entry.select_range(0, tk.END)
        else:
            self.to_entry.select_range(0, tk.END)
                
    def set_date(self, evt):
        if str(evt.widget)== '.!frame.!entry':
            if(self.from_date.get()==""):
                self.from_date.set("yyyy-mm-dd")
        else:
            if(self.to_date.get()==""):
                self.to_date.set("yyyy-mm-dd")
        
    def init_components(self):
        self.window = tk.Tk()
        self.head_frame = tk.Frame(self.window)
        self.heading_label = tk.Label(self.head_frame, text="Medicines Expiration", 
                                      font="Verdana 18 bold", fg="white")
        #self.backbtn = tk.Button(self.head_frame, text="Back", bg="#63D792", fg="white", activebackground="#63D7CC")
        self.homebtn = tk.Button(self.head_frame, text="Home", bg="#D76386", fg="white", activebackground="#D763C2", command = self.home)
        self.logoutbtn = tk.Button(self.head_frame, text="Log Out", bg="#D79F63", fg="white", activebackground="#D77D63", command = self.logout)
        self.username_label = tk.Label(self.window, text="Sort", font="Verdana 12 ")
        
        self.frame = tk.Frame(self.window)
        self.from_Label = tk.Label(self.frame, text="From: ", bg="white", font="Verdana 14")
        self.from_date = tk.StringVar()
        self.from_entry = tk.Entry(self.frame, bg="#525252", fg="white", font="Verdana 14 italic", text=self.from_date)
        self.to_date = tk.StringVar()
        self.init_date_placeholder() 
        self.to_Label = tk.Label(self.frame, text="To: ", bg="white", font="Verdana 14")
        self.to_entry = tk.Entry(self.frame, bg="#525252", fg="white", font="Verdana 14 italic", text=self.to_date)
        self.go_Button = tk.Button(self.frame, text="Go", bg="#24a7ed", fg="white", font="Verdana 12 bold", command = self.plot_data)
        self.from_entry.bind('<FocusIn>', self.remove_placeholder)
        self.to_entry.bind('<FocusIn>', self.remove_placeholder)                        
        self.from_entry.bind('<FocusOut>', self.set_date)
        self.to_entry.bind('<FocusOut>', self.set_date)                        
        self.fig = Figure(figsize=(20,20))
        self.ax = self.fig.add_subplot(111)
        #self.plot_data()
        self.canvas = FigureCanvasTkAgg(self.fig, self.window)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.window)
        self.toolbar.pan()
        self.toolbar.update()
        
    def configure_components(self):
        self.window['bg'] = "white"
        self.head_frame['bg'] = "#7800cf"
        self.heading_label.configure(bg="#7800cf", fg="white", font="Verdana 18 bold")
        self.frame['bg'] = "white"
        
                                   
                               
    def pack_components(self):
        self.head_frame.pack(fill = tk.BOTH)
        self.logoutbtn.pack(side = tk.RIGHT, ipadx = 10, padx = 10)
        self.homebtn.pack(side = tk.RIGHT, ipadx = 10, padx = 10)
        #self.backbtn.pack(side = tk.RIGHT, ipadx = 10, padx = 10)    
        self.heading_label.pack(side = tk.TOP, padx = (250,0), ipady=20, ipadx = 20)
        self.from_Label.pack(side=tk.LEFT, padx = 10, pady = 10)
        self.from_entry.pack(side = tk.LEFT, padx = 10, pady = 10)
        self.to_Label.pack(side=tk.LEFT, padx = 10, pady = 10)
        self.to_entry.pack(side=tk.LEFT, padx = 10, pady = 10)
        self.go_Button.pack(side=tk.LEFT, padx = 10, pady = 10, ipadx = 20)
        self.frame.pack()
        self.canvas.get_tk_widget().pack()
    
    def logout(self):
        self.window.destroy()
        from login import LoginWindow
        LoginWindow()
    
    def home(self):
        self.window.destroy()
        from Admin_Panel import AdminPanel
        AdminPanel(self.username)
    
    def run(self):
        self.window.geometry("1200x800")
        self.window.mainloop()

#me = Medicines_Expiry()        