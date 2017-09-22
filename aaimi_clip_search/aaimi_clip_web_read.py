#!/bin/bash

#AaimiClip Web Reader
# By Anthony Hartup   https://anthscomputercave.com

# Site-search system parses site-lists created by the AaimiClip Clipper

## Part of The AAIMI Project
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

import sys
import time
import subprocess

# Text file that stores clipped URLs and their details
link_file = "clip_list.txt"
# Array to store contents of link file
links = {}
# Holder for search results
gui_store = []

# Reply to send to browser via PHP
send = ""


# Read link_file to populate links dictionary
def convert_to_dict():
    global links
    t = open(link_file)
    t.seek(0)

    # Separate URL from keywords and timestamp
    for line in t:
        # line will be subject folder, URL, search terms, date(y_m_d_h_m)
        # Example line: subject1 http://yoursite.html term1_term2_term3 17_09_15_04_31
        words = line.split(' ')
        folder = words[0]
        add_time = words[3].replace("\n", "") # Define timestamp and remove from text
        description = words[2].replace("\n", "") # Define description and remove from text
        url = words[1] # Define URL from remaining text
        
        # Combine into library and add library to the relevant section in links dictionary
        new_link = [url, description, add_time]
        # Add subject folder in not already in links array
        if folder not in links:
            links[folder] = []
        # Add URL entry 
        links[folder].append(new_link)
    t.close()

# Reload links file
def refresh_list():
    links = {}
    convert_to_dict()


##################################################################################
# Prepare search results for browser
def search_results(term_num):
    global gui_store, send
    # Print results to canvas in order of relevance
    # term_num is number of search terms provided by browser
    count = 0
    result_count = len(gui_store)
    # Write heading before results
    # Change to plural if not 1    
    if result_count == 1:
        heading = " Result"
    else:
        heading = " Results"
    # Prepend number to heading HTML
    beginning = "<h2>" + str(result_count) + heading + "</h2>"
    send += beginning
    # Write HTML for each entry
    for i in gui_store:
        url = gui_store[count][0]
        # Display search terms for url
        sterms = gui_store[count][1]
        
        # Split time from date-stamp
        stamp = gui_store[count][2]
        date_stamp = stamp[:8]
        time_s = stamp[9:]
        time_stamp = time_s.replace("_", ":")

        # Define rating color according to number of matching keywords
        ## Green is "all matched", blue is "some matched"
        rating = gui_store[count][3]        
        rating_col = "gray"
        # If any search terms match
        if rating > 0:
            # Change result color to green if all search terms match
            if rating == term_num:
                rating_col = "green"
            # Change result color to maroon if some search terms match
            else:
                rating_col = "maroon"
        # Replace the underscores dividing search terms with spaces
        fsterms = sterms.replace("_", " ")
        # Write HTML for this entry with the number of matches, all of its search terms and a link to the URL
        senditem2 = "<p class='searchtermline' style='word-wrap:break-word;font-size:1.2em;'><span style='color:" + rating_col + ";'>" + str(rating) + "__</span>" + fsterms + " " + str(date_stamp) + "</p>"
        send += senditem2                
        senditem = "<p style='word-wrap:break-word;font-size:1em;'><a style='font-size:1em;' class='urlline' href='" + url + "' target='_blank'>" + url + "</a></p><p>__________________</p>"
        # Add HTML to response for PHP
        send += senditem
        count += 1       
    gui_store = []


#Search from GUI and prepare results
def site_search(cat, *argv):
    global gui_store
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
    # Arrange results from temporary array by number of matching search terms and create new array
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
            
    # Load global list ready for writing search results to HTML           
    for i in store:
        c = 0
        for details in links[cat]:
            if i[0] in links[cat][c]:
                det = [links[cat][c][1], links[cat][c][2]]
            c += 1
        d = [i[0], det[0], det[1], i[1]]
        gui_store.append(d)
    # Write the HTML
    search_results(len(argv))


def readweb():
    # Read subject folder and search terms from browser and search for entries
    if len(sys.argv) > 1:
        subject_folder = sys.argv[1]
        arg_count = 2
        kwords = []
        while arg_count < len(sys.argv):
            kwords.append(sys.argv[arg_count])
            arg_count += 1
        if len(kwords) > 0:
            site_search(subject_folder, *kwords)
            return send
        else:
            print("No search terms given")
            

convert_to_dict()
readweb()

