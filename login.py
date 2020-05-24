# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 17:09:25 2020

@author: MAYANK
"""
import tkinter as tk
from Model import Login_Model
import Admin_Panel

class LoginWindow():
    def __init__(self):
        self.init_components()
        self.configure_components()
        self.pack_components()
        self.run()
    
    def init_components(self):
        self.window = tk.Tk()
        self.warning = tk.StringVar()
        self.warning.set('')
        self.heading_label = tk.Label(self.window, text="Welcome to Medical Analysis Application", font="Verdana 18 bold", fg="white")
        self.username_label = tk.Label(self.window, text="Username:", font="Verdana 12 ")
        self.password_label = tk.Label(self.window, text="Password:", font="Verdana 12 ")
        self.warning_label = tk.Label(self.window, textvariable = self.warning)
        self.username_field = tk.Entry(self.window)
        self.password_field = tk.Entry(self.window, show = '*')
        self.login_button = tk.Button(self.window, text="Login", command = self.login)
        
    def login(self):
        username = self.username_field.get()
        password = self.password_field.get()
        
        isVerified = Login_Model.login(username, password)
             
        if isVerified is True:
            self.window.destroy()
            am = Admin_Panel.AdminPanel(username)            
            
        else:
            self.warning.set("You've entered incorrect username or password")
        
    def configure_components(self):
        self.window.configure(bg="#d7eaf5")
        self.heading_label.configure(bg="#0064de")                      
        self.password_label.configure(bg="#d7eaf5")
        self.username_label.configure(bg="#d7eaf5")
        self.warning_label.configure(bg="#d7eaf5", fg="red")
        
        
    def pack_components(self):
        self.heading_label.grid(row = 0, column = 0, columnspan = 2, ipady=20, ipadx = 20, pady=(0, 50))
        self.username_label.grid(row = 1, column = 0, ipady = 5, padx = 30, sticky = "e")
        self.username_field.grid(row = 1, column = 1, pady = 5, padx = 30, sticky = "w")
        self.password_label.grid(row = 2, column = 0, ipady = 5, padx = 30, sticky = "e")
        self.password_field.grid(row = 2, column = 1, pady = 5, padx = 30, sticky = "w")
        self.warning_label.grid(row = 3, column = 0, columnspan = 2, pady = 10)
        self.login_button.grid(row = 4, column = 0, columnspan = 2, pady = (20, 0))
        
        
    def run(self):
        self.window.geometry("590x300")
        self.window.mainloop()
    
