from django.test import TestCase
import requests
import time
#API测试
URL = "http://10.23.140.196/NetTrack/GetIpInfo/"
TOKEN = "634e0b664736d85c7fc22fef00fe99df2d315630"
headers = {
    "token": "Bearer " + TOKEN
}
with open('ip_test.txt', 'r') as file:
    ip_addresses = file.readlines()
with open('error.txt','w') as outfile:
    for ip in ip_addresses:
        ip = ip.strip()
        params = {
            'ip': ip
        }
        start_time = time.time()
        response = requests.get(URL, headers=headers, params=params)
        end_time = time.time()
        print(f" {end_time - start_time:.2f} seconds")
        if response.status_code == 200:
            outfile.write(ip + ":")
            outfile.write(response.json()['data']['prefix_description']['value'] + " " + response.json()['data']['site']['value']+'\n')
            print(response.json()['data']['prefix_description']['value']+response.json()['data']['site']['value'])

        else:
            outfile.write(f"'Error'{response.status_code}: {response.text}")

