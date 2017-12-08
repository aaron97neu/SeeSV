import sys
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import math

#global variables
numPoints = 0
features = 0
inputTextFile = sys.argv[1]

svgPath = inputTextFile.split("/csvs/")[0] + "/svgs/"
outputPath = inputTextFile.split("/csvs/")[0] + "/ehabd_scripts/"
distThresh = -1
radius = distThresh

import importlib.util
spec = importlib.util.spec_from_file_location("ehabd_scripts.csvFormat", outputPath + "csvFormat.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)

foo.reduce(inputTextFile)

percent = 30.0/100.0

data = open(inputTextFile)

#Takes a string of format value1,value2,value3 and returns an array with values of deisred features
def Parse(s,feature1,feature2):
	tem = s.split(",")
	ohNaNa = []
	ohNaNa.append(tem[feature1])
	ohNaNa.append(tem[feature2].split("\n")[0])
	return ohNaNa

#Calculates distance between two points
def distance(point1, point2):
	return math.sqrt(math.pow(float(point1[0]) - float(point2[0]),2) + math.pow(float(point1[1]) - float(point2[1]),2))

#Get pointDataString in correct format?
def prime():
	global data, numPoints, features
	fileName = sys.argv[1].split("/")
	fileName = fileName[len(fileName) - 1]
	fileName = fileName.split(".")[0]
	infophile = open(outputPath + "formated/" + fileName + ".format.csv",'r')
	dataWay = infophile.readline()
	maxRange = int(dataWay.split(":")[1])
	numPoints = maxRange
	features = int(dataWay.split(":")[0])

#Get all data points as an array from file
def getAllPoints(feature1,feature2):
	global numPoints, pointDataString, data, distThresh, radius, percent
	setOfAll = []
	dataString = data.readline()
	try:
		float(dataString.split(",")[0])
	except:
		dataString = data.readline()
	while dataString != "":
		setOfAll.append(Parse(dataString,feature1,feature2))
		dataString = data.readline()

	#Get max X and Y
	Xhigh = float(setOfAll[0][0])
	Yhigh = float(setOfAll[0][1])
	Xlow = float(setOfAll[0][0])
	Ylow = float(setOfAll[0][1])
	for point in setOfAll:
		if float(point[0]) > Xhigh:
			Xhigh = float(point[0])
		elif float(point[0]) < Xlow:
			Xlow = float(point[0])
		if float(point[1]) > Yhigh:
			Yhigh = float(point[1])
		elif float(point[1]) < Ylow:
			Ylow = float(point[1])
	distThresh = distance([(Xhigh-Xlow)*percent,(Yhigh-Ylow)*percent],[0,0])
	radius = distThresh
	return setOfAll


#adds ranking to loaded list (finds num neighbors within range)
def rankAll(points):
	rankedPointz = []
	for point in points:
		print("Running rank for point " + str(point[0]) + "...")
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
	print("Filtering List")
	ranked_points = []
	ranked_points.append(points[0])
	for point in points:
		insert = False
		for i in range(0,len(ranked_points)):
			if distance(point,ranked_points[i]) > radius:
				ranked_points.insert(i, point)
				print("Inserting " + point[0] + ": value=" + str(point[2]) +": At position " + str(i))
				insert = True
				break
			elif point[2] > ranked_points[i][2]:
				ranked_points.remove(ranked_points[i])
				ranked_points.insert(i,point)
				print("Replacing")
				break
	return ranked_points

	

def reduce(points,feature1,feature2):
	newPointList = []
	for point in points:
		nah = True
		for newPoint in newPointList:
			if (point[2] <= newPoint[2] and distance(newPoint,point) < radius):# or point[2] < 10:
				nah = False
		if nah:
			newPointList.append(point)
	return newPointList

#Make the array of reduced points
prime()
#Actually do stuff
finin = []
for i in range(0,features):
	for j in range(0,features):
		if i != j:
			finin.append(reduce(sortList(rankAll(getAllPoints(i,j))),i,j))
			data.seek(0)

for i in range(0,features):
	for j in range(0,features):
		if i != j:
			print(str(i),str(j),len(finin[i]))
			print(finin[i*(features-1)+j])

#Make the .ehabd file
inputFileName = inputTextFile.split("/")
inputFileName = inputFileName[len(inputFileName)-1]
inputFileName = inputFileName.split(".")[0]
f, axes = plt.subplots(features, features, figsize=(50,50))
output = open(outputPath + "EHABD_Files/" + inputFileName + ".ehabd","w+")
for i in range(0,features):
	for j in range(0,features):
		if i != j:
			axes[i,j].plot(finin[i*(features-1)+j],'ro')
			axes[i,j].set_title("Feature " + str(i) + " vs. Feature " + str(j))
			output.write(str(i) + ":" + str(j) + ":" + str(len(finin[i])))
			output.write("\n")
			for k in range(0,int(len(finin[i]))):
				output.write(str(finin[i][k][0]) + ";" + str(finin[i][k][1].split("\r\n")[0]) + "||")
			output.write('\n')
#for i in range(0,len(finin)):
#	for j in range(0,len(finin[i])):
#		for k in range(0,len(finin)):
#			if j < len(finin[k]):
#				output.write(str(finin[k][j][0]) + ";" + str(finin[k][j][1]))
#		output.write('\n')


fileName = sys.argv[1].split("/")
fileName = fileName[len(fileName) - 1]
fileName = fileName.split(".")[0]
plt.savefig(svgPath + fileName + ".ehabd.svg")


spec = importlib.util.spec_from_file_location("ehabd_scripts.manifold", outputPath + "manifold.py")
bar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bar)

bar.runIt(inputTextFile)
print("done")

def findAndPlot():
        list = rankAll()
        sortedList = sortList(list)
        reduct = reduce(sortedList)
        print("\n\n\n")

"""
--------Test Methods-------
"""
