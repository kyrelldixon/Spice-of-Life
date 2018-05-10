import requests
import json

def save_json(data, fname):
  with open('r-listentothis_new.json', 'w') as fname:
    json.dump(data, fname, sort_keys=True, indent=2)

def get_json(fname=None, url=None, headers=None):
  data = None
  
  if fname != None:
    with open(fname, 'r') as f:
      data = json.load(f)

  elif url != None:
    r = requests.get(url, headers=headers)
    data = r.json()
    save_json(data, 'r-listentothis_new.json')

  else:
    print('There is no data.')

  return data

def pretty_print(data):
  counter = 0
  for item in data['data']['children']:
      counter += 1
      print("Title:", item['data']['title'],
            "\nComments:", item['data']['num_comments'])
      print("----")

  print("Number of titles: ", counter)

def main():
  url = 'https://www.reddit.com/r/listentothis/new.json'
  headers = {'user-agent': 'Chrome'}
  data = get_json(url=url, headers=headers)
  pretty_print(data)

if __name__ == '__main__':
  main()
