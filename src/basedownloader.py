"""
Purpose:  This class consists of general functions that are useful 
in downloading and storing data from various websites that 
are being scraped.

Author:  Natalie Chun
Created: 22 November 2018
"""

import urllib
import urllib.request
from bs4 import BeautifulSoup
import sys
import pandas as pd
import re
import datetime
import time
import random
import csv
import sqlite3


class BaseDownloader(object):
    """Base code for downloading data from various websites for NSV project.
    """
    
    def __init__(self, db):
        super(BaseDownloader, self).__init__(db)
        self.conn = sqlite3.connect(db)
        self.cursor = conn.cursor()
        self.datecur = datetime.datetime.now()
                
    def _display_db_tables(self):
        query = """SELECT name FROM sqlite_master WHERE type='table';"""
        tablenames = self.cursor.execute(query).fetchall()
        for name in tablenames:
            query = """SELECT * FROM %s;""" % (name)
            temp = pd.read_sql(query, self.conn)
            print("Entries in table %s: %d" % (name[0], len(temp)))
            print(temp.head())
            #query = """SELECT DISTINCT * FROM %s LIMIT 5;""" % (name[0])
            #temp = self.cursor.execute(query).fetchall()
            #print(temp)
                
    def _request_until_succeed(self, url):
        """URL request helper, set to only request a url 5 times before giving up."""
        
        req = urllib.request.Request(url)
        count = 1
        while count <= 5:
            time.sleep(random.randint(3,6))
            try: 
                response = urllib.request.urlopen(req)
                if response.getcode() == 200:
                    return(response)
            except Exception:
                print("Error for URL %s : %s" % (url, datetime.datetime.now()))
            count+=1
        return(None)
        
    def _export_csv_data(self):
        """Export all data in sql into csv files."""
        
        query = """SELECT name FROM sqlite_master WHERE type='table';"""
        tablenames = self.cursor.execute(query).fetchall()
        for name in tablenames:
            query = """SELECT * FROM %s""" % (name)
            chunk_iter = pd.read_sql(query, chunksize=10000)
            for i, chunk in enumerate(chunk_iter):
                mode = 'w' if i == 0 else 'a'
                header = True if i == 0 else False
                chunk.to_csv(os.path.join(self.outdir, '%s.csv' % (name)), mode=mode, header=header, index=False)
     
    def _create_table_schema(self, tables):
        """Generate table schema for database.  If it doesn't currently exist"""

        for t, query in tables.items():
            self.cursor.execute(query)
            self.conn.commit()
        
        # Print out tables in database
        query = """SELECT name FROM sqlite_master WHERE type='table';"""
        tablenames = self.cursor.execute(query).fetchall()
        print(tablenames)
            
    def download_pdf(self, url):
        """Download pdf and save it to a file."""
        
        #page = urllib.request.urlopen('https://journals.sagepub.com/doi/pdf/10.1177/2158244017700460')
        page = requests.get(url)
        with open('./data/pdf/temp.pdf', 'wb') as f:
            f.write(page.content)
            
    def download_page(self, url):
        """Download specific page for parsing."""

        page = urllib.request.urlopen(url)
        # parse the page
        parser = BeautifulSoup(page,'html.parser')
        print(parser)
        #print(parser.find_all('meta'))
        randnum = random.randint(1,5) 
        time.sleep(randnum)
            
    def run_all(self):
        raise NotImplementedError