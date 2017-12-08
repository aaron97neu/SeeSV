# Author: Jake Vanderplas -- <vanderplas@astro.washington.edu>
#Edited for use in SeeSV by Evan

print(__doc__)

from time import time
import sys

import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import NullFormatter

from sklearn import manifold, datasets

# Next line to silence pyflakes. This import is needed.
Axes3D

if len(sys.argv) != 3:
	print("Usage: sudo python3 manifold.py <manifold type> <csv File>")
	exit()

#globals
csvFile = open(sys.argv[2],'r')
csvFormat = open("formated/" + sys.argv[2].split("/")[1].split(".")[0] + ".format.csv",'r')
csvFormat = csvFormat.readline().split(":")
n_points = int(csvFormat[1])

data = csvFile.readline()
try:
	int(data.split(","))
except:
	data = csvFile.readline()

X = []
while data != '':
	array = []
	for point in data.split(","):
		array.append(float(point))
	X.append(array)
	data = csvFile.readline()

n_neighbors = 10
n_components = int(csvFormat[0])

fig = plt.figure(figsize=(15, 8))
plt.suptitle("Manifold Learning with %i points, %i features"
             % (len(X), n_components), fontsize=14)


def isoMap():
	t0 = time()
	Y = manifold.Isomap(n_neighbors, n_components).fit_transform(X)
	t1 = time()
	print("Isomap: %.2g sec" % (t1 - t0))
	ax = fig.add_subplot(257)
	plt.scatter(Y[:, 0], Y[:, 1])
	plt.title("Isomap (%.2g sec)" % (t1 - t0))
	ax.xaxis.set_major_formatter(NullFormatter())
	ax.yaxis.set_major_formatter(NullFormatter())
	plt.axis('tight')

def mds():
	t0 = time()
	mds = manifold.MDS(n_components, max_iter=300, n_init=1)
	Y = mds.fit_transform(X)
	t1 = time()
	print("MDS: %.2g sec" % (t1 - t0))
	ax = fig.add_subplot(258)
	plt.scatter(Y[:, 0], Y[:, 1])
	plt.title("MDS (%.2g sec)" % (t1 - t0))
	ax.xaxis.set_major_formatter(NullFormatter())
	ax.yaxis.set_major_formatter(NullFormatter())
	plt.axis('tight')


def specteralEmbedding():
	t0 = time()
	se = manifold.SpectralEmbedding(n_components=n_components,
                                n_neighbors=n_neighbors)
	Y = se.fit_transform(X)
	t1 = time()
	print("SpectralEmbedding: %.2g sec" % (t1 - t0))
	ax = fig.add_subplot(259)
	plt.scatter(Y[:, 0], Y[:, 1])
	plt.title("SpectralEmbedding (%.2g sec)" % (t1 - t0))
	ax.xaxis.set_major_formatter(NullFormatter())
	ax.yaxis.set_major_formatter(NullFormatter())
	plt.axis('tight')

def tSNE():
	t0 = time()
	tsne = manifold.TSNE(n_components=n_components, init='pca', random_state=0)
	Y = tsne.fit_transform(X)
	t1 = time()
	print("t-SNE: %.2g sec" % (t1 - t0))
	ax = fig.add_subplot(2, 5, 10)
	plt.scatter(Y[:, 0], Y[:, 1])
	plt.title("t-SNE (%.2g sec)" % (t1 - t0))
	ax.xaxis.set_major_formatter(NullFormatter())
	ax.yaxis.set_major_formatter(NullFormatter())
	plt.axis('tight')

def save():
	plt.savefig("svgs/" + sys.argv[2].split("/")[1].split(".")[0])

if sys.argv[1] == "mds":
	mds()
elif sys.argv[1] == "t-sne":
	tSNE()
elif sys.argv[1] == "specteral_embedding":
	specteralEmbedding()
elif sys.argv[1] == "isomap":
	isoMap()
elif sys.argv[1] == "all":
	mds()
	if n_components < 4:
		tSNE()
	specteralEmbedding()
	isoMap()
else:
	print("Types: mds, t-sne, specteral_embedding, isomap, all")
	exit()

save()
