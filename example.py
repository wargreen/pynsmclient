#! /usr/bin/env python3
"""
Author: Nils Gey ich@nilsgey.de http://www.nilsgey.de  April 2013.
Non Session Manager Author: Jonathan Moore Liles  <male@tuxfamily.org> http://non.tuxfamily.org/nsm/

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


#You need pyliblo for Python3 for nsmclient and of course an installed and running non-session-manager
import nsmclient 

"""Quick Guide how to get Non Session Manager support in your 
python application.

0) You can try to start your client via the NSM server right now. 
Which will not work: I have planted invalid python variable names in 
this file. Replace them all, make the program runnable at all, and 
you have entered all strictly necessary information.

1) Not so Quick behavior guidelines. These are 
non-negotiable. http://non.tuxfamily.org/nsm/API.html

If you can't  implement them easily consider implementing a special 
session mode.

2) Below are one dictionary with general information about your program
and two blocks of functions. One is mandatory, the other is optional.
See the comments to learn more about what your functions must accept
and return.

3)Change the prettyName string in the call nsmclient.init() call below.
This string is very important and used by NSM to generate your saveFile
names. If you change the prettyName NSM will think this is a different
program. So set it to your real program name and don't worry about 
mutiple instances.

Calling the nsmclient.init() function returns two objects. 
First is the ourNsmClient class. You only need this if you want to send
messages yourself. The functions to be executed directly by the 
program are:
	ourNsmClient.updateProgress(value from 0.1 to 1.0) #give percentage during load, save and other heavy operations
	ourNsmClient.setDirty(True or False) #Inform NSM of the save status. Are there unsaved changes?
	ourNsmClient.sendError(errorCode or String, message string)
	
Second, more important, is the even loop processor that checks for new
messages and queues outgoing ones. See the bottom of this example client
"""

#All capabilities default to False. Just change one value to True if you program can do that.
capabilities = {
	"switch" : False,		#client is capable of responding to multiple `open` messages without restarting
	"dirty" : False, 		#client knows when it has unsaved changes
	"progress" : False,		#client can send progress updates during time-consuming operations
	"message" : False, 		#client can send textual status updates
	"optional-gui" : False,	#client has an optional GUI	
	}

#requiredFunctions
"""
The save function must accept one parameter and the open two: 
First: The beginning of a path. NSM never creates directories or paths.
It is up to you what you do with the path. Append your file 
extension or use it as a directory (the directory approach is 
recommended). You only have to remember your naming scheme and use 
it every time. For example it is save, if your program is in session 
mode, to always just use "receivedPath/session.yourExtension" since 
it will be a unique path. The important part is that the filename, 
once after it was created, must never change again. 

Second: Open must accept a clientId parameter in the second position.
JackPorts must be created only after open was called and prefixed
with this clientId.
Since open can reload other states (Switching clients) this is done
after open, and not through the nsm welcome message.

Open and Save must return two values:
	return Bool,String
Bool is True or False, depending if the open function succeeded or 
not. 

If True: string is just the file name WITHOUT the path. 
It will be extended by nsmclient and a "/path/foo.save successful",
save or open, message will be given out.

If False: string is a message  which will be used to inform nsm and 
the user what exactly went wrong (file unreadable, wrong format 
etc.). Please include all needed information including the full filepath.

Important: Do not register any JACK clients and ports before a file 
was opened. After open you get ourNsmClient.states.clientId which 
must be used as prefix for your jack clients (client, not ports). 
This also enables your application to be used with multiple instances.

Don't ask the user for confirmation or do 
anything that pauses the save process.
"""

	
requiredFunctions = {
	"function_open" : myLoadFunction, #Accept two parameters. Return two values. A bool and a status string. Otherwise you'll get a message that does not help at all: "Exception TypeError: "'NoneType' object is not iterable" in 'liblo._callback' ignored"
	"function_save" : mySaveFunction, #Accept one parameter. Return two values. A bool and a status string. Otherwise you'll get a message that does not help at all: "Exception TypeError: "'NoneType' object is not iterable" in 'liblo._callback' ignored"					
	}


#Optional functions
"""Leave the dict-value as None to ignore the function.

function_quit should be a function that cleans up. Do whatever you 
must do. Shutdown your JACK engine, send a final message to a 
webserver or whatever makes your program special. The program will 
exit anyway, even if you don't implement this extra quit hook. Do 
NOT warn for unsaved changes etc. Quit means quit. No questions asked

function_showGui and function_hideGui will be ignored if you did not 
set "optional-gui" to True in the capabilities dict. If you have an 
optional GUI this enables the session manager to tell your program 
to show and hide your gui. Obviously in this case a hidden Gui 
should not stop the program. If you have, for example, a synthesizer 
with midi in, it should still react and produce sound.

function_sessionIsLoaded": The intent is to signal to 
clients which may have some interdependence (say, peer to peer OSC 
connections) that the session is fully loaded and all their peers 
are available.
Do not use it to auto-connect jack connections. No auto-conncect from
within a session! Jack connections are stored in a seperate NSM client
which belongs to the session.
"""

optionalFunctions = {
		"function_quit" : None,  #Accept zero parameters. Return True or False
		"function_showGui" : None, #Accept zero parameters. Return True or False
		"function_hideGui" : None, #Accept zero parameters. Return True or False
		"function_sessionIsLoaded" : None, #No return value needed.
		} 

ourNsmClient, process = nsmclient.init(prettyName = YourApplicationName, capabilities = capabilities, requiredFunctions = requiredFunctions, optionalFunctions = optionalFunctions,  sleepValueMs = 0) 

#Direct send only functions for your program.
#ourNsmClient.updateProgress(value from 0.1 to 1.0) #give percentage during load, save and other heavy operations
#ourNsmClient.setDirty(True or False) #Inform NSM of the save status. Are there unsaved changes?
#ourNsmClient.sendError(errorCode or String, message string) #for a list of error codes: http://non.tuxfamily.org/nsm/API.html#n:1.2.5.

"""Instead of this while loop, call this function from your own event 
loop. Whatever that might be. A Gui event loop, a python module, or 
indeed a while loop. Don't worry about performance in THIS while 
loop, don't input a sleep value. choose a ms value in the init() 
function.

If you are running this in a Qt timer or similar, good, 
unblocking manner just let sleepValueMs at 0 ms because cpu load management is 
done by another part of the program. sleepValueMs over 0 are just 
for python standalone purposes, instead of a sleep(). 
"""

while True:
	process()
