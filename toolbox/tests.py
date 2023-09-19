from django.test import TestCase
#API测试
import requests

URL = "http://10.23.140.196/NetTrack/GetIpInfo/"
TOKEN = ""
headers = {
    "token": "Bearer " + TOKEN
}
with open('ip_test.txt', 'r') as file:
    ip_addresses = file.readlines()
for ip in ip_addresses:
    ip = ip.strip()
    params = {
        'ip': ip
    }
    response = requests.get(URL, headers=headers, params=params)
    if response.status_code == 200:
        print(response.json())
        print(ip)
    else:
        print(f"Error {response.status_code}: {response.text}")
