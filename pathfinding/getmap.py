import matplotlib.image as mpimg

class getmap:
	def __init__(self, filepath, sep=' ', format='png'):
		self.image = []
		self.maxVal = 1
		self.minVal = 0

		if format == 'png':
			img = mpimg.imread(filepath, format='png')

			x = img.shape[0]
			y = img.shape[1]

			for i in range(x):
				self.image.append([])
				for j in range(y):
					newValue = int(img[i][j][0] == 0)
					self.image[i].append(newValue)
					self.maxVal = max(self.maxVal, newValue)
					self.minVal = min(self.minVal, newValue)
		elif format == 'txt':
			with open(filepath, 'r') as file:
				for line in file:
					newLine = list(map(int, line.strip().split(sep)))
					self.image.append(newLine)
					self.maxVal = max(self.maxVal, max(newLine))
					self.minVal = min(self.minVal, min(newLine))