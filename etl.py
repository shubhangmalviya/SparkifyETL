import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import datetime


def process_song_file(cur, filepath):
    '''
    Responsible for processing a single song file and inserting the song and artist records into the table.

    :param cur: the cursor for inserting the song table records
    :param filepath: the directory file path for song data
    :return: no return type
    '''
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert artist record
    artist_data = list(df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', \
                           'artist_longitude']].values[0])
    cur.execute(artist_table_insert, artist_data)

    # insert song record
    song_data = list(df[["song_id", "title", "artist_id", "year", "duration"]].values[0])
    cur.execute(song_table_insert, song_data)


def process_log_file(cur, filepath):
    '''
    Responsible for processing a single log file and inserting the records into the time, users and song play tables.

    :param cur: the cursor for inserting the time, users and song play records
    :param filepath: the directory file path for log data.
    :return: no return type
    '''

    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = df['ts'].apply(lambda x: datetime.datetime.fromtimestamp(x / 1000))

    # insert time data records
    loadTimeData(cur, df, t)

    # load user table
    loadUserData(cur, df)

    # insert songplay records
    loadSongPlayData(cur, df)


def loadSongPlayData(cur, df):
    '''
    Responsible for loading the data into the SongPlay table
    
    :param cur: the database cursor
    :param df: The dataframe object containing log file filtered on Next song
    :return: nothing
    '''
    
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId,
                         row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def loadUserData(cur, df):
    '''
    Responsible for loading the data into the UserData table.
    
    :param cur: the database cursor
    :param df: The dataframe object containing log file filtered on Next song
    :return: nothing
    '''
    
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)


def loadTimeData(cur, df, t):
    '''
    Reponsible for loading the data into the time data table.
    
    :param cur: the database cursor
    :param df: The dataframe object containing log file filtered on Next song
    :param t: the time series converting the timestamp column to the date time.
    :return: nothing
    '''
    
    time_data = (df['ts'], t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))


def process_data(cur, conn, filepath, func):
    '''
    Responsible for scanning the directories and processing all the files in them.

    :param cur: the cursor responsible for inserting the records.
    :param conn: the database connection
    :param filepath: the directory file path of the data.
    :param func: the callback function responsible for processing a single file.
    :return: no return type
    '''

    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    '''
    Entry point of the program and responsible for initiating the process of ETL.

    :return: no return type
    '''
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()