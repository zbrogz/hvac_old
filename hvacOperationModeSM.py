import time
import json
import urllib.request
import hvacSM


TICK_PERIOD_CONST = 5

# SM states:
SETUP_ST, NORMAL_ST, ERROR_ST = range(3)
OFF_TIME_MIN = 5  # AC off time before it can turn back on

hvac_SM = hvacSM.HvacStateMachine()


class HvacOpModeSM:
    def __init__(self):
        self.currentState = SETUP_ST
        self.vState = hvacSM.VirtualState("off", "off", "auto", 0)
        self.error = False

    def runState(self):
        if(self.currentState == SETUP_ST):
            print("SETUP_ST")
            # Run setup code...
            # pass
        elif self.currentState == NORMAL_ST:
            print("NORMAL_ST")
            # Get the Virtual state from the server
            self.vState = self.getVirtualState()
            if(self.stateIsValid()):
                hvac_SM.setVState(self.vState)
            else:
                self.error = True
                # don't update the virtual state
        elif self.currentState == ERROR_ST:
            print("ERROR_ST")
            self.vState = self.computeState()
            hvac_SM.setVState(self.vState)
            # computeState should ensure it is a valid state

    def runTransition(self):
        if self.currentState == SETUP_ST:
            self.currentState = NORMAL_ST
            # for now just go to the normal state
        elif self.currentState == NORMAL_ST:
            if self.error:
                self.currentState = ERROR_ST
                self.vState = hvacSM.VirtualState("off", "off", "auto", 0)
                hvac_SM.setVState(self.vState)
        elif self.currentState == ERROR_ST:
            pass
            # Stay here until power cycle

    def getVirtualState(self):
        r = urllib.request.urlopen(
            "http://n0owrjuhj8.execute-api.us-west-2.amazonaws.com/test/mydemoresource")
        #hvacState = json.loads(r.read());
        obj = json.loads(r.read().decode("utf-8"))  # .read())
        a = hvacSM.VirtualState(
            obj['heat'], obj["ac"], obj["fan"], obj["off_time"])
        print(a.toString())
        return a

    def computeState(self):

        # eventually this should be its own file with an algorithm for computing the state
        # based on  current temperature and its rate of change. This should only be used when there is a network access error or bad data.
        return hvacSM.VirtualState("off", "off", "auto", 0)

    def stateIsValid(self):
        if(self.vState.ac == "on"):
            if(self.vState.heat == "on"):
                return False
            elif(self.vState.off_time < OFF_TIME_MIN):
                return False
            else:
                return True
        else:
            return True



# Main:
hvacOpModeSM = HvacOpModeSM()
while(True):
    hvacOpModeSM.runState()
    hvacOpModeSM.runTransition()
    # OpModeSM should update the VState in hvacSM
    hvac_SM.runState()
    hvac_SM.runTransition()
    time.sleep(TICK_PERIOD_CONST)
