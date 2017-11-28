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
def Parse(s):
	tem = s.split(",")
	return tem

def distance(point1, point2, metric1, metric2):
	#latlong1 = (float(point1[1]),float(point1[2]))
	#latlong2 = (float(point2[1]),float(point2[2]))
	return math.sqrt(math.pow(float(point1[metric1]) - float(point2[metric1]),2) + math.pow(float(point1[metric2]) - float(point2[metric2]),2))
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

#testParse()

def getAllPoints():
	global numPoints, features
	setOfAll = []
	pointDataString = data.readline()
	maxRange = int(pointDataString.split(",")[0])
	numPoints = maxRange
	features = int(pointDataString.split(",")[0])
	pointDataString = data.readline()
	#print pointDataString
	for i in range(0,maxRange):
		setOfAll.append(Parse(pointDataString))
		pointDataString = data.readline()
	return setOfAll

#testAllPoints
#print getAllPoints()
print "Loading list..."
pointlist = getAllPoints()
print(len(pointlist))
print "Loaded"

#adds ranking to loaded list (finds num neighbors within range)
def rankAll():
	rankedPointz = []
	for point in pointlist:
		print "Running rank for point " + str(point[0]) + "..."
		numNeighbors = 0
		for point2 in pointlist:
			if point != point2 and distance(point,point2,0,1) < distThresh:
				numNeighbors = numNeighbors + 1
				#iprint distance(point,point2)
		point.append(numNeighbors)
		rankedPointz.append(point)
		print point[4]
	return rankedPointz

#legacy
def sortList(points):
	print "Filtering List"
	ranked_points = []
	ranked_points.append(points[0])
	for point in points:
		insert = False
		for i in range(0,len(ranked_points)):
			if distance(point,ranked_points[i],0,1) > radius:
				ranked_points.insert(i, point)
				print "Inserting " + point[0] + ": value=" + str(point[4]) +": At position " + str(i)
				insert = True
				break
			elif point[4] > ranked_points[i][4]:
				ranked_points.remove(ranked_points[i])
				ranked_points.insert(i,point)
				print "Replacing"
				break
	return ranked_points

	

def reduce(points):
	newPointList = []
	for point in points:
		nah = True
		for newPoint in newPointList:
			if (point[4] <= newPoint[4] and distance(newPoint,point,0,1) < radius) or point[4] < 10:
				nah = False
		if nah:
			newPointList.append(point)
	return newPointList

print reduce(sortList(rankAll()))
								
def findAndPlot():
        list = rankAll()
        sortedList = sortList(list)
        reduct = reduce(sortedList)
        print("\n\n\n")

