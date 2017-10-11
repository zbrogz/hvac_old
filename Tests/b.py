import urllib3
http = urllib3.PoolManager()
r = http.request('GET', 'https://n0owrjuhj8.execute-api.us-west-2.amazonaws.com/test')
print(r.status)
print(r.data)
