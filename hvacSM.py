import time
import json
import urllib.request


# SM states:
IDLE_ST, FAN_ST, AC_ST, HEAT_ST = range(4)


class VirtualState:
    'The HVAC virtual state object'

    def __init__(self, heat, ac, fan, off_time):
        self.heat = heat
        self.ac = ac
        self.fan = fan
        self.off_time = off_time

    def toString(self):
        return "Heat: %s AC: %s Fan: %s, Off_time: %d" % (self.heat, self.ac, self.fan, self.off_time)


class HvacStateMachine:
    def __init__(self):
        self.currentState = IDLE_ST
        self.vState = VirtualState("off", "off", "auto", 0)
        self.off_time = 0

    def setVState(self, v):
        self.vState = v

    def runState(self):
        print(self.currentState)
        print(self.vState.toString())
        if(self.currentState == IDLE_ST):
            # increment off_time
            self.off_time += 1
        elif(self.currentState == FAN_ST):
            self.off_time += 1
        elif(self.currentState == AC_ST):
            pass
        elif(self.currentState == HEAT_ST):
            self.off_time += 1

    def runTransition(self):
        if(self.currentState == IDLE_ST):
            if(self.vState.heat == "on"):
                self.currentState = HEAT_ST
                print("Turning on heat")
                print("Turning on fan")
            elif(self.vState.ac == "on"):
                self.currentState = AC_ST
                print("Turning on ac")
                print("Turning on fan")
            elif(self.vState.fan == "on"):
                self.currentState = FAN_ST
                print("Turning on fan")

        elif(self.currentState == FAN_ST):
            if(self.vState.heat == "on"):
                self.currentState = HEAT_ST
                print("Turning on heat")
            elif(self.vState.ac == "on"):
                self.currentState = AC_ST
                print("Turning on ac")
            elif(self.vState.fan == "auto"):
                self.currentState = IDLE_ST
                print("Turning off fan")

        elif(self.currentState == HEAT_ST):
            if(self.vState.ac == "on"):
                self.currentState = AC_ST
                print("Turning off heat")
                print("Turning on ac")
            elif(self.vState.heat == "off"):
                print("Turning off heat")
                if(self.vState.fan == "on"):
                    self.currentState = FAN_ST
                elif(self.vState.fan == "auto"):
                    self.currentState = IDLE_ST
                    print("Turning off fan")

        elif(self.currentState == AC_ST):
            if(self.vState.heat == "on"):
                self.currentState = HEAT_ST
                print("Turning off ac")
                print("Turning on heat")
            elif(self.vState.ac == "off"):
                print("Turning off ac")
                if(self.vState.fan == "on"):
                    self.currentState = FAN_ST
                elif(self.vState.fan == "auto"):
                    self.currentState = IDLE_ST
                    print("Turning off fan")
