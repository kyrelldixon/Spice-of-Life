import requests
import json
import pandas as pd
import sqlite3

def save_json(data, fname):
  with open(fname, 'w') as fname:
    json.dump(data, fname, sort_keys=True, indent=2)

def get_json(url, fname=None):
  
  if fname != None:
    try:
      with open(fname, 'r') as f:
        data = json.load(f)
        return data
    except:
      print(f'No file named {fname} found. Fetching data from {url}')

  if url != None:
    headers = {'user-agent': 'Chrome'}
    r = requests.get(url, headers=headers)
    data = r.json()
    return data

def pretty_print(data):
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
  df_data = []
  for item in data['children']:
    post_title = item['data']['title']
    num_comments = item['data']['num_comments']
    url = item['data']['url']
    score = item['data']['score']
    video_title = item['data']['media']['oembed']['title']

    df_data.append([post_title, num_comments, url, score, video_title])

  col_names = ['Post Title', 'Comments', 'URL', 'Score', 'Video Title']
  df = pd.DataFrame(df_data, columns=col_names)
  
  return df

def get_urls(conn=None, df=None):
  '''Gets songs from either a df or the sqlite db'''
  
  if conn is not None:
    c = conn.cursor()
    c.execute('select `url` from songs')
    results = c.fetchall()
    results = [result[0] for result in results]
    return results
  elif df is not None:
    return list(df['URL'])
  else:
    return []

def main():
  url = 'https://www.reddit.com/r/listentothis/new.json'
  fname = 'r-listentothis_new.json'
  
  data = get_json(fname=fname, url=url)
  # save_json(data, fname)
  df = json_to_dataframe(data)
  # pretty_print(data)

  sqlite_file = 'spice_of_life.db'    # name of the sqlite database file

  # Inserting Data into Database
  conn = sqlite3.connect(sqlite_file)
  c = conn.cursor()
  df.to_sql('songs', conn, if_exists='replace', index=False)
  print(get_urls(conn=conn))

  # Committing changes and closing the connection to the database file
  conn.commit()
  conn.close()

if __name__ == '__main__':
  main()
