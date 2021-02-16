#!/usr/bin/python
# -*- coding: utf-8 -*-

import zipfile
import sqlite3
import tempfile
import youtube_dl
import musicbrainzngs

# Params
input_zip = "NewPipeData-20210215_104140.zip"
newpipe_db_file = "newpipe.db"
query = "select * from streams;" # à virer plus tard
# Global variable use to get downloaded file name
output_filename = ''


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


# def extract_zip(input_zip, name):
#     input_zip = zipfile.ZipFile(input_zip)
#     return {name: input_zip.read(name) for name in input_zip.namelist()}

def download_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
        global output_filename
        output_filename =d['filename']


"""
query = "select * from streams;"
with zipfile.ZipFile(input_zip) as newpipe_zipfile:
    newpipe_zipfile.extract(newpipe_db_file, tempfile.gettempdir())

conn = create_connection(tempfile.gettempdir() + '/' + newpipe_db_file)
if conn is None: exit(-1) # marche pô

result = query_sqlite(conn, query)
print('coucou')
print(result)
conn.close()
"""

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
       # 'preferredquality': '192',
    }],
    'progress_hooks': [download_hook],
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    # ydl.download([result[0][2]])
    ydl.download(['https://www.youtube.com/watch?v=1kKk2qshv5Q'])
#     dl_info = ydl.extract_info(
#         'https://www.youtube.com/watch?v=1kKk2qshv5Q', download=False
#   )
# dl_file = dl_info['title']+'.mp3'
output_filename = output_filename[:-3]+'mp3'
print(output_filename)

# idée récupérer le nom de fichier à partir du tuple récupéré lors de la requête.
def download(self, filename, directory, url):
    ydl_opts = {
        "format": "best",
        "outtmpl": str(directory / (filename + ".%(ext)s")),
        "progress_hooks": [self._hook],
        "playlistend": 1,
        "nooverwrites": True,
        "quiet": True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

