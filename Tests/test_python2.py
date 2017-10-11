import urllib2
import json

response = urllib2.urlopen("https://qrdr3yk7s4.execute-api.us-west-2.amazonaws.com/testStage/hvac/testHvacID")
data = json.load(response)   
print data