import time
import json
import urllib2

INIT_ST, IDLE_ST, AC_ST, HEATER_ST = range(3)
TICK_PERIOD_CONST = 60
MIN_OFF_STATE = 5


class HVACState:
	'The HVAC state object retrieved from server'
	def __init__(self, heat, cool, fan):
		self.heat = heat
		self.cool = cool
		self.fan = fan
	def toString(self):
		return "Heat: %d Cool: %d Fan: %d" % (self.heat, self.cool, self.fan)

class ACStateMachine:
	'The AC SM'

	def __init__(self):
		self.acState = INIT_ST #or state = INIT_ST?
		self.hvacState = HVACState(0,0,0)
		self.no_ac_count = 0
	
	def getHVACState(self):
		#web blah blah blah
		r = urllib2.urlopen("http://n0owrjuhj8.execute-api.us-west-2.amazonaws.com/test/mydemoresource")
		#syntax to close this?
		#parse blah blah blah
		jsonObj = json.loads(r.read());
		#store into hvacState object
		heat = jsonObj['heat']
		cool = jsonObj['cool']
		fan = jsonObj['fan']
		#return hvacState obj

		#heat = input("Enter heat: ")
		#cool = input ("Enter cool: ")
		#fan = input("Enter fan: ")
		self.hvacState = HVACState(heat, cool, fan) #update this later
		#Also, I assume the previous instance of HVACState is garbage collected in python, so no need to delete it.
	def checkHVAC(self):
		if self.hvacState.heat == 1 and self.hvacState.cool == 1:
			return False
		else:
			return True

	def tick(self):
				#state action
		print self.hvacState.toString()
		if self.acState == INIT_ST:
			print "INIT_ST"
			#GPIO stmts here
		elif self.acState == AC_OFF_ST:
			print "AC_OFF_ST"
			#GPIO
		elif self.acState == AC_ON_ST:
			print "AC_ON_ST"
			#GPIO
		elif self.acState == NO_AC_ST:
			print "NO_AC_ST"
			#GPIO
			self.no_ac_count = self.no_ac_count + 1
		elif self.acState == ERROR_ST:
			#GPIO
			#FIX THIS TO LOOP BACK TO INIT AND RESET hvac/ac State
			raise Exception("Stuck in error state. Implement system reset.")
		else:
			pass
			#error

		#common actions
		self.getHVACState()
		if  not self.checkHVAC():
			#ERROR
			self.acState = ERROR_ST

		#state transition
		if self.acState == INIT_ST or self.acState == AC_OFF_ST:
			if self.hvacState.cool == 1:
				self.acState = AC_ON_ST
			elif self.hvacState.cool == 0:
				self.acState = AC_OFF_ST
			else:
				self.acState = ERROR_ST
		elif self.acState == AC_ON_ST:
			if self.hvacState.cool == 1:
				pass
			elif self.hvacState.cool == 0:
				self.acState = NO_AC_ST
			else:
				self.acState = ERROR_ST	 	
		elif self.acState == NO_AC_ST:
			if self.no_ac_count > 5:
				self.no_ac_count = 0
				if self.hvacState.cool == 1:
					self.acState = AC_ON_ST
				elif self.hvacState.cool == 0:
					self.acState = AC_OFF_ST
				else:
					self.acState = ERROR_ST
			else:
				self.acState = ERROR_ST
		elif self.acState == ERROR_ST:
			pass
		else:
			pass
			#error

#Main method:
#create ACSM obj
#call tick method every minute or so
acSM = ACStateMachine()
while(True):
	acSM.tick()
	time.sleep(TICK_PERIOD_CONST)




