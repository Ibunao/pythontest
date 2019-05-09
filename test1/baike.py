import requests

url = 'https://ja.wikipedia.org/wiki/%E7%BE%8E%E8%A1%93%E5%AD%A6%E6%A0%A1'
res = requests.get(url)
print(res.text)