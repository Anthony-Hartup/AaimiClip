## AaimiClipViewer 0.3
## By Anthony Hartup https://anthscomputercave.com

#Copyright (C) 2017  Anthony Hartup

## This is the GUI viewer for the AAIMI Clip system
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

# Import AAIMI search and sorting functions
import aaimi_clip_read as clip


url_buttons = []
choices = {}
mod_choices = {}
q_length = 0

# GUI window
class AAIMICLIP(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, bg="green")
        self.master.title("AAIMI Clip Viewer")
        self.pack()
        self.width = 900
        self.height = 700
        self.c = Canvas(self.master, width=self.width, height=self.height, scrollregion=(0,0,800,4000))
        self.scrollbar = Scrollbar(self.master)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.c.config(yscrollcommand=self.scrollbar.set)
        self.c.create_line(0, 25, 900, 25,
                           fill="green", width=8)
        self.scrollbar.config(command=self.c.yview)
        
        # Handle mouse-click events on canvas to select web pages
        def callback(event):
            global status
            zone = [0, 0]
            zone[0] = event.x
            zone[1] = event.y
            
            # Check to see if one of the circles was clicked
            for u in choices:
                if zone[0] in range(choices[u][0], choices[u][2]) and zone[1] in range(choices[u][1], choices[u][3]):
                    clip.open_web_page(u)
                elif zone[0] in range(mod_choices[u][0], mod_choices[u][2]) and zone[1] in range(mod_choices[u][1], mod_choices[u][3]):
                    self.create_mod_fields(u)
        self.c.bind("<Button-1>", callback)
        self.c.pack()
        self.createFields()

    # Activate window to modify details for a url        
    def create_mod_fields(self, target_url):
        self.t = Toplevel(self)
        self.t.wm_title("Modify Links")
        self.mod_keywords = ""
        self.turl = target_url

        # Folder choice
        self.mod_folder = StringVar(self.master)
        self.mod_folder.set('Choose Folder')
        self.mod_folder_drop = OptionMenu(self.t, self.folder, *clip.folders)
        self.mod_folder_drop.pack(side="left")
        self.mod_folder_drop.config(bg="GREEN", foreground="white")
        self.mod_divider = Label(self.t, bg="green", foreground="green",
                            text="SpaceLabel")
        self.mod_divider.pack(side="left")

        # Search field
        count = 0
        self.modf = self.folder.get()
        for x in clip.links[self.modf]:
            if x[0] == target_url:
                
                self.mod_keywords = x[1]
        self.mod_field = Entry(self.t, width=60)
        self.mod_field.insert(0, self.mod_keywords)
        self.mod_field.bind("<3>", self.clear_field)
        self.mod_field.pack(side="left")
        self.mod_button = Button(self.t)
        self.mod_button["text"] = "Change"
        self.mod_button["foreground"] = "white"
        self.mod_button["command"] = self.change_details
        self.mod_button["bg"] = "blue"
        self.mod_button.pack(side="left")


