import requests

url = 'http://localhost:8080/2015-03-31/functions/function/invocations'
# data = {"key": "value"}
# response = requests.post(url, data=data)
#
#
# print(response.text)

payload = {'key1': 'value1', 'key2': 'value2'}

r = requests.post('https://httpbin.org/post', json=payload)
print(r.json())