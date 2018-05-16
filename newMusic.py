import requests
import json
import pandas as pd

def save_json(data, fname):
  with open(fname, 'w') as fname:
    json.dump(data, fname, sort_keys=True, indent=2)

def get_json(url, fname=None):
  
  if fname != None:
    try:
      with open(fname, 'r') as f:
        data = json.load(f)
        data = data['data']
        return data
    except:
      print(f'No file named {fname} found. Fetching data from {url}')

  if url != None:
    headers = {'user-agent': 'Chrome'}
    r = requests.get(url, headers=headers)
    data = r.json()
    data = data['data']
    return data

def pretty_print(data):
  counter = 0
  for item in data['children']:
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

def main():
  url = 'https://www.reddit.com/r/listentothis/new.json'
  fname = 'r-listentothis_new.json'
  
  data = get_json(fname=fname, url=url)
  save_json(data, fname)
  df = json_to_dataframe(data)
  print(df.head())
  # pretty_print(data)

if __name__ == '__main__':
  main()
