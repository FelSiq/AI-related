import matplotlib.pyplot as plt 
from getmap import getmap
import copy
import sys

class colorpath(getmap):
	def __init__(self, filepath, sep=' ', format='png'):
		self.paintedImage = []
		super().__init__(filepath, sep, format)

	def colorMap(self, start):
		moveseq = [(0,1), (0,-1), (1,0), (-1,0)]

		self.paintedImage = copy.deepcopy(self.image)

		xMax = len(self.image[0])
		yMax = len(self.image)


		queue = [start]
		color = self.maxVal + 1
		threshold = (self.maxVal + self.minVal)/2.0

		self.paintedImage[start[1]][start[0]] = color
		while len(queue):
			color += 1
			curPlace = queue.pop()

			x = curPlace[0]
			y = curPlace[1]

			for m in moveseq:
				xPlus = m[0] 
				yPlus = m[1]
				if 0 <= x+xPlus < xMax and 0 <= y+yPlus < yMax and self.paintedImage[y + yPlus][x + xPlus] < threshold:
					self.paintedImage[y + yPlus][x + xPlus] = color
					queue.insert(0, (x + xPlus, y + yPlus))

		return self.paintedImage

	def findPath(self, end):
		moveseq = [(0,1), (0,-1), (1,0), (-1,0)]

		path = []
		xCur = end[0]
		yCur = end[1]
		xPrv = xCur + 1
		yPrv = yCur + 1

		yMax = len(self.image)
		xMax = len(self.image[0])

		while xCur != xPrv or yCur != yPrv:
			flag = False
			path.append((xCur, yCur))
			xPrv = xCur
			yPrv = yCur
			for m in moveseq:
				xNew = xPrv + m[0]
				yNew = yPrv + m[1]
				if not flag and 0 <= xNew < xMax and 0 <= yNew < yMax:
					if self.maxVal < self.paintedImage[yNew][xNew] < self.paintedImage[yCur][xCur]:
						flag = True
						xCur = xNew
						yCur = yNew
		return path

	def plotPlath(self, end):
		originalYVals = []
		originalXVals = []
		paintedYVals = []
		paintedXVals = []
		pathXVals = []
		pathYVals = []

		findPath = self.findPath(end)

		threshold = (self.maxVal + self.minVal)/2
		for i in range(len(self.image)):
			for j in range(len(self.image[i])):
				if self.image[i][j] >= threshold:
					originalXVals.append(j)
					originalYVals.append(i)
				if self.paintedImage[i][j] > self.maxVal:
					paintedXVals.append(j)
					paintedYVals.append(i)
		for n in findPath:
			pathXVals.append(n[0])
			pathYVals.append(n[1])
		plt.scatter(paintedXVals, paintedYVals, color='0.75', s=1.0)
		plt.scatter(originalXVals, originalYVals, color='black', marker='s', s=1.0)
		plt.scatter(pathXVals, pathYVals, color='red', s=1.0)
		plt.gca().invert_yaxis()
		plt.show()

def printResult(string):
	for s in string:
		for c in s:
			print('{m: <{fill}}'.format(m = c, fill = 5), end='')
		print()

if __name__ == '__main__':
	if len(sys.argv) <= 2:
		print('usage:', sys.argv[0], '<image> <format (txt/png)>')
		exit(1)

	model = colorpath(sys.argv[1], format=sys.argv[2])
	image = model.colorMap((792, 7))

	model.plotPlath((806, 1585))