import time  # Measuring attack intervals

# Executing, communicating with, killing processes
from subprocess import Popen, call, PIPE, check_output

has_handshake = False
bssid = "F8:D1:11:26:6D:32"
crack = 'echo "" | aircrack-ng -a 2 -w - -b ' + bssid + ' ' + 'output*.cap'
proc_crack = Popen(crack, stdout=PIPE, shell=True)
proc_crack.wait()
txt = proc_crack.communicate()[0]
txt = txt.splitlines()
print txt[2]

if txt[2] != "No valid WPA handshakes found.":
	print True
