#!/usr/bin/python
# -*- coding: utf-8 -*-

import zipfile
import sqlite3
import acoustid
import chromaprint
import youtube_dl

filename = './a.m4a'
acoustic_id_api_key = "MZBW9HJUzd"
for score, recording_id, title, artist in acoustid.match(acoustic_id_api_key, filename):
    pass



def main(input_zip):
    # newpipe_db_file = "newpipe.db"
    # query = "select * from streams;"
    #
    # with zipfile.ZipFile(input_zip) as newpipe_zipfile:
    #     newpipe_zipfile.extract(newpipe_db_file, tempfile.gettempdir())
    #
    # conn = create_connection(tempfile.gettempdir() + '/' + newpipe_db_file)
    # if conn is None: exit(-1) # marche pô
    #
    # resources_list = query_sqlite(conn, query)
    # conn.close()
    # for  resource in resources_list:
    #     filename = ytd(resource[3], resource[2])
    filename = './a.m4a'


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print('coucou')
        print(e)
    return conn


def query_sqlite(conn, query):
    """
    Execute a query on a sqlite connection
    :param conn: sqlite3 connection
    :param query: string : sql query
    :return: List of tuples (one by recordset) or None
    """
    list_url = []
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    if len(rows) > 0:
        for row in rows:
            list_url.append(row)
        return list_url
    return None


def ytd(title, url ):
    """
    TO DO les extensions
    :param title:
    :param url:
    :return:
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            # 'preferredquality': '192',
        }],
        'progress_hooks': [download_hook],
        'outtmpl': title + '.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return(title + ".m4a")

def download_hook(d):
    """
    Manages YTDL hooks
    :param d:
    :return:
    """
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
        global output_filename
        output_filename =d['filename']



# To do Itération sur results

# if __name__ == '__main__':
#     # Params
#     input_zip = "NewPipeData-20210215_104140.zip"
#     main(input_zip)