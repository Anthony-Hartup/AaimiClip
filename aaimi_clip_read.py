#AaimiClipReader 0.3
# Search and open links from an AaimiClip list
# By Anthony Hartup    https://anthscomputercave.com

# These are the functions used by aaimi_clip_viewer.pyw to search links
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


import webbrowser
import time
import subprocess
import os


# File containing links created by aaimi_clipper.py
link_file = "clip_list.txt"
# Array to hold all links' details from txt file
links = {}
# The subject folder names. These are the distinct sections of the links file chosen from a dropdown menu
folders = []
# Array to store finished search results before writing to HTML
gui_store = []




# Read links text file to populate links dictionary
def convert_to_dict():
    global folders, links
    t = open(link_file)
    t.seek(0)

    # Separate URL from keywords and timestamp
    for line in t:
        # line will be space-separated subject, URL, search terms, date (y_m_d_h_m)
        # Search terms are underscore-separated.
        # Example line: subject1 http://yoursite.html term1_term2_term3 17_09_15_04_31
        words = line.split(' ')
        if len(words) == 4:
            folder = words[0]
            if folder not in folders:
                folders.append(folder)
            add_time = words[3].replace("\n", "") # Define timestamp and remove newline from text
            description = words[2].replace("\n", "") # Define description and remove newline from text
            url = words[1] # Define URL from remaining text
            
            # Combine into library and add library to the relevant section in links dictionary
            new_link = [url, description, add_time]
            if folder not in links:
                links[folder] = []
            links[folder].append(new_link)
    t.close()


# Reload links file after modifying link
def refresh_list():
    links = {}
    folders = []
    convert_to_dict()

# Open URL for link in default browser
def open_web_page(address):
    webbrowser.open(address)


#Search from GUI and return results
def gui_search(cat, *argv):
    relative = {}
    store = []
    
    # Search links for search terms and add to relative dictionary
    ## with the number of search terms matching
    for a in argv:
        count = 0
        finish = len(links[cat]) - 1
        link_count = 0
        while link_count <= finish:
            # Check if search term is in any of the keywords for this entrie
            if a in links[cat][count][1]:
                if links[cat][count][0] not in relative:
                    # Add URL to temporary array if first instance
                    relative[links[cat][count][0]] = 1
                else:
                    # Increment match count if subsequent instance
                    relative[links[cat][count][0]] += 1
            count += 1
            link_count += 1
    rl = len(relative)
    t = ""
    # Order results from temporary array by number of matching search terms and create new array
    while len(store) < rl:
        highest = 0
        for link in relative:
            # Order from highest to lowest number of matches
            if relative[link] >= highest:
                highest = relative[link]
                results = [link, relative[link]]
        # Remove temporary entry        
        relative.pop(results[0])
        # Add to final list
        store.append(results)
            
    # Store results for GUI            
    for i in store:
        c = 0
        for details in links[cat]:
            if i[0] in links[cat][c]:
                det = [links[cat][c][1], links[cat][c][2]]
            c += 1
        d = [i[0], det[0], det[1], i[1]]
        gui_store.append(d)

# Back up main link file before removing folders
def bak():
    p = os.system("COPY aaimi_links.txt aaimi_links_old.txt")
    print(str(p))
    pbak = os.system("COPY clip_list.txt aaimi_links.txt")
    print(str(pbak))
    
# Remove folder at user request
def remove_folder(rem_folder):
    bak()
    place = len(rem_folder)
    old = open(link_file, "r")
    lines = old.readlines()
    old.close()
    new = open(link_file, "w")
    for line in lines:
        if line[:place] != rem_folder:
            new.write(line)

# Rewrite link file from links dictionary
def write_links():
    bak()
    write_count = 0
    test_new = open(link_file, "w")
    for link in links:
        for lt in links[link]:
            # Create space-separated line of text with subject, URL, serarch terms and date
            whole_line = link + " " + lt[0] + " " + lt[1] + " " + lt[2] + "\n" 
            test_new.write(whole_line)
            write_count += 1
        write_count = 0
    test_new.close()
            
        
# Add or remove keywords for specific link
def add_details(fol, linkurl, new_details):
    lib_count = 0
    for lib in links[fol]:
        if links[fol][lib_count][0] == linkurl:
            links[fol][lib_count][1] = new_details
        lib_count += 1
    write_links()    

# Restore last-removed folder
def restore_folder():
    p = os.system("COPY aaimi_links.txt clip_list.txt")
    print(str(p))
    pbak = os.system("COPY aaimi_links_old.txt aaimi_links.txt")
    print(str(pbak))
        
convert_to_dict()
