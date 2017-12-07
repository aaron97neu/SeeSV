import sys

if len(sys.argv) != 2:
	print("Usage: sudo python csvFormat.py <csv>")
	exit()

toReduce = open(sys.argv[1],'r')
reduced = open("formated/" + sys.argv[1].split(".")[0].split("/")[1] + ".format.csv",'w+')

currLine = toReduce.readline()
features = len(currLine.split(","))

try:
	int(currLine.split(",")[0])
	totalLines = 1
except:
	totalLines = 0

currLine = toReduce.readline()
while currLine != '':
	totalLines = totalLines + 1
	currLine = toReduce.readline()

reduced.write(str(features) + ":" + str(totalLines) + "\n")
