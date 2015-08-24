import fileinput 
fname = 'wash.out'
with open(fname) as f:
    content = f.readlines()

networks = list()
data = list()

for info in content[7:]:
	if not info == '\n':
		networks.append(info)

for info in networks:
	data = info.split(' ')

for info in data:
	if not not info:
		print info