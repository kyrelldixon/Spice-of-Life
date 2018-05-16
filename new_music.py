'''
This application requires you to have youtube-dl installed in order to
actually download songs. Otherwise, it just stores the songs
'''

import json
import sqlite3
import subprocess
import requests
import pandas as pd

def save_json(data, fname):
  '''Saves json to a file'''
  with open(fname, 'w') as fname:
    json.dump(data, fname, sort_keys=True, indent=2)

def get_json(url, fname=None):
  '''Gets json from file or requests from url'''
  if fname != None:
    try:
      with open(fname, 'r') as f:
        data = json.load(f)
        return data
    except IOError:
      print(f'No file named {fname} found. Fetching data from {url}')

  if url != None:
    headers = {'user-agent': 'Chrome'}
    r = requests.get(url, headers=headers)
    data = r.json()
    return data

def pretty_print(data):
  '''Prints out data nicely formatted'''
  counter = 0
  for item in data['data']['children']:
    counter += 1
    print("Post Title:", item['data']['title'],
          "\nComments:", item['data']['num_comments'],
          "\nURL:", item['data']['url'],
          "\nScore:", item['data']['score'],
          "\nVideo Title:", item['data']['media']['oembed']['title'],
         )
    print("----")

  print("Number of titles: ", counter)

def json_to_dataframe(data):
  '''Extracts most relevant data from json and stores in a Dataframe'''
  df_data = []
  for item in data['children']:
    post_title = item['data']['title']
    num_comments = item['data']['num_comments']
    url = item['data']['url']
    score = item['data']['score']
    video_title = item['data']['media']['oembed']['title']
    artist = extract_artist(video_title)
    provider = item['data']['media']['oembed']['provider_name']
    song_title = extract_song_title(video_title)

    df_data.append([post_title, num_comments, url, score, video_title, song_title, artist, provider])

  col_names = ['Post Title', 'Comments', 'URL', 'Score', 'Video Title', 'Song Title', 'Artist', 'Provider']
  df = pd.DataFrame(df_data, columns=col_names)
  return df

def get_db_urls(conn):
  '''Gets songs from the sqlite db'''
  if conn is not None:
    c = conn.cursor()
    c.execute('select `url` from songs')
    results = c.fetchall()
    results = [result[0] for result in results]
    return results
  else:
    return []

def download(url, output_dir=None):
    '''Downloads youtube audio as mp3'''
    if output_dir is None:
      output_dir = "'./songs/%(title)s.%(ext)s'"
    args = f'youtube-dl -x --audio-format mp3 {url} -o {output_dir}'
    subprocess.call(args, shell=True)

def extract_song_title(video_title):
  '''Uses black magic to extract song title from video title'''
  if '-' not in video_title:
    return video_title
  
  # Split on hyphen gets the song part. The second split
  # makes a list containing each word. The " ".join puts
  # the word back together with a space in between
  song_title = " ".join(video_title.split('-')[1].split())
  return song_title

def extract_artist(video_title):
  '''Extracts artist from video title if artist is present'''
  if '-' not in video_title:
    return None

  artist = " ".join(video_title.split('-')[0].split())
  return artist  

def main():
  '''Runs the script'''
  url = 'https://www.reddit.com/r/listentothis/new.json'
  fname = 'r-listentothis_new.json'

  data = get_json(fname=fname, url=url)
  df = json_to_dataframe(data)
  # pretty_print(data)

  sqlite_file = 'spice_of_life.db'

  # Inserting Data into Database
  conn = sqlite3.connect(sqlite_file)
  c = conn.cursor()
  df.to_sql('songs', conn, if_exists='replace', index=False) # replacing for now, but I may want to append

  # Committing changes and closing the connection to the database file
  conn.commit()
  c.close()
  conn.close()

if __name__ == '__main__':
  main()
