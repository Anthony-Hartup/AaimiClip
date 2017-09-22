## AaimiClipper 0.3
## By Anthony Hartup https://anthscomputercave.com

# This is the GUI-based clipper for the AAIMI Clip system
# It creates a list of URLs and keywords for parsing with the AaimiClip site-search system

# Copyright (C) 2017  Anthony Hartup
## It is part of The AAIMI Project
## https://theaaimiproject.com

###############

# Copyright (C) 2017  Anthony Hartup

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

###############

# Import tkinter graphical library
from tkinter import *

# Import Pyperclip for retrieving URLs from clipboard
#from pyperclip import 
import pyperclip

import os

# Time and date functions
import time, datetime
cd = datetime.date.today()
currentday = cd.strftime("%y_%m_%d")
currenttime = time.strftime("_%H_%M")
time_stamp = currentday + currenttime
      
# Text file to store clipped URLs and details
urls = ("clip_list.txt")

# List of subjects
folder_choices = []

# Use FTP for automatically sending links file to server after modification?
# NOTE that FTP is not secure, I only use this for LAN servers. We're working on a SFTP option now
use_ftp = "no"
ftpuser = ""
password = ""
server_folder = ""
if use_ftp == "yes":
    import getpass
    # Library to sync links file with web server
    from ftplib import FTP
    # Comment out the following four lines to add your ftpuser and password in the variables above instead (Not recommended)
    print("Enter password for FTP account")
    pw = getpass.getpass()
    if len(str(pw)) > 1:
        password = str(pw)



# Send the updated links file to the server
def placeFile(filename):
    if use_ftp == "yes":
        #Start FTP server and change to sync folder:
        ftp = FTP('yourServer')
        ftp.login(user=ftpuser, passwd = password)
        ftp.cwd(server_folder)
        ftp.storbinary('STOR '+filename, open(filename, 'rb'))
        print("Placing " + filename)
        ftp.quit()


# Read main link file and create subject folder list
def load_folders():
    global folder_choices
    t = open(urls, "r")
    # line will be subject, URL, search terms, date
    # Example line: subject1 http://yoursite.html term1_term2_term3 17_09_15_04_31
    for line in t:
        words = line.split(' ') 
        f = words[0]
        if f not in folder_choices:
            folder_choices.append(f)
    t.close()  

# Back up main link file before adding link
def bak():
    p = os.system("COPY aaimi_links.txt aaimi_links_old.txt")
    print(str(p))
    pbak = os.system("COPY clip_list.txt aaimi_links.txt")
    print(str(pbak))

# Append clipboard, folder and keywords to main link file    
def take_link(subject, description):
    global folder_choices
    # Retrieve URL from clipboard
    link = pyperclip.paste()

    # Organize keywords
    desc = description.replace(" ", "_")

    # Add folder, URL and time stamp to create entry
    linktext = subject + " " + link + " " + desc + " " + time_stamp + "\n"

    # Back up files first
    # Back up main link file before removing folders
    bak()
    
    # Append entry to main link file
    t = open(urls, "a")
    t.write(linktext)
    t.close()
    if subject not in folder_choices:
        folder_choices.append(subject)
    print("Sucess")
    placeFile(urls)

load_folders()    

# Build GUI for adding new webpages
class AAIMICLIPPER(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, bg="blue")
        self.master.title("AAIMI Clipper")
        self.pack()
        self.createFields()

    # Create fields and buttons
    def createFields(self):
        self.divider_top = Label(self, bg="maroon4", foreground="white",
                            text="Add URL from clipboard to selected AaimiClip folder with multiple keywords")
        self.divider_top.pack(side="top")
        
        # Folder field
        # Text-based option for entering subject folder name
        self.folder_field = Entry(self, width=30)
        self.folder_field.insert(0, "Enter or choose Folder Name")
        self.folder_field.bind("<3>", self.clear_folder_field)
        self.folder_field.pack(side="left")
        self.folder = StringVar(self.master)
        self.folder.set('Choose Folder')
        # Create drop-down menu with all subject folders
        if len(folder_choices) > 0:
            self.folder_drop = OptionMenu(self, self.folder, *folder_choices)
        else:
            self.folder_drop = OptionMenu(self, self.folder, "None")
        self.folder_drop.pack(side="left")
        self.folder_drop.config(bg="GREEN", foreground="white")

        # Create divider between subject and search term fields
        self.divider = Label(self, bg="blue", foreground="blue",
                            text="Space")
        self.divider.pack(side="left")
        
        #Enter search terms
        self.search_terms_field = Entry(self, width=40)
        self.search_terms_field.insert(0, "Enter keywords with spaces")
        self.search_terms_field.bind("<3>", self.clear_search_field)
        self.search_terms_field.pack(side="left")

        # Create the submit button
        self.add_button = Button(self)
        self.add_button["text"] = "Add"
        self.add_button["foreground"] = "white"
        self.add_button["command"] = self.add_link
        self.add_button["bg"] = "maroon4"
        self.add_button.pack(side="left")


    # Sort folder and keyword fields into AAIMI format
    ## and send to take_link function
    def add_link(self):
        self.folder_choice = self.folder_field.get()
        self.auto_choice = self.folder.get()
        self.terms = self.search_terms_field.get()
        self.chosen_folder = ""
        self.keywords = ""
        self.message = ""
        if self.folder_choice == "Enter or choose Folder Name" and self.auto_choice != "Choose Folder":
            self.chosen_folder = self.auto_choice
        elif self.auto_choice == "Choose Folder" and self.folder_choice != "Enter or choose Folder Name":
            self.chosen_folder = self.folder_choice
        else:
            self.message = "Please choose a folder."
        print(self.chosen_folder)

        if self.terms != "Enter keywords with spaces":
            self.keywords = self.terms
        else:
            self.message = "Please enter some keywords."
        if self.message == "":
            take_link(self.chosen_folder, self.keywords)
            # Comment tthe following line to keep the program open after adding links
            root.destroy()
            
            

    #Remove placeholder in folder field on mouse-click
    def clear_folder_field(self, a):
        self.folder_field.delete(0, END)

    #Remove placeholder in search field on mouse-click
    def clear_search_field(self, a):
        self.search_terms_field.delete(0, END)

root = Tk()
guiWindow = AAIMICLIPPER(master=root)
guiWindow.mainloop()
