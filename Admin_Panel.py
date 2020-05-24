# -*- coding: utf-8 -*-
"""
Created on Mon May 11 17:10:51 2020

@author: MAYANK
"""

import tkinter as tk
from PIL import ImageTk, Image
from Customers_Per_Medicine import Customers_Per_Medicine
from Medicines_Expiry import Medicines_Expiry
from profitperday import ProfitPerDayAnalysis
from profitanalysis import ProfitAnalysis

class AdminPanel:
    def __init__(self, username):
        self.username = username
        self.init_components()
        self.configure_components()
        self.pack_components()
        self.run()
    
    def open_window(self, window_name):
        if(window_name=="customer"):
            self.window.destroy()
            cpm = Customers_Per_Medicine(self.username)
        elif(window_name == "expiration"):
            self.window.destroy()
            me = Medicines_Expiry(self.username)  
        elif(window_name == "profit"):
            self.window.destroy()
            ProfitPerDayAnalysis(self.username)
        else:
            self.window.destroy()
            ProfitAnalysis(self.username)
            
            
    
    def init_components(self):
        self.window = tk.Tk()
        self.heading_label = tk.Label(self.window, text="Digissist-Analysis",bg="#7800cf", fg = "white", font="Verdana 18 bold")
        self.left_frame = tk.Frame(self.window, bg = "white")
        
        self.image = ImageTk.PhotoImage(Image.open("AdminImage.png"))
        
        self.admin_image_label = tk.Label(self.left_frame,bg = "white", image = self.image)
        self.username_label = tk.Label(self.left_frame, text="Welcome\n\n"+self.username, bg = "white" , font = "Verdana 16 bold")
        
        self.right_frame = tk.Frame(self.window, bg = "white")
        self.right_frame_top = tk.Frame(self.right_frame, bg = "white")
        self.right_frame_bottom = tk.Frame(self.right_frame, bg = "white")
        
        
        self.image_profit = ImageTk.PhotoImage(Image.open("Profit.png").resize((200, 200), Image.ANTIALIAS))
        self.image_sale = ImageTk.PhotoImage(Image.open("Sale.png").resize((200, 200), Image.ANTIALIAS))
        self.image_customers = ImageTk.PhotoImage(Image.open("Customers.png").resize((200, 200), Image.ANTIALIAS))
        self.image_expiration = ImageTk.PhotoImage(Image.open("Expiration.png").resize((200, 200), Image.ANTIALIAS))
        self.profit_analysis = tk.Button(self.right_frame_top, text="Profit Analysis", font = "Verdana 12", bg = "white", compound = tk.BOTTOM, command = lambda:self.open_window("profit"), image = self.image_profit)
        self.sale_analysis = tk.Button(self.right_frame_top,  text="Sales", font = "Verdana 12", bg = "white",compound = tk.BOTTOM, command = lambda:self.open_window("sale"), image = self.image_sale)
        self.customer_analysis = tk.Button(self.right_frame_bottom, text="Popular Medicines", font = "Verdana 12",compound = tk.BOTTOM, bg = "white",command = lambda:self.open_window("customer"), image = self.image_customers)
        self.expiration_analysis = tk.Button(self.right_frame_bottom, text="Expiry Dates", font = "Verdana 12", bg = "white",compound = tk.BOTTOM, command = lambda:self.open_window("expiration"), image = self.image_expiration)
        
    def configure_components(self):
        self.window.configure(bg="white")
    
    def pack_components(self):
        
        self.heading_label.pack(fill = tk.BOTH, ipady = 20)
        self.left_frame.pack(side = tk.LEFT, fill = tk.BOTH, ipadx = 30)
        
        self.admin_image_label.pack()
        self.username_label.pack()
        self.right_frame.pack(fill = tk.BOTH)
        self.right_frame_top.pack(side = tk.TOP)
        self.right_frame_bottom.pack(side = tk.BOTTOM)
        self.profit_analysis.pack(side = tk.LEFT, padx = 20, pady = 20)
        self.sale_analysis.pack(side = tk.RIGHT, padx = 20, pady = 20)
        self.customer_analysis.pack(side = tk.RIGHT, padx = 20, pady = 20)
        self.expiration_analysis.pack(side = tk.LEFT, padx = 20, pady = 20)
       
    
    def run(self):
        self.window.geometry("800x650")
        self.window.mainloop()
        
