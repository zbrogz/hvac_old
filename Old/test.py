import requests

r = requests.get('https://n0owrjuhj8.execute-api.us-west-2.amazonaws.com/test')
print(r.text)