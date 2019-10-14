# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (
                                songplay_id SERIAL PRIMARY KEY, 
                                start_time bigint NOT NULL, 
                                user_id int REFERENCES users (user_id), 
                                level varchar, 
                                song_id varchar REFERENCES songs (song_id), 
                                artist_id varchar REFERENCES artists (artist_id), 
                                session_id int, 
                                location varchar, 
                                user_agent varchar
                                );""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (
                                song_id varchar PRIMARY KEY, 
                                title text NOT NULL, 
                                artist_id varchar REFERENCES artists (artist_id), 
                                year int NOT NULL, 
                                duration float8 NOT NULL
                                );""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (
                                artist_id varchar PRIMARY KEY, 
                                name text NOT NULL, 
                                location varchar, 
                                latitude float8, 
                                longitude float8
                                );""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (
                                _id SERIAL PRIMARY KEY, 
                                start_time bigint NOT NULL, 
                                hour int NOT NULL, 
                                day int NOT NULL, 
                                week int NOT NULL, 
                                month int NOT NULL, 
                                year int NOT NULL, 
                                weekday int NOT NULL
                                );""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (
                                user_id int PRIMARY KEY, 
                                first_name text NOT NULL, 
                                last_name text, 
                                gender char(1) NOT NULL, 
                                level varchar NOT NULL
                                );""")


# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays (
                            start_time, user_id, level, 
                            song_id, artist_id, session_id, location, user_agent) VALUES 
                            (%s, %s, %s, %s, %s, %s, %s, %s)
                            """)

user_table_insert = ("""INSERT INTO users (
                            user_id, first_name, last_name, gender, level) VALUES 
                            (%s, %s, %s, %s, %s) 
                            ON CONFLICT(user_id) 
                            DO UPDATE SET (first_name, last_name, gender, level) = 
                            (EXCLUDED.first_name, EXCLUDED.last_name, EXCLUDED.gender, EXCLUDED.level)
                            """)

song_table_insert = ("""INSERT INTO songs (
                            song_id, title, artist_id, year, duration) VALUES 
                            (%s, %s, %s, %s, %s) ON CONFLICT(song_id) 
                            DO UPDATE SET (title, artist_id, year, duration) = 
                            (EXCLUDED.title, EXCLUDED.artist_id, EXCLUDED.year, EXCLUDED.duration)
                            """)

artist_table_insert = ("""INSERT INTO artists (
                            artist_id, name, location, latitude, longitude) VALUES 
                            (%s, %s, %s, %s, %s) ON CONFLICT(artist_id) 
                            DO UPDATE SET (artist_id, name, location, latitude, longitude) = 
                            (EXCLUDED.artist_id, EXCLUDED.name, EXCLUDED.location, EXCLUDED.latitude, 
                            EXCLUDED.longitude
                            )""")

time_table_insert = ("""INSERT INTO time (
                            start_time, hour, day, week, month, year, weekday) VALUES 
                            (%s, %s, %s, %s, %s, %s, %s)
                            """)

# FIND SONGS

song_select = ("""SELECT    songs.song_id, 
                            songs.artist_id 
                            FROM songs JOIN artists 
                            ON songs.artist_id = artists.artist_id 
                            WHERE songs.title = %s AND artists.name = %s AND songs.duration = %s""")

# QUERY LISTS

create_table_queries = [
    user_table_create,
    artist_table_create,
    song_table_create,
    time_table_create,
    songplay_table_create,
]

drop_table_queries = [
    songplay_table_drop,
    user_table_drop,
    song_table_drop,
    artist_table_drop,
    time_table_drop
]
