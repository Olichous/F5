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
    except    Exception, e:
        print e

# Function getting F5 Virtual Server HTTP Class -- Use F5 Object

def get_all_VirtualServer_ProfileType(F5):
    try:
        VirtualServer = get_VirtualServer_list(F5)
        return VirtualServer, F5.LocalLB.VirtualServer.get_profile(VirtualServer)
    except    Exception, e:
        print e

# Function getting F5 VIP -- Use F5 object and VirtualServer 

def get_VirtualServer_destination(F5, VS):
    try:
        return F5.LocalLB.VirtualServer.get_destination([VS])
    except    Exception, e:
        print e

# Main 

if __name__ == "__main__":

    ''' Import Module : Bigsuds (F5 Module) / Getpass (Password) / Socket (DNS) / xlwt (Writing Excel)'''
    import bigsuds
    import getpass
    import socket
    from xlwt import Workbook 

    # List of Equipement -- Put your F5-IP in F5_IP_LIST.txt
    F5_BIGIP_IP_LIST = [line.strip() for line in open('F5_IP_LIST.txt', 'r')]
    print F5_BIGIP_IP_LIST
        
    # Obtain Login of equipement
    print "Give your Login of your(s) Equipement(s)",
    login = raw_input()
    
    # Obtain password of equipement
    print "Give Your Password of your(s) Equipement(s)",
    pswd = getpass.getpass() 
    
    # Create an .xls and a sheet and create 
    book = Workbook()
    feuill1 = book.add_sheet('VIP_SSL')

    # For every equipement we have to connect to the equipement,
    # obtain all the VIP and find all the VIP with a PROFILE_TYPE_CLIENT_SSL activate
    # We put all the VIP SSL in a xls
    # Use var = "to{}to".format(j) with j an integer if you want to put an integer in a string.
    j = 0
    for F5_BIGIP_IP in F5_BIGIP_IP_LIST:
        print " Pour le LB %s = %s \n" %(socket.gethostbyaddr(F5_BIGIP_IP)[0], F5_BIGIP_IP)
        #pswd = "{}wx".format(j+1)
        F5_BIGIP = bigsuds.BIGIP(F5_BIGIP_IP, username = login, password = pswd)
        VS, VS_PROFILE_ATTRIBUTE = get_all_VirtualServer_ProfileType(F5_BIGIP)
        VS_IP = get_VirtualServer_destination(F5_BIGIP, VS)
        feuill1.write(0,j,socket.gethostbyaddr(F5_BIGIP_IP)[0])
        i=0
        for vip in VS_PROFILE_ATTRIBUTE:
            for prof in vip:
                if  prof['profile_type'] == 'PROFILE_TYPE_CLIENT_SSL':
                    print "Cette IP : %s est a checker \n" % VS_IP[i]['address']
                    feuill1.write(i+1,j,VS_IP[i]['address'])    
            i+=1
        j+=1
    book.save('test.xls')
