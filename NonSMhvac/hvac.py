#import urllib.request
import urllib2
import json
import time

OFF_TIME_MIN = 5

error = False


class HvacState:
    'The HVAC state object'

    def __init__(self, heat, ac, fan, off_time):
        self.heat = heat
        self.ac = ac
        self.fan = fan
        self.off_time = off_time

    def toString(self):
        return "Heat: %s AC: %s Fan: %s Off_time: %d" % (self.heat, self.ac, self.fan, self.off_time)


def getState():
    #r = urllib.request.urlopen("http://n0owrjuhj8.execute-api.us-west-2.amazonaws.com/test/mydemoresource")
    r = urllib2.urlopen(
        "http://n0owrjuhj8.execute-api.us-west-2.amazonaws.com/test/mydemoresource")
    obj = json.loads(r.read())
    # print(obj['ac'])
    return HvacState(obj['heat'], obj["ac"], obj["fan"], obj["off_time"])


def computeState():
    # eventually this should be its own file with an algorithm for computing the state
    # based on  current temperature and its rate of change. This should only be used when there is a network access error or bad data.
    pass


def checkState(next_state):
    if(next_state.heat == "on"):
        if(next_state.ac == "on"):
            error = True
        elif(next_state.off_time < OFF_TIME_MIN):
            error = True
        else:
            pass
            #error = False
    else:
        pass
        #error = False


current_state = HvacState("off", "off", "auto", 0)
while(True):
    next_state = getState()
    checkState(next_state)
    if(error):
        next_state = computeState
    error = False

    if current_state.ac != next_state.ac:
        if next_state.ac == "on":
            print("AC turning on")
        elif next_state.ac == "off":
            print("AC turning off")
        else:
            print("Error")

    if current_state.heat != next_state.heat
        if next_state.heat == "on":
            print("Heat turning on")
        elif next_state.heat == "off":
            print ("Heat turning off")
        else:
            print("Error")

    if current_state.fan != next_state.fan
        if next_state.fan == "on"
            print("Fan turning on")
        elif next_state.fan == "auto" and next_state.heat == "off"

    # if current_state.fan
    # finish fan logic

    current_state = next_state
    print(current_state.toString())
    time.sleep(5)
