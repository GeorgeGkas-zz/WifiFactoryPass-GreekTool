import subprocess
import os
import commands
import time
import re
import fileinput

from threading import Thread
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMainWindow
from asa import Ui_Main_window


class RetardedKill(Thread):
    def __init__ (self, prog, sec):
        Thread.__init__(self)
        self.prog = prog
        self.sec  = sec

    def run(self):
        time.sleep(self.sec)
        status = commands.getstatusoutput("killall " + self.prog)
        if status[0] != 0: 
            print status
            print 'Something went wrong when try to stop the process ' + self.prog
        else:
            print self.prog + ' stoped successfully'

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



def install_aircrack():
    print "Aircrack suit isn't installed in our machine."
    print "Now we are going to install aircrack-ng"
    status = commands.getstatusoutput('apt-get install aircrack-ng') 
    if status[0] != 0: 
        print 'Something wrong happened with aircrack installation'
    else:
        print 'Aircrack installed successfully'
	

def aircrack_exist():
    try:
        devnull = open(os.devnull)
        subprocess.Popen("aircrack-ng", stdout=devnull, stderr=devnull).communicate() # try to find if airackrack is installed in our machine
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False # it isn't installed
    print 'Aircrack suit was successfuly located on our machine'
    return True # it is installed


def stop_network_manager():
    status = commands.getstatusoutput('service network-manager stop')
    if status[0] != 0: 
        print 'Couldn\'t stop network manager'
    else:
        print 'Network manager stoped successfuly'
    

def start_network_manager():
    status = commands.getstatusoutput('service network-manager start')
    if status[0] != 0: 
        print 'Couldn\'t start network manager'
    else:
        print 'Network manager started successfuly'

def get_wireless_card():
    airmon = commands.getoutput("airmon-ng | egrep -e '^[a-z]{2,4}[0-9]'")

    airmon = airmon.split('\n')
    device_interface = list()
    for interface in airmon:
        if interface == "":
                continue
        elif interface[0:3] == 'mon':
            tmp_inteface = interface.split('\t')
            print 'found enable monitor mode :' + tmp_inteface[0]
            print 'we are going to remove it'
            disable_monitor_mode(tmp_inteface[0])
        elif interface[0:4] == 'wlan':
            device_interface = interface.split('\t')
    print 'Device interface we using is' + device_interface[0]
    return device_interface[0]


def get_device_mac(device_interface):
    current_mac = commands.getoutput("ifconfig " + device_interface + " | grep HWaddr | awk ' { print $5 } ' | tr '-' ':'")
    current_mac = current_mac[:17]
    print 'Our device-host mac adress is ' + current_mac
    return current_mac

def enable_monitor_mode(device_interface):
    status = commands.getstatusoutput('airmon-ng start ' + device_interface)
    if status[0] != 0: 
        print 'Error setting device ' + device_interface + ' into monito mode'
    else:
        print 'Monitor Mode enabled successfuly on divice: ' + device_interface

def disable_monitor_mode(device_interface):
    command = 'airmon-ng stop ' + device_interface
    status = commands.getstatusoutput(str(command))
    if status[0] != 0: 
        print 'Error getting ' + device_interface + ' back to Manage mode'
    else:
        print 'Montor Mode disabled successfuly from divice: ' + device_interface

def scan_for_networks(self):
    print 'Now we\'re going to scan for avaible networks'
    scan_command = 'airodump-ng --output-format csv --write wifi-scan mon0' 
    thr = RetardedKill("airodump-ng", 15)
    thr.start()

    status = commands.getstatusoutput(scan_command)

    if status[0] != 0:
        print 'Couldn\'t scan from networks'
    else:
        print 'successfuly scaned from networks'

    output_raw = commands.getoutput('cat wifi-scan*.csv')

    output     = output_raw.split("\n")
    return output

def parse_output(self, output):

    uniq_bssid = set()
    order_id=0
        
    for out in output:
        match = re.match(r"([0-9A-Fa-f]{2,2}:[0-9A-Fa-f]{2,2}:[0-9A-Fa-f]{2,2}:[0-9A-Fa-f]{2,2}:[0-9A-Fa-f]{2,2}:[0-9A-Fa-f]{2,2})\s*,\s*\d{4,4}-\d{2,2}-\d{2,2}\s*\d{2,2}:\d{2,2}:\d{2,2}\s*,\s*\d{4,4}-\d{2,2}-\d{2,2}\s*\d{2,2}:\d{2,2}:\d{2,2}\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\w+)\s*,\s*([\w\s]*)\s*,\s*(\w*)\s*,\s*(.\d+)\s*,.+,\s*(.+)\s*,.*", out)

        if not match:
            continue

        bssid = match.group(1)

        if bssid in uniq_bssid:
            continue

        uniq_bssid.add(bssid)
            
        channel = match.group(2)
        mb      = match.group(3)
        enc     = match.group(4)
        cipher  = match.group(5)
        auth    = match.group(6)
        pwr     = match.group(7)
        essid   = match.group(8)


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

        order_id=order_id+1

        self.table_networks.clearSelection()
        commands.getstatusoutput('rm wifi-scan*')



def generate_NetFaster_keyfile(bssid):
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
        print 'removed index : ' + str(i)
    self.statusBar().showMessage('Rescan Networks')
    disable_monitor_mode(self.device_interface)
    enable_monitor_mode(self.device_interface)
    self.output = scan_for_networks(self)                                   #[SUCCESS] 
    parse_output(self, self.output)                                         #[SUCCESS]

def first_scan(self):
    # check if we have aircrack suit installed on our machine               #[SUCCESS]
    # if we don't then we install it
    if bool(aircrack_exist()) == False:
        install_aircrack()

    #init_config_dir()                                                      #[SUCCESS]
    stop_network_manager() # we stop network manager to avoid errors        #[SUCCESS]
    self.device_interface = get_wireless_card()                             #[SUCCESS]
    self.device_mac = get_device_mac(self.device_interface)                 #[SUCCESS]
    enable_monitor_mode(self.device_interface)                              #[SUCCESS]
    self.output = scan_for_networks(self)                                   #[SUCCESS] 
    parse_output(self, self.output)                                         #[SUCCESS]
    self.start_procedure_is_pressed = True
    self.button_rescan_networks.setText("Make a new Scan")
