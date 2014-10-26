#! /usr/bin/python

##########################
# 
# GET VIP SSL ON F5_BIGIP
#
##########################

# Function getting F5 Virtual Server.

def get_VirtualServer_list(F5):
	try:
		return F5.LocalLB.VirtualServer.get_list()
	except	Exception, e:
		print e

# Function getting F5 Virtual Server HTTP Class -- Use F5 Object

def get_all_VirtualServer_VirtualServerHttpClass(F5):
	try:
		VirtualServer = get_VirtualServer_list(F5)
		return VirtualServer, F5.LocalLB.VirtualServer.VirtualServerHttpClass.get_profile_name(VirtualServer)
	except	Exception, e:
		print e

# Function getting F5 VIP -- Use F5 object and VirtualServer 

def get_VirtualServer_destination(F5, VS):
	try:
		return F5.LocalLB.VirtualServer.get_destination([VS])
	except	Exception, e:
		print e

# Main 

if __name__ == "__main__":

''' Import Bigsuds Module / getpass '''
import bigsuds
import getpass

# List of equipement -- Uncomment and change your IP here

# F5_BIGIP_IP_LIST = ['IP']

# Obtain Login of equipement
print "Give your Login of your(s) Equipement(s)",
login = raw_input()

# Obtain password of equipement
print "Give Your Password of your(s) Equipement(s)",
pswd = getpass.getpass() 

# For every equipement we have to connect to the equipement,
# obtain all the VIP SSL

for F5_BIGIP_IP in F5_BIGIP_IP_LIST:
	F5_BIGIP = bigsuds.BIGIP(F5_BIGIP_IP, username = login, password = pswd)
	if  get_VirtualServer_VirtualServerHttpClass(F5_BIGIP) == 'SSL':
	 	print get_VirtualServer_destination(F5_BIGIP)
	else:




