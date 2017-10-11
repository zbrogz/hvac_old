import urllib.request

r = urllib.request.urlopen("https://qrdr3yk7s4.execute-api.us-west-2.amazonaws.com/testStage/hvac/testHvacID")


print(r.read())