import requests
from config.public_data import *
from utils.ParseExcel import ParseExcel
import json
import os
import hashlib

print ("register------")
data = json.dumps({'username': 'lily', 'password': 'wcx123wac', 'email': 'lily@qq.com'}) #
r = requests.post('http://39.106.41.11:8080/register/', data= data)
print(r.status_code)
print(r.text)
res_body = r.json()
if res_body["code"] == "00":
    print("用户注册成功！")
else:
    print("用户注册失败！")
