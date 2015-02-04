#!/usr/bin/env python

'''---------------------------------------------------------------
| PROGRAM DESCRIPTION:
|`````````````````````````````````````````````````````````````````
| WebScrape is a data mining tool tailored to grabbing professor 
| and comment data from ratemyprofessors.com for later processing.
| Currently, the program scrapes text from a webpage, and acquires
| the professor name. A directory is created and named after the 
| professor in question. Next, the comment section is located, and 
| a file is created for each comment. 
| 
| I am considering using SQLite to manage data going forward.
| Complete implementation of SQLite depends on the results of my 
| own research. 
| 
| See NEXT STEPS section at the bottom of this file for more 
| information regarding future updates.
---------------------------------------------------------------'''

import urllib2
import sqlite3 as lite
import os
import sys
from bs4 import BeautifulSoup

# scrapeData takes a URL as a parameter, scrapes the data
def scrapeData ( url ):

    '''---------------- Begin Variables ----------------'''
    response = False

    # Data Tracking Variables
    handlingProfName = False
    doneWithProfName = False

    handlingComments = False
    doneWithComments = False

    scrapedUnicode = ''

    prev1 = ''
    prev2 = ''
    prev3 = ''

    profName = ''
    fileName = 'Comment'
    fileNumber = 0

    # File object Variable
    f = open('Webscrape.py', 'r')

    # SQLite Variables
    con = None
    '''---------------- End Variables ------------------'''

    # Make a request to the URL provided
    req = urllib2.Request(url)

    try:

        # Attempt to get a response from HTTP server
        response = urllib2.urlopen(req)
        
        # Attempt to create a database
        con = lite.connect ('data.db')

        cur = con.cursor()
        cur.execute ('SELECT SQLITE_VERSION()')

        data = cur.fetchone()

        print ('SQLite version: %s' % data)

    # If this fails, print exception reason
    except urllib2.URLError as urlError:
    	  print (urlError.reason)

    except lite.Error as sqliteError:
        print (sqliteError.reason)
        sys.exit(1)

    # If response was successful...
    if response:

        # Pull the html from response and BS4-ify it
        html = response.read()
        soup = BeautifulSoup(html)

        for string in soup.stripped_strings:

            # Trigger prof name handling
            if string == 'at':
                handlingProfName = True
            
            # Trigger comment handling
            elif string == 'Comment':
                handlingComments = True
                continue

            if handlingProfName:

                # Gather first and last name
                profName = prev3 + ' ' + prev2

                # Set up directory 
                if not os.path.exists(profName):
                    os.makedirs(profName)
                    
                os.chdir(profName)

                # Initialize starting file object
                f = open(fileName + str(fileNumber), 'w')
                
                handlingProfName = False
                doneWithProfName = True
                continue
                     
            elif handlingComments:
                
                # Handle end of comment section
                if string == 'Rate this Professor':
                    handlingComments = False
                    doneWithComments = True
                    f.close()
                    continue
                    
                # Handle end of single comment
                elif string == 'report this rating':
                    
                    # Write data to file
                    f.write( scrapedUnicode.encode( 'utf-8' ))

                    # Reset variable
                    scrapedUnicode = ''
                    
                    # Start working with next file
                    fileNumber += 1
                    f = open( fileName + str(fileNumber), 'w' )
                    continue

                # Handle comment data
                else:
                    # Add data to scrapedUnicode
                    scrapedUnicode += string + '\n'
            
            # Store past strings to accurately acquire profName
            if not handlingProfName and not doneWithProfName:
                prev3 = prev2
                prev2 = prev1
                prev1 = string
            
            if doneWithComments and string == 'Load More':
                print ("There is more data!!")

    # Else, report accordingly
    else:
    	  print ("No response received.")

scrapeData( raw_input( 'Enter a URL: ' ) )


'''---------------------------------------------------------------
| NEXT STEPS (from highest-priority to lowest) :
|`````````````````````````````````````````````````````````````````
| + Gather complete data (not just first 20 entries) 
| + Become OS-agnostic (May already be achieved)
| + Scrape multiple pages in one run
| + Convert to SQLite
| + Support Vector Machine
---------------------------------------------------------------'''

'''---------------------------------------------------------------
| Developed by: Nicholas Rebhun  
| Started: 11/11/2014
| Updated: 02/03/2015
| Version: 0.1.02
---------------------------------------------------------------'''