# Modify detail for URL (Clicked from canvas)
    def change_details(self):
        newdet = self.mod_field.get()
        clip.add_details(self.modf, self.turl, newdet)
        
        self.t.destroy()

    # Create search fields, menus and buttons
    def createFields(self):

        # Folder choice
        self.folder = StringVar(self.master)
        self.folder.set('Choose Folder')
        if len(clip.folders) > 0:
            self.folder_drop = OptionMenu(self, self.folder, *clip.folders)
        else:
            self.folder_drop = OptionMenu(self, self.folder, "None")
        self.folder_drop.pack(side="left")
        self.folder_drop.config(bg="GREEN", foreground="white")
        self.menu = self.folder_drop.children["menu"]
        self.divider = Label(self, bg="green", foreground="green",
                            text="SpaceLabel")
        self.divider.pack(side="left")

        # Search field
        self.search_field = Entry(self, width=60)
        self.search_field.insert(0, "Enter keywords with spaces")
        self.search_field.bind("<3>", self.clear_field)
        self.search_field.pack(side="left")
        self.search_button = Button(self)
        self.search_button["text"] = "Search"
        self.search_button["foreground"] = "white"
        self.search_button["command"] = self.search
        self.search_button["bg"] = "blue"
        self.search_button.pack(side="left")

        # Clear search results
        self.clear_button = Button(self)
        self.clear_button["text"] = "Clear"
        self.clear_button["command"] = self.new_search
        self.clear_button["bg"] = "maroon4"
        self.clear_button["foreground"] = "white"
        self.clear_button.pack(side="left")
        self.divider2 = Label(self, bg="green", foreground="green",
                            text="SpaceLabel")
        self.divider2.pack(side="left")

        # Remove selected folder from links file
        self.remove = StringVar(self.master)
        self.remove.set('Remove Folder')
        if len(clip.folders) > 0:
            self.remove_drop = OptionMenu(self, self.remove, *clip.folders)
        else:
            self.remove_drop = OptionMenu(self, self.remove, "None")
        self.remove_drop.pack(side="left")
        self.remove_drop.config(bg="red", foreground="white")
        self.menu2 = self.remove_drop.children["menu"]
        self.remove_button = Button(self)
        self.remove_button["text"] = "Remove"
        self.remove_button["foreground"] = "white"
        self.remove_button["command"] = self.remove_fold
        self.remove_button["bg"] = "red"
        self.remove_button.pack(side="left")

        #Restore last deleted folder
        self.restore_button = Button(self)
        self.restore_button["text"] = "Undo"
        self.restore_button["foreground"] = "white"
        self.restore_button["command"] = self.restore_fold
        self.restore_button["bg"] = "maroon4"
        self.restore_button.pack(side="left")


    #Remove placeholder in search field on mouse-click
    def clear_field(self, a):
        self.search_field.delete(0, END)


    # Clear previous results and refresh canvas
    def new_search(self):
        global choices
        choices = {}
        self.c.delete(ALL)
        self.c.create_line(0, 25, 800, 25,
                           fill="green", width=8)

    # Remove an unwanted file from AAIMI link list
    def remove_fold(self):
        self.rem_fold = self.remove.get()
        clip.remove_folder(self.rem_fold)
        self.menu.delete(self.rem_fold)
        self.menu2.delete(self.rem_fold)

    # Restore last-deleted folder to AAIMI link list and return to drop-down menus
    def restore_fold(self):
        clip.restore_folder()
        self.folder_drop.pack_forget()
        self.divider.pack_forget()
        self.search_field.pack_forget()
        self.search_button.pack_forget()
        self.clear_button.pack_forget()
        self.divider2.pack_forget()
        self.remove_drop.pack_forget()
        self.remove_button.pack_forget()
        self.restore_button.pack_forget()
        self.createFields()

    #Perform a search based on folder-choice and search terms
    def search(self):
        global q_length, choices
        choices = {}
        self.c.delete(ALL)
        self.c.create_line(0, 25, 900, 25,
                           fill="green", width=8)
        self.target_folder = self.folder.get()
        self.terms = self.search_field.get()
        self.sorted_terms = []
        word = ""
        letter_count = 1


        # Prepare search terms to send to AAIMI ClipRead
        for l in self.terms:

            # Split overall search text into individual words
            if l != " " and l != "\n":
                word += l
            else:
                self.sorted_terms.append(word)
                if letter_count < len(self.terms):
                    word = ""
            letter_count += 1
        self.sorted_terms.append(word)
        q_length = len(self.sorted_terms)


        # Send the search to AAIMI ClipRead    
        if self.target_folder != "Choose Folder" and self.terms != "Enter keywords with spaces":
            clip.gui_search(self.target_folder, *self.sorted_terms)
            self.text_height = 100
            self.text_width = 100
            self.icon_width = 50
            self.modification_icon_width = 20
            count = 0
            results_sum = len(clip.gui_store)
            results_heading = str(results_sum) + " Results"
            self.c.create_text(50, 55,
                               fill="green", anchor="w", font=("Arial", 16), text=results_heading)

            # Print results to canvas in order of relevance
            for i in clip.gui_store:
                self.url = clip.gui_store[count][0]

                # Set clickable positions for web icons
                pos = [self.icon_width - 8, self.text_height - 8,self.icon_width + 8, self.text_height + 8]
                choices[self.url] = pos

                # Set clickable positions for modification icons
                modpos = [self.modification_icon_width - 8, self.text_height - 8, self.modification_icon_width + 8, self.text_height + 8]
                mod_choices[self.url] = modpos

                # Split time from date-stamp
                stamp = clip.gui_store[count][2]
                date_stamp = stamp[:8]
                time_s = stamp[9:]
                time_stamp = time_s.replace("_", ":")

                # Define rating color according to number of matching keywords
                ## Green is "all matched", blue is "some matched"
                rating = clip.gui_store[count][3]
                rating_col = "gray"
                if rating > 0:
                    if rating == q_length:
                        rating_col = "green"
                    else:
                        rating_col = "blue"

                # Draw icons, rating-number, URLs, keywords, date and time
                self.c.create_oval(self.icon_width - 10, self.text_height - 10,self.icon_width + 10, self.text_height + 10, 
                                   fill=rating_col)
                self.c.create_rectangle(self.modification_icon_width - 10, self.text_height - 10,self.modification_icon_width + 10, self.text_height + 10, 
                                   fill="maroon4")
                self.c.create_text(self.icon_width + 20, self.text_height,
                                   fill=rating_col, anchor="w", font=("Arial", 16), text=rating)

                self.c.create_text(self.text_width, self.text_height,
                                   fill=rating_col, anchor="w", text=self.url)
                self.text_height += 20
                url_details = clip.gui_store[count][1] + "    ||    " + date_stamp + "    ||      " + time_stamp
                self.c.create_text(self.text_width, self.text_height,
                                   anchor="w", text=url_details)
                self.text_height += 35
                count += 1
            clip.gui_store = []                

                
        else:
            # Warn that fields are missing
            print("Missing fields")
            t_height = 100
            if self.target_folder == "Choose Folder":
                self.c.create_text(100, t_height,
                                   text="Choose Folder", anchor="w", fill="maroon4", font=("Arial", 16))
                t_height += 50
            if self.terms == "Enter keywords with spaces":
                self.c.create_text(100, t_height,
                                   text="Enter one or more keywords above or leave the field empty (right-click inside field)", anchor="w", fill="maroon4", font=("Arial", 16))
            

root = Tk()
guiWindow = AAIMICLIP(master=root)
guiWindow.mainloop()
