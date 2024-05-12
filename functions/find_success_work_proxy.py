import requests
from bs4 import BeautifulSoup
import json
import datetime

from variables.common import path_to_proxy_list, path_to_success_work_proxy, url_check_ip

def find_success_work_proxy():
  with open(path_to_proxy_list, 'r', encoding='utf-8') as f:
    
    data = json.load(f)

    f = open(path_to_success_work_proxy, 'w')

    f.write('<============= Start =================>\n')
    f.write(f" {datetime.datetime.now()}")
    f.write("\n\n")

    for item in data:

      proxies = {
        'http': f"{item['protocols'][0]}://{item['ip']}:{item['port']}",
        'https': f"{item['protocols'][0]}://{item['ip']}:{item['port']}",
      }

      try:
        response = requests.get(url=url_check_ip, proxies=proxies)

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
