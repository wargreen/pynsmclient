#! /usr/bin/env python3
#You need pyliblo for Python3 for nsmclient and of course an installed and running non-session-manager
import nsmclient 
from time import sleep
from random import randint

#All capabilities default to False. Just change one value to True if you program can do that.
capabilities = {
	"switch" : False,		#client is capable of responding to multiple `open` messages without restarting
	"dirty" : False, 		#client knows when it has unsaved changes
	"progress" : True,		#client can send progress updates during time-consuming operations
	"message" : True, 		#client can send textual status updates
	"optional-gui" : False,	#client has an optional GUI	
	}
	
def myLoadFunction(pathBeginning, clientId):
	"""Pretend to load a file"""
	return True, "foo.save"

def mySaveFunction(pathBeginning):
	"""Pretend to save a file"""
	if randint(1,5) == 3: #1 in a 5 chance to fail
		return False, " ".join(["/".join([pathBeginning, "foo.save"]), "has failed to save because an RNG went wrong"])
	else:
		return True, "foo.save"	

requiredFunctions = {
	"function_open" : myLoadFunction, #Accept two parameters. Return two values. A bool and a status string. Otherwise you'll get a message that does not help at all: "Exception TypeError: "'NoneType' object is not iterable" in 'liblo._callback' ignored"
	"function_save" : mySaveFunction, #Accept one parameter. Return two values. A bool and a status string. Otherwise you'll get a message that does not help at all: "Exception TypeError: "'NoneType' object is not iterable" in 'liblo._callback' ignored"					
	}

def quitty():
	ourNsmClient.sendStatusMessage("Preparing to quit. Wait for progress to finish")
	#Fake quit process
	ourNsmClient.updateProgress(0.1)
	sleep(0.5)
	ourNsmClient.updateProgress(0.5)
	sleep(0.5)
	ourNsmClient.updateProgress(0.9)
	ourNsmClient.updateProgress(1.0)
	return True

optionalFunctions = {
		"function_quit" : quitty,  #Accept zero parameters. Return True or False
		"function_showGui" : None, #Accept zero parameters. Return True or False
		"function_hideGui" : None, #Accept zero parameters. Return True or False
		"function_sessionIsLoaded" : None, #No return value needed.
		} 

ourNsmClient, process = nsmclient.init(prettyName = "PyNsmTestClient", capabilities = capabilities, requiredFunctions = requiredFunctions, optionalFunctions = optionalFunctions,  sleepValueMs = 100) 
#Direct send only functions for your program.
#ourNsmClient.updateProgress(value from 0.1 to 1.0) #give percentage during load, save and other heavy operations
#ourNsmClient.setDirty(True or False) #Inform NSM of the save status. Are there unsaved changes?

while True:
	process()
