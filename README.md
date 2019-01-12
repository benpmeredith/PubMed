# PubMed

This repository searches pubmed for key search terms related to school violence.
Search term and article ids, and article information are deposited into a sqlite database
that prevents redundancies and entry and makes it easy to query.

Note:  It may be useful to improve the quality of search terms in particular ensuring that
school is added to every search term so that it is not focused on general behaviors.

## TODO

1. Implement a crontab to run code once a week to search and update database (via Azure?)
2. Generate EDA or graphical files to get counts of terms for search terms
3. Process data  
