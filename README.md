## Sparkify ETL Pipelines

### Project Summary

This project contains the database schema and ETL pipeline for analysing the data that is collected on songs and user activity on music streaming app. These pipelines extract the data which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs and transforms them as required for analytics and then loads the data into Postgres in the format that provides an easy way to query the Songs users are listening to.

### Explanation of the files in the repository

#### The Data files inside `data` folder in workspace

**Song Dataset**
Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

    song_data/A/B/C/TRABCEI128F424C983.json

    song_data/A/A/B/TRAABJL12903CDCF1A.json

And below is an example of what a single song file, `TRAABJL12903CDCF1A.json`, looks like.

    {"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

**Log Dataset**
The second dataset consists of activity logs from music streaming.

The log files in the dataset are partitioned by year and month. For example, here are filepaths to two files in this dataset.

    log_data/2018/11/2018-11-12-events.json
    
    log_data/2018/11/2018-11-13-events.json


### The project workspace includes six files:

`test.ipynb` displays the first few rows of each table and allows to check the database.
`create_tables.py` drops and creates tables. Run this file to reset your tables before each time you run your ETL scripts.
`etl.ipynb` reads and processes a single file from song_data and log_data and loads the data into tables. This notebook contains detailed instructions on the ETL process for each of the tables.
`etl.py` reads and processes files from song_data and log_data and loads them into tables. 
`sql_queries.py` contains all sql queries, and is imported into the last three files above.
`README.md` provides discussion on your project.


### Database schema design and ETL pipeline.

The Data modeling is done keeping in mind Postgres as database and the ETL pipeline are build using Python.  The fact and dimension tables schema is mentioned below based on star schema for analytic focus, and the ETL pipeline are written to transfers data from files in two local directories into these tables in Postgres using Python and SQL.

**Schema for Song Play Analysis**
Using the song and log datasets, We create a star schema optimized for queries on song play analysis. This includes the following tables.

**Fact Table**
`songplays` - records in log data associated with song plays i.e. records with page NextSong

| Column  		| Type  				| Unique  	|
|---------------|-----------------------|-----------|
| songplay_id 	| SERIAL PRIMARY KEY  	| Yes 		|
| start_time 	| bigint 				| No 		|
| user_id 		| int 					| No 		|
| level 		| varchar 				| No 		|
| song_id 		| varchar 				| No 		|
| artist_id 	| varchar 				| No 		|
| session_id 	| int 					| No 		|
| location 		| varchar 				| No 		|
| user_agent 	| varchar 				| No 		|

**Dimension Tables**
`users` - users in the app

| Column  		| Type  				| Unique  	|
|---------------|-----------------------|-----------|
| user_id 		| int PRIMARY KEY 		| Yes 		|
| first_name	| text 					| No 		|
| last_name 	| text 					| No 		|
| gender 		| char(1) 				| No 		|
| level 		| varchar 				| No 		|


`songs` - songs in music database

| Column  		| Type  					 | Unique  	|
|---------------|----------------------------|----------|
| song_id 		| varchar PRIMARY KEY		 | Yes 		|
| title 		| text 						 | No 		|
| artist_id 	| varchar 					 | No 		|
| year 			| int 					 	 | No 		|
| duration 		| float8 					 | No 		|


`artists` - artists in music database

| Column  		| Type  					 | Unique  	|
|---------------|----------------------------|----------|
| artist_id 	| varchar PRIMARY KEY 		 | Yes 		|
| name 			| text 						 | No 		|
| location 		| varchar 					 | No 		|
| latitude 		| float8 					 | No 		|
| longitude 	| float8 					 | No 		|


`time` - timestamps of records in songplays broken down into specific units

| Column  		| Type  				| Unique  	|
|---------------|-----------------------|-----------|
| _id 			| SERIAL PRIMARY KEY  	| Yes 		|
| start_time 	| bigint 				| No 		|
| hour 			| int 					| No 		|
| day 			| int 					| No 		|
| week 			| int 					| No 		|
| month 		| int 					| No 		|
| year 			| int 					| No 		|
| weekday 		| int 					| No 		|


### How to run the Python scripts

 1. Launch a terminal
 2. To create the database first run the below command to create your database and tables 
   `python create_tables.py`
 4. To perform the ETL on the data and loading into database run the below command in the terminal 
    `python etl.py`
 5. [Optional] You can run `test.ipynb` to confirm the creation of your tables with the correct columns. Make sure to click "Restart kernel" to close the connection to the database after running this notebook.

**NOTE:** You will not be able to run `test.ipynb`, `etl.ipynb`, or `etl.py` until you have run `create_tables.py` at least once to create the `sparkifydb` database, which these other files connect to.