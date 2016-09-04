# coding: utf-8

import re
import requests
from pprint import pprint


url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8964'
#r = requests.get(url, verify=False)
#stations = re.findall(r'([A-Z]+)\|([a-z)+)',r.text)
#print stations
#stations = dict(stations)
#print stations
#stations = dict(zip(stations.values(),stations.keys()))
#print stations
#pprint(stations,indent=4)

r = requests.get(url, verify=False)
stations = re.findall(r'([A-Z]+)\|([a-z]+)', r.text)
stations = dict(stations)
stations = dict(zip(stations.values(), stations.keys()))
pprint(stations, indent=4)
