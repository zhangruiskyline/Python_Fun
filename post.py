import requests
url = 'http://127.0.0.1:5000/login'
resp = requests.post(url, data={}, auth=('user', 'pass'))
print resp
