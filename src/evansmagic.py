import sys
import math

numPoints = 0
features = 0

inputTextFile = sys.argv[1]
distThresh = 1
radius = distThresh
#open file
data = open(inputTextFile)


#Create set with format format time,latitude,longitude,velocity from download.py style
def Parse(s,feature1,feature2):
	tem = s.split(",")
	ohNaNa = []
	ohNaNa.append(tem[feature1])
	ohNaNa.append(tem[feature2])
	return ohNaNa

def distance(point1, point2):
	return math.sqrt(math.pow(float(point1[0]) - float(point2[0]),2) + math.pow(float(point1[1]) - float(point2[1]),2))
	#return great_circle(latlong1, latlong2).miles
#test parse
def testParse():
	pointDataString = data.readline()
	print pointDataString
	while pointDataString != None:
		print Parse(pointDataString)
		data.readline()
		pointDataString = data.readline()
		if "Number of entries: " in pointDataString:
			break

pointDataString = ""

def prime():
	global numPoints, pointDataString, features
	#testParse()
	pointDataString = data.readline()
	maxRange = int(pointDataString.split(",")[0])
	numPoints = maxRange
	features = int(pointDataString.split(",")[1])
	pointDataString = data.readline()

def getAllPoints(feature1,feature2):
	global numPoints, pointDataString
	setOfAll = []
	#print pointDataString
	for i in range(0,numPoints):
		setOfAll.append(Parse(pointDataString,feature1,feature2))
		pointDataString = data.readline()
	return setOfAll

#testAllPoints
#print getAllPoints()

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
		print(point[2])
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
finin = []
for i in range(0,features):
	for j in range(i,features):
		if i != j:
			finin.append(reduce(sortList(rankAll(getAllPoints(i,j))),i,j))
			data.seek(0)
			prime()

for i in range(0,features):
	for j in range(i,features):
		if i != j:
			print(str(i),str(j),len(finin[i]))
			print(finin[i])
def findAndPlot():
        list = rankAll()
        sortedList = sortList(list)
        reduct = reduce(sortedList)
        print("\n\n\n")

