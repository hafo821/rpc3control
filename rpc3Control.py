#!/usr/bin/python

'''

Control Class for the Baytech RPC3 
J. Adams <jna@retina.net>

'''

from pexpect import *
import sys

class rpc3ControlError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class rpc3Control:
    ''' Class to control a Baytech RPC-3   '''

    child = None

    def __init__(self, hostname, user=None, password=None):
        self.hostname = hostname
        self.connect()

        '''
        the RPC supports username, or password, or both 
        so we support both of those cases in this code. 
        '''

        if user != None:
            self.child.expect("Enter username>")
            self.child.send("%s\r" % user)

        if password != None:
            self.child.expect("Enter password>")
            self.child.send("%s\r" % password)
        
    def connect(self):
        if self.child == None:
            self.child = spawn("telnet " + self.hostname)
            ''' todo; implement login and an option for it. I assume you have logins disabled for now. '''

# Uncomment the next line for debuggin
#            self.child.logfile = sys.stdout

    def outlet(self,outlet_number,state):
        '''
        control an outlet 
        state is one of "on","off",or "reboot"
        outlet_number is an integer. 
        '''

        if state not in ("on", "off", "reboot"):
            raise rpc3ControlError('Invalid outlet state')

        if int(outlet_number) > 8 or int(outlet_number) < 1:
            return None
        
        self.child.expect("Enter Selection>")
	self.child.send("1\r")
        self.child.expect("RPC-3>")

        self.child.send("%s %d\r"  % (state, outlet_number) )

        self.child.send("Y\r")
        self.child.expect("RPC-3>")

        self.child.send("MENU\r")

        return True

    def outlet_status(self, outlet_number):
        ''' Get the status table for an outlet '''

        if int(outlet_number) > 8 or int(outlet_number) < 1:
            return None

        self.child.expect("Enter Selection>")
	self.child.send("1\r")

        self.child.expect("RPC-3>")
        self.child.send("MENU\r")

        # parse the output
        inlist = False
        status = {}

        for line in self.child.before.split('\n'):
            if line.rstrip() == "" and inlist:
                inlist = False

            if inlist:
                words = line.split()
                if words[3] == "On":
                    status[int(words[0])] = True
                else:
                    status[int(words[0])] = False

            if line.find("Status") != -1:
                inlist = True

        return status[outlet_number]







