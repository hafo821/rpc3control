#!/usr/bin/env python 

"""

control_outlet.py
Perform actions on an outlet. 

J. Adams <jna@retina.net>

"""
import syslog
 
from rpc3Control import *
from ping import * 

UPLINK="75.101.56.3"
RPC=None
RPCUSER=None
RPCPASS=None
TIMEOUT=5

def usage():
    print "\nUsage: %s outlet_number (on|off|reboot|status)\n" % sys.argv[0]
    sys.exit(1)

(RPC, RPCUSER, RPCPASS) = load_credentials()

# sanity check
if len(sys.argv) != 3:
    usage()

outlet = int(sys.argv[1])
state  = sys.argv[2]

if (outlet < 1 or outlet > 8) or (state not in ['on','off','reboot','status']):
    usage()

r = rpc3Control(RPC, RPCUSER, RPCPASS, False)
if state == 'status':
    print r.outlet_status(outlet)
else:
    r.outlet(outlet, state)