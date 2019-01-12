"""
Purpose:  This file sets the SQL table schema for the pubmed downloader.  It inserts 
the data into a sql database for easy querying, extraction and to prevent redundancies in data.

Author:  Natalie Chun
Created:  12 January 2019
"""

def get_pubmed_table_schema():
    """Table schema for pubmed will supercede the above."""
    
    tables = {}
    
    # table contains articles pulled up based on various search terms
    tables['searchterms'] = """CREATE TABLE IF NOT EXISTS searchterms (
        pmid INTEGER,
        searchterm VARCHAR(100),
        PRIMARY KEY(pmid, searchterm),
        FOREIGN KEY(pmid) REFERENCES pubmeddata(pmid)
    );
    """
    
    # contains all of pubmed meta data for articles
    tables['pubmeddata'] = """CREATE TABLE IF NOT EXISTS pubmeddata (
        pmid INTEGER,
        pubmedarticleset VARCHAR(10),
        pubmedarticle VARCHAR(10),
        medlinecitation VARCHAR(100),
        daterevised VARCHAR(10),
        year INTEGER,
        month INTEGER,
        day INTEGER,
        article VARCHAR(100),
        journal VARCHAR(50),
        issn VARCHAR(10),
        journalissue VARCHAR(10),
        pubdate VARCHAR(10),
        title VARCHAR(100),
        isoabbreviation VARCHAR(50),
        articletitle VARCHAR(100),
        elocationid VARCHAR(20),
        abstract VARCHAR(1000),
        abstracttext VARCHAR(1000),
        authorlist VARCHAR(200),
        author VARCHAR(100),
        lastname VARCHAR(20),
        forename VARCHAR(20),
        initials VARCHAR(5),
        affiliationinfo VARCHAR(30),
        affiliation VARCHAR(50),
        language VARCHAR(5),
        publicationtypelist VARCHAR(10),
        publicationtype VARCHAR(10),
        articledate VARCHAR(10),
        medlinejournalinfo VARCHAR(20),
        country VARCHAR(25),
        medlineta VARCHAR(25),
        nlmuniqueid INTEGER,
        issnlinking VARCHAR(9),
        pubmeddata VARCHAR(20),
        history VARCHAR(10),
        pubmedpubdate VARCHAR(10),
        hour INTEGER,
        minute INTEGER,
        publicationstatus VARCHAR(15),
        articleidlist VARCHAR(10),
        articleid VARCHAR(30),
        PRIMARY KEY (pmid)
    );
    """
    
    return tables

def get_pubmed_table_schema2():
    """Updated table schema for pubmed will supercede the above."""
    
    tables = {}
    
    # table contains articles pulled up based on various search terms
    tables['searchterms'] = """CREATE TABLE IF NOT EXISTS searchterms (
        pmid INTEGER,
        searchterm VARCHAR(100),
        PRIMARY KEY(pmid, searchterm),
        FOREIGN KEY(pmid) REFERENCES pubmeddata(pmid)
    );
    """
    
    # contains all of pubmed meta data for articles
    tables['pubmeddata'] = """CREATE TABLE IF NOT EXISTS pubmeddata (
        pmid INTEGER,
        medlinecitationstat VARCHAR(20),
        medlinecitationowner VARCHAR(10),
        daterevyear INTEGER,
        daterevmonth INTEGER,
        daterevday INTEGER,
        articlepubmodel VARCHAR(100),
        journal VARCHAR(50),
        issn VARCHAR(10),
        journalissuevol INTEGER,
        pubdateyear INTEGER,
        pubdatemonth VARCHAR(3),
        title VARCHAR(100),
        isoabbreviation VARCHAR(50),
        articletitle VARCHAR(100),
        medlinepgn INTEGER,
        elocationidpii VARCHAR(20),
        elocationiddoi VARCHAR(30),
        authorlist VARCHAR(200),
        authoraffiliation VARCHAR(300),
        language VARCHAR(5),
        publicationtype VARCHAR(10),
        articledateyear INTEGER,
        articledatemonth INTEGER,
        articledateday INTEGER,
        medlinejrnlcountry VARCHAR(25),
        medlinejrnlta VARCHAR(25),
        nlmuniqueid INTEGER,
        issnlinking VARCHAR(9),
        publicationstatus VARCHAR(15),
        artidpubmed INTEGER,
        artidpii VARCHAR(30),
        artiddoi VARCHAR(30)
        PRIMARY KEY (pmid)
    );
    """
    
    return tables
