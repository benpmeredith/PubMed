"""
Purpose:  This file creates a scraper for PubMed.  It downloads the data and deposits them
into a SQL database for easier extraction.

Author:  Natalie Chun
Created: 17 Nov 2018
Updated: 12 Jan 2019  
"""

import pandas as pd
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import time
import random
import re
import requests
import unicodedata
import csv
import os
import xml.etree.ElementTree as ET
from config import FileConfig
from basedownloader import BaseDownloader
from table_schema import get_pubmed_table_schema
import sqlite3

class PubMedDownloader(BaseDownloader):
    """Class for downloading PubMed Abstracts and Article Names based on key search terms.  
    Currently initialized with key words related to school violence.
    Note:  The downloader stores files in csv with key search term appended.
    """
    
    # pmid is a PubMed ID
    # url is the url of the PubMed web page
    # search_term is the string used in the search box on the PubMed website
    def __init__(self, debug=False):
        self.url = "http://www.ncbi.nlm.nih.gov/pubmed/"
        self.entrezurl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # open csv file for search terms
        df = pd.read_csv(os.path.join(FileConfig.RAWDIR, "searchterms.csv"), encoding="ISO-8859-1")
        self.kws = list(set(df['keyword']))
        print("Keyword terms to search: %s" % (self.kws))
    
        self.outdir = os.path.join(FileConfig.EXTDIR, 'pubmed')
        # open the pubmed sql database
        self.conn = sqlite3.connect(os.path.join(self.outdir, 'pubmed.db'))
        self.cursor = self.conn.cursor()
        # create table schema
        self._create_table_schema(get_pubmed_table_schema())
        self.debug=debug

    def graph_searchterms(self):
        """Graph search terms in the database."""
        
        query = """SELECT DISTINCT * FROM searchterms;"""
        df = pd.read_sql(query, self.conn)
        query = """SELECT DISTINCT pmid FROM searchterms;"""
        num_articles = len(pd.read_sql(query, self.conn))
        
        df['cnt'] = 1
        temp = df.groupby(['searchterm'])['cnt'].sum()
        print(temp)
        temp.sort_values(inplace=True)
        ax = temp.plot(kind='barh', figsize=(8, 10), color='blue', zorder=2, width=0.85)
      
        ax.set_xlabel("Counts", labelpad=20, weight='bold', size=12)
        ax.set_ylabel("Search term", labelpad=20, weight='bold', size=12)
        plt.title("No School Violence Articles in PubMed\nTotal unique articles: %s" % (num_articles))
        plt.show()
        
    def search_page(self, searchterm):
        """Get search results from pubmed for particular search term.
        Note:  Only use if the entrez page does not work
        """
        
        url = self.url + '?term=%s&cmd=DetailsSearch' % (searchterm)
        print(url)
        page = urllib.request.urlopen(url)
        parser = BeautifulSoup(page,'html.parser')
        randnum = random.randint(3,10) 
        time.sleep(randnum)
        self.parse_search_page(parser)
        
    def parse_search_page(self, parser):
        """Parses general page of pubmed and insert into database.
        TODO:  Search multiple pages (right now only gets first page)
        need to return
        Note:  No need to use.
        """
        
        data = []
        
        # parse one page of results
        results = parser.find_all('div', {'class':'rslt'})
        for res in results:
            #print(res)
            tempdata = {}
            temp = res.find('p', {'class':'title'})
            print(temp)
            tempdata['title'] = temp.text
            tempdata['href'] = temp.find('a',{'href':True})['href']
            tempdata['desc'] = res.find('p',{'class':'desc'}).text
            temp = res.find('p',{'class':'details'})
            tempdata['jrnl'] = temp.text
            if tempdata['title'] != '':
                cols = []
                for key, value in tempdata.items():
                    cols.append(value.strip('\n'))
                data.append(cols)
                print(data)
        
        with open(self.outdir + 'pubmed-%s.csv' % (self.date), 'w', newline='') as f:
            w = csv.writer(f, delimiter=',')
            w.writerow(['title','href','desc','details'])
            for d in data:
                w.writerow(d)
                
        # get the next page
    
    def search_entrez(self, searchterm, retmax=20):
        """Entrez is the API call that makes it easier to retrieve information from PubMed. 
        Fair use policy entails waiting at least 3 seconds to make a new call.
        """
        print("Downloading: %s" % (searchterm))
        # use keyword term that requires both words to show up in article for it to be relevant
        srch = '{}%5BKYWD%5D'.format(searchterm.replace(' ','%2B'))
        
        url = self.entrezurl + 'esearch.fcgi?db=pubmed&term=%s&retmax=%d' % (srch, retmax)
        page = urllib.request.urlopen(url)
        #print(page)
        parser = BeautifulSoup(page,'html.parser')
        #print(parser)
        ids = parser.find_all('id')
        data = []
        cols = ['PMID', 'PubmedArticleSet', 'PubmedArticle', 'MedlineCitation', 'DateRevised', 
                'Year', 'Month', 'Day', 'Article', 'Journal', 'ISSN', 'JournalIssue', 'PubDate', 
                'Title', 'ISOAbbreviation', 'ArticleTitle', 'ELocationID', 'Abstract', 'AbstractText',
                'AuthorList', 'Author', 'LastName', 'ForeName', 'Initials', 'AffiliationInfo', 'Affiliation', 
                'Language', 'PublicationTypeList', 'PublicationType', 'ArticleDate', 'MedlineJournalInfo',
                'Country', 'MedlineTA', 'NlmUniqueID', 'ISSNLinking', 'PubmedData', 'History', 'PubMedPubDate',
                'Hour', 'Minute', 'PublicationStatus', 'ArticleIdList', 'ArticleId']
  
        # get the new pubmed ids and insert into database
        for i in ids:
            query = """INSERT OR IGNORE INTO searchterms (pmid, searchterm) VALUES (?, ?);""" 
            row = [i.text, searchterm]
            self.cursor.execute(query, row)
        self.conn.commit() 
        
        # query existing pubmed database to get new pubmed articles to insert into database
        query = """SELECT DISTINCT pmid FROM searchterms WHERE pmid NOT IN (SELECT pmid FROM pubmeddata WHERE searchterm == '%s');""" % (searchterm)
        ids = pd.read_sql(query, self.conn)
        query = """SELECT DISTINCT * FROM pubmeddata;"""
        pubmeddata = pd.read_sql(query, self.conn)
        pubmedcols = ','.join(list(pubmeddata.columns))
        valcols = ','.join(['?' for i, col in enumerate(pubmeddata.columns)])
        print("Number of new articles to query for search term %s: %d" % (searchterm, len(ids)))
        
        for cnt, uid in enumerate(ids['pmid']):
            if cnt % 10 == 0:
                print("Number of summaries downloaded: %d" % (cnt))
            tempdata = self.clean_xml_abstract_page(uid)
            coldata = [tempdata[col] if col in tempdata else '' for col in cols]
            query = """INSERT OR IGNORE INTO pubmeddata (%s) VALUES(%s)""" % (pubmedcols, valcols)
            self.cursor.execute(query, coldata)
            self.conn.commit()
            time.sleep(3)
        
    def clean_xml_abstract_page(self, uid):
        """Clean XML node for Entrez abstract page.  These pages provide a fairly complete list of variables
        on each type of publication."""
        
        url = self.entrezurl + 'efetch.fcgi?db=pubmed&id=%s&rettype=abstract&retmode=XML' % (uid)
        page = urllib.request.urlopen(url)
        tree = ET.parse(page)
        root = tree.getroot()
        data = {}
        for elem in root.iter():
            if elem.tag != '':
                if elem.text is not None:
                    if elem.tag in ['ArticleTitle','AbstractText']:
                        data[elem.tag] = elem.text.strip('\n ').encode('ascii','ignore')
                    else:
                        data[elem.tag] = elem.text.strip('\n ')
                    
        #print(data)
        return(data)
        
    def download_entrez_summary(self, uid):
        """This downloads individual entrez summaries based on the UID.
        This page contains easily parsable information, but lacks detail of the abstract page.  
        Therefore this function may not be very useful for collecting data, but could collect certain type 
        of information faster than for the abstract which uses xml parsing."""
        
        url = self.entrezurl + 'esummary.fcgi?db=pubmed&id=%s' % (uid)
        page = urllib.request.urlopen(url)
        #print(page)
        parser = BeautifulSoup(page,'html.parser')
        #print(parser)
        
        # parse the entrez summary
        items = parser.find_all('item')
        data = {}
        data['id'] = uid
        for item in items:
             data[item['name']] = item.text
        time.sleep(3)
        headers = data.keys()
        return(list(headers), list(data.values()))
    
    def run_all_kws(self):
        """Run and download articles for all kws.  Max out at 1000 article per term."""
        
        numsearch = 10 if self.debug else 1000
        self._display_db_tables()
        for i, kw in enumerate(self.kws):
            if self.debug and i > 0:
                break
            self.search_entrez(kw, numsearch)
        self._display_db_tables()
        self.graph_searchterms()
        self._export_csv_data()
        self.conn.close()
        
if __name__ == "__main__":

    debug = False
    pm = PubMedDownloader(debug=debug)
    pm.run_all_kws()
