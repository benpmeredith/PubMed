# PubMed

This repository searches pubmed for key search terms related to school violence.
Search term and article ids, and article information are deposited into a sqlite database
that prevents redundancies and entry and makes it easy to query.

Note:  Search term quality can potentially be improved by ensuring that
school is added to every search term so that it is not focused on general behaviors.

## TODO

1. Implement a crontab to run code once a week to search and update database (via Azure?)
2. Develop model for data to identify key terms related to school violence.
3. Identify which articles cite a statistically significant intervention programs related to school violence. Alternatively generate meta data analysis to show share of studies which show a statistically significant effect.
4. Pull out all author names from the data.
