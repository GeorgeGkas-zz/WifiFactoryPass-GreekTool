variables = list()
with open('variables.txt', 'r') as f:
    variables = f.readlines()
mac_vendor = variables[0].split('|')
mac_serial = variables[1].split('|')

if mac_vendor[1][0:-1] and mac_serial[1][0:-1]:
	print 'both'
elif mac_vendor[1][0:-1]:
	print 'vendor'
elif mac_serial[1][0:-1]:
	print 'serial'
else:
	print 'none'
