import requests
from bs4 import BeautifulSoup
import json
import datetime

headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'
}

def main():
  with open('Free_Proxy_List_copy.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    f = open('result_copy.txt','w')

    f.write('<============= Start =================>\n')
    f.write(f" {datetime.datetime.now()}")
    f.write("\n\n")

    for item in data:

      proxies = {
        'http': f"{item['protocols'][0]}://{item['ip']}:{item['port']}",
        'https': f"{item['protocols'][0]}://{item['ip']}:{item['port']}",
      }
      
      try:
        response = requests.get(url='https://2ip.ru', headers=headers, proxies=proxies)

        if response.status_code == 200:
          print(f"Success to connect to {proxies['http']}. In process ... .")

          soup = BeautifulSoup(response.text, 'lxml')
          ip = soup.find('div', id='d_clip_button').find('span').text.strip()

          f.write(f" IP: {item['ip']}\n")
          f.write(f" Protocol: {item['protocols'][0]}\n")
          f.write(f" Port: {item['port']}\n")
          f.write(f" IP on site: {ip}\n")

      except requests.exceptions.ConnectionError:
        print(f"Failed to connect to {proxies['http']}. Skipping.")
        continue

      f.write("\n\n")
      f.write(f" {datetime.datetime.now()}\n")
      f.write('<============= End =================>\n\n')
      f.close()

if __name__ == '__main__':
  main()