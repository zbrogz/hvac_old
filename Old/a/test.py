import urllib2
r = urllib2.urlopen("http://n0owrjuhj8.execute-api.us-west-2.amazonaws.com/test/mydemoresource")
print(r.read())
