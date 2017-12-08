import sys

if len(sys.argv) != 2:
	print("Usage: sudo python csvFormat.py <csv>")
	exit()

def reduce(filePath):
	toReduce = open(filePath,'r')
	fileName = filePath.split(".")[0].split("/")
	fileName = fileName[len(fileName) - 1]
	reduced = open(filePath.split("/csvs/")[0] + "/ehabd_scripts/formated/" + fileName + ".format.csv",'w+')

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
