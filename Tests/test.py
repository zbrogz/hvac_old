import urllib.request
import ssl

#ctx = ssl.create_default_context()
#ctx.check_hostname = False
#ctx.verify_mode = ssl.CERT_NONE
r = urllib.request.urlopen("http://qrdr3yk7s4.execute-api.us-west-2.amazonaws.com/testStage/hvac/testHvacID")#, context=ctx)
print(r.read())
#jsonObj = json.loads(r.read());

#import urllib2
#r = urllib2.urlopen("http://n0owrjuhj8.execute-api.us-west-2.amazonaws.com/test/mydemoresource")
#print(r.read())