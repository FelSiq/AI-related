import matplotlib.pyplot as plt
from getmap import getmap
import random
import sys

class pathfindAstart(getmap):
	def __init__(self, filepath, sep=' ', format='png'):
		super().__init__(filepath, sep, format)

	def _euclidianDist(self, a, b):
		return sum([(a[i] - b[i])**2.0 for i in range(min(len(a), len(b)))])**0.5

	def _plot(self, predMatrix, start, end, wall=True):
		xCoords = []
		yCoords = []

		if wall:
			wallXVals = []
			wallYVals = []
			threshold = (self.maxVal + self.minVal)/2
			for i in range(len(self.image)):
				for j in range(len(self.image[i])):
					if self.image[i][j] >= threshold:
						wallXVals.append(j)
						wallYVals.append(i)
			plt.scatter(wallXVals, wallYVals, color='black', s=1.0)

		curNode = end
		while curNode != start:
			xCur = curNode[0]
			yCur = curNode[1]
			xCoords.append(xCur)
			yCoords.append(yCur)
			curNode = predMatrix[yCur][xCur]

		plt.scatter(xCoords, yCoords, color='red', s=1.0)
		plt.gca().invert_yaxis()
		plt.show()


	# It will use a non-optimum A*.
	def plotPath(self, start, end):
		xMax = len(self.image[0])
		yMax = len(self.image)

		predMatrix = [[(-1, -1)] * xMax for i in range(yMax)]

		moveSeq = [(0, 1), (0, -1), (1, 0), (-1, 0)]

		minHeap = [{'g': 0.0, 'h': 0.0, 'coord': start}]

		threshold = (self.maxVal + self.minVal)/2.0

		if start != end:
			while len(minHeap):
				curNode = minHeap.pop()
				curDist = curNode['g']
				xCur = curNode['coord'][0]
				yCur = curNode['coord'][1]

				for m in moveSeq:
					xNew = xCur + m[0]
					yNew = yCur + m[1]
					if 0 <= xNew < xMax and 0 <= yNew < yMax and self.image[yNew][xNew] < threshold and predMatrix[yNew][xNew] == (-1, -1):
						predMatrix[yNew][xNew] = curNode['coord']
						if (xNew, yNew) != end:
							minHeap.append({'g': curDist + 1.0, 'h': self._euclidianDist((xNew, yNew), end), 'coord': (xNew, yNew)})
						else:
							minHeap.clear()
				minHeap.sort(key = lambda k : k['g'] + k['h'], reverse=True)

		self._plot(predMatrix, start, end)

if __name__ == '__main__':
	if len(sys.argv) <= 2:
		print('usage:', sys.argv[0], '<image> <format (txt/png)>')
		exit(1)

	model = pathfindAstart(sys.argv[1], format=sys.argv[2])
	model.plotPath((150, 7), (166, 315))