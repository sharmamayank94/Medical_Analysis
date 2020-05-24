# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 19:55:47 2020

@author: MAYANK
"""
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from Model import customers_per_medicine_Model
class Customers_Per_Medicine():
    
    def __init__(self, username):
        self.username = username
        self.init_components()
        self.configure_components()
        self.pack_components()
        self.run()
    
    def setmarks(self, rects):
        for rect in rects:
            print(rect.get_width())
            self.ax.annotate('{}'.format(rect.get_width()), 
                             xy = (rect.get_width()+0.5, rect.get_y()+0.25))
            
    def get_customers_per_medicine(self, parameter=1, asc=False):
        self.df = customers_per_medicine_Model.customers_per_medicine()
        
        self.df = self.df.sort_values(by=parameter, ascending=asc)
        
        self.x, self.y = self.df[0], self.df[1]       
        #self.ax.grid(color="green")
        #self.ax.set_position([0.1, 0, 0.9, 1], which = "original")
        self.ax.set_ylim(1,15)
        self.ax.set_ybound(upper = len(self.y), lower = 15)
        
        
       
        bari = self.ax.barh(self.y, self.x, animated=False)
        self.setmarks(bari)
        self.ax.set_xticks(self.x)
        
        #plt.barh(self.y, self.x)
        #plt.show()
    
    def reorder(self, event):
        
        self.ax.clear()
        print(self.optionmenu_var.get())
        print(self.optionmenu_var2.get())
        if self.optionmenu_var2.get()=="Name":
            if(self.optionmenu_var.get()=="Ascending"):
                self.get_customers_per_medicine(1, False)
            else:
                self.get_customers_per_medicine(1, True)
        else:
            if(self.optionmenu_var.get()=="Ascending"):
                self.get_customers_per_medicine(0, False)
            else:
                self.get_customers_per_medicine(0, True)
        
        self.canvas.draw()
        
    def init_components(self):
        self.window = tk.Tk()
        self.option_frame = tk.Frame(self.window)
        self.fig = Figure(figsize=(15,65))
        self.ax = self.fig.add_subplot(111)   
        #self.ax.margins(0.5, -0.2)
        
        #self.ax.set_anchor('SW')
        self.get_customers_per_medicine()
        #self.ax.set_xticks(self.x)
        self.canvas = FigureCanvasTkAgg(self.fig, self.window)
        
        toolbar = NavigationToolbar2Tk(self.canvas, self.window)
        toolbar.draw()
        toolbar.pan()
        
        toolbar.update()
        
        self.optionmenu_var = tk.StringVar()
        self.optionmenu_var2 = tk.StringVar()
        self.optionmenu_var.set("Ascending")
        self.optionmenu_var2.set("Name")
        self.sort_label = tk.Label(self.option_frame, text="Sort by:")
        self.sort_optionmenu = tk.OptionMenu(self.option_frame, self.optionmenu_var, "Ascending", "Descending", command = self.reorder)
        self.sort2_optionmenu = tk.OptionMenu(self.option_frame, self.optionmenu_var2, "Name", "Customer/medicine", command = self.reorder)
        self.head_frame = tk.Frame(self.window)
        self.heading_label = tk.Label(self.head_frame, text="Customers for Each medicine", 
                                      font="Verdana 18 bold", fg="white")
        #self.backbtn = tk.Button(self.head_frame, text="Back", bg="#63D792", fg="white", activebackground="#63D7CC")
        self.homebtn = tk.Button(self.head_frame, text="Home", bg="#D76386", fg="white", activebackground="#D763C2", command = self.home)
        self.logoutbtn = tk.Button(self.head_frame, text="Log Out", bg="#D79F63", fg="white", activebackground="#D77D63", command = self.logout)
        self.username_label = tk.Label(self.window, text="Sort", font="Verdana 12 ")
        
            
    def configure_components(self):
        self.window['bg'] = "white"
        self.head_frame['bg'] = "#7800cf"
        self.heading_label.configure(bg="#7800cf")
        self.option_frame.configure(bg="white")
        self.sort_label.configure(bg="white")
        self.sort_optionmenu.configure(bg="white", relief=tk.GROOVE)
        self.sort2_optionmenu.configure(bg="white", relief=tk.FLAT)
        
    def pack_components(self):
        self.head_frame.pack(fill = tk.BOTH)
        self.logoutbtn.pack(side = tk.RIGHT, ipadx = 10, padx = 10)
        self.homebtn.pack(side = tk.RIGHT, ipadx = 10, padx = 10)
        #self.backbtn.pack(side = tk.RIGHT, ipadx = 10, padx = 10)    
        self.heading_label.pack(side = tk.TOP, padx = (250,0), ipady=20, ipadx = 20)
        self.sort_optionmenu.pack(side = tk.RIGHT, padx = (10, 10), pady=20  )
        self.sort2_optionmenu.pack(side = tk.RIGHT, pady=10)
        self.sort_label.pack(side = tk.RIGHT, padx = 10)
        self.option_frame.pack()
        self.canvas.get_tk_widget().pack(side = tk.BOTTOM, fill = tk.BOTH)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
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
    
    
#loginwindow = Customers_Per_Medicine()