"""
This is a dumb tic-tac-toe player, made just for statistical purposes.
"""

class dumbttt:
	def __init__(self):
		self.countMat = [[0, 0] for i in range(9)]
		self.position = 0
		self.gameMat = [[[0] for j in range(3)] for i in range(3)]
		self.gameRefs = [
			[self.gameMat[0][i] for i in range(3)],
			[self.gameMat[1][i] for i in range(3)],
			[self.gameMat[2][i] for i in range(3)],
			[self.gameMat[i][0] for i in range(3)],
			[self.gameMat[i][1] for i in range(3)],
			[self.gameMat[i][2] for i in range(3)],
			[self.gameMat[i][i] for i in range(3)],
			[self.gameMat[i][2-i] for i in range(3)]
		]

	def evaluate(self):
		for p in self.gameRefs:
			aux = 0
			for n in p:
				aux += n[0]
			if abs(aux) == 3:
				self.countMat[self.position][1] += 1
				if aux > 0:
					self.countMat[self.position][0] += 1
				return True
		return False

	def _play(self, x, y, p):
		self.gameMat[x][y][0] = p
		if not self.evaluate():
			for i in range(3):
				for j in range(3):
					if self.gameMat[i][j][0] == 0:
						self._play(i, j, -p)
		self.gameMat[x][y][0] = 0

	def play(self):
		for startPos in range(9):
			self.position = startPos
			xStart = startPos % 3
			yStart = startPos //3
			self._play(xStart, yStart, 1)
		return self.countMat

if __name__ == '__main__':
	result = dumbttt().play()
	for pos in range(len(result)):
		print(result[pos][0]/result[pos][1], end='\t')
		if (pos + 1) % 3 == 0:
			print()
	print()

	"""
	RESULT:
		0.6498137307078233	0.5830875122910522	0.6498137307078233	
		0.5830875122910522	0.7358916478555305	0.5830875122910522	
		0.6498137307078233	0.5830875122910522	0.6498137307078233	

	Therefore, if you will blindly gamble whoever will win a tic-tac-toe game, 
	then you should make your bet at the player who starts playing, independently
	of its first move.
	"""