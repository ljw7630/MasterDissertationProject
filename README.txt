- html_downloader.py
	Download some linkedIn public profiles using Google Search
	
- html_parser.py
	Parse a public profile and return all content of interest

- schema_generator.py
    Generate class and property definitions, and some instances of 'constants'

- rdf_generator.py
    Generate the actual rdf triples from personal and company public profiles.
	
- utils.py
	Common utility methods.

- models.py
	dummpy class for transfer objects

- socket_handler.py
	send and receive message from and to Java Lucene text search engine

- db_helper.py
	connect to database, methods for db manipulation

- profile_cleaner.py
	clean profile to remove useless data

- query_measure.py
	measure the performance of the query


./resources
	- Irish_Boys_Names.htm  
		A list of common Irish boys name that can be used at the starting point
	- Irish_Boys_Names.htm  
		A list of common Irish boys name that can be used at the starting point

./user_raw
	Raw html files that download by html_downloader.py that need to be processed

./company_raw
	Raw html files that downloaded by html_downloader.py

./result
    folder for output files

./jar
	jar files for Lucene text search engine

./website
	the evaluation websites