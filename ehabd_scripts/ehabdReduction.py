import sys
import math

#global variables
numPoints = 0
features = 0
inputTextFile = sys.argv[1]
distThresh = 10000
radius = distThresh
data = open(inputTextFile)

#Takes a string of format value1,value2,value3 and returns an array with values of deisred features
def Parse(s,feature1,feature2):
	tem = s.split(",")
	ohNaNa = []
	ohNaNa.append(tem[feature1])
	ohNaNa.append(tem[feature2])
	return ohNaNa

#Calculates distance between two points
def distance(point1, point2):
	return math.sqrt(math.pow(float(point1[0]) - float(point2[0]),2) + math.pow(float(point1[1]) - float(point2[1]),2))

#Get pointDataString in correct format?
def prime():
	global data, numPoints, features
	data.readline()
	pointDataString = data.readline()
	maxRange = int(pointDataString.split(",")[1])
	numPoints = maxRange
	features = int(pointDataString.split(",")[0])
	data.seek(0)	

#Get all data points as an array from file
def getAllPoints(feature1,feature2):
	global numPoints, pointDataString, data
	setOfAll = []
	data.readline()
	dataString = data.readline()
	while dataString != "":
		setOfAll.append(Parse(dataString,feature1,feature2))
		dataString = data.readline()
	return setOfAll


#adds ranking to loaded list (finds num neighbors within range)
def rankAll(points):
	rankedPointz = []
	for point in points:
		print "Running rank for point " + str(point[0]) + "..."
		numNeighbors = 0
		for point2 in points:
			if point != point2 and distance(point,point2) < distThresh:
				numNeighbors = numNeighbors + 1
				#iprint distance(point,point2)
		point.append(numNeighbors)
		rankedPointz.append(point)
	return rankedPointz

#legacy
def sortList(points):
	print "Filtering List"
	ranked_points = []
	ranked_points.append(points[0])
	for point in points:
		insert = False
		for i in range(0,len(ranked_points)):
			if distance(point,ranked_points[i]) > radius:
				ranked_points.insert(i, point)
				print "Inserting " + point[0] + ": value=" + str(point[2]) +": At position " + str(i)
				insert = True
				break
			elif point[2] > ranked_points[i][2]:
				ranked_points.remove(ranked_points[i])
				ranked_points.insert(i,point)
				print "Replacing"
				break
	return ranked_points

	

def reduce(points,feature1,feature2):
	newPointList = []
	for point in points:
		nah = True
		for newPoint in newPointList:
			if (point[2] <= newPoint[2] and distance(newPoint,point) < radius) or point[2] < 10:
				nah = False
		if nah:
			newPointList.append(point)
	return newPointList

prime()
#Actually do stuff
finin = []
for i in range(0,features):
	for j in range(i,features):
		if i != j:
			finin.append(reduce(sortList(rankAll(getAllPoints(i,j))),i,j))
			data.seek(0)

for i in range(0,features):
	for j in range(i,features):
		if i != j:
			print(str(i),str(j),len(finin[i]))
			print(finin[i])

inputFileName = inputTextFile.split("/")
inputFileName = inputFileName[len(inputFileName)-1]
inputFileName = inputFileName.split(".")[0]
output = open("EHABD_Files/" + inputFileName + ".ehabd","w+")
for i in range(0,features):
	for j in range(i,features):
		if i != j:
			output.write(str(i) + ":" + str(j) + ":" + str(len(finin[i])))
			if i != features - 2:
				output.write(",")
			else:
				output.write("\n")
for i in range(0,len(finin)):
	for j in range(0,len(finin[i])):
		for k in range(0,len(finin)):
			if j < len(finin[k]):
				output.write(str(finin[k][j][0]) + ";" + str(finin[k][j][1]))
		output.write('\n')

def findAndPlot():
        list = rankAll()
        sortedList = sortList(list)
        reduct = reduce(sortedList)
        print("\n\n\n")

"""
--------Test Methods-------
"""

#test parse
def testParse():
	pointDataString = data.readline()
	print pointDataString
	while pointDataString != None:
		print Parse(pointDataString)
		data.readline()
		pointDataString = data.readline()
