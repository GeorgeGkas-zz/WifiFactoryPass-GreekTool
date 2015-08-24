import fileinput
import os, random 

def get_random_mac():
    # We read the list file and choose a random vendor
    total_bytes = os.stat('ouis.lst').st_size 
    random_point = random.randint(0, total_bytes)
    file = open('ouis.lst')
    file.seek(random_point)
    file.readline() # skip this line to clear the partial line
    line = file.readline()
    mac_vendor = line[0:8] # These are the first three bytes of mac adress
    vendor_info = line[9: -1] # info about the company who owns the vendor
    mac_vendor = mac_vendor.replace(' ',':')
    mac_serial = str()

    # We get the last three bytes randomly
    for byte in range(0,3):
        byte = random.randint(0, 99)
        two_digit = str()
        if 0 <= byte <= 9:
            two_digit = str(random.randint(0, 9)) + str(byte)
        else:
            two_digit = str(byte)
        mac_serial =  mac_serial + ':' + two_digit


    mac_adress = (mac_vendor + mac_serial).replace('[', '').replace('\'', '').replace(']', '')


    mac_info = [mac_adress, vendor_info]
    return mac_info



line_mac = get_random_mac()

