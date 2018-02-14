import colorama
import random
import math

class tictactoe:
	def __init__(self):
		self.gameMat = [[[0.0] for j in range(3)] for i in range(3)]
		self.gameRefs = [
			[self.gameMat[0][i] for i in range(3)],
			[self.gameMat[1][i] for i in range(3)],
			[self.gameMat[2][i] for i in range(3)],
			[self.gameMat[i][0] for i in range(3)],
			[self.gameMat[i][1] for i in range(3)],
			[self.gameMat[i][2] for i in range(3)],
			[self.gameMat[i][i] for i in range(3)],
			[self.gameMat[2-i][i] for i in range(3)]
		]

	def _getNextMoves(self):
		moveList = []
		for i in range(3):
			for j in range(3):
				if not self.gameMat[j][i][0]:
					moveList.append((i, j))
		return moveList

	def _checkMoves(self):
		for i in self.gameMat:
			for j in i:
				if j[0] == 0.0:
					return True
		return False

	def _minValue(self, alpha, beta):
		gameValue = self._getStaticValue()
		if gameValue or not self._checkMoves():
			return gameValue
		
		for x, y in self._getNextMoves():
			self.gameMat[y][x][0] = -1.0
			beta = min(beta, self._maxValue(alpha, beta))
			self.gameMat[y][x][0] = +0.0
			if alpha >= beta:
				return beta

		return beta

	def _maxValue(self, alpha, beta):
		gameValue = self._getStaticValue()
		if gameValue or not self._checkMoves():
			return gameValue

		for x, y in self._getNextMoves():
			self.gameMat[y][x][0] = +1.0
			alpha = max(alpha, self._minValue(alpha, beta))
			self.gameMat[y][x][0] = +0.0
			if alpha >= beta:
				return alpha

		return alpha

	def _firstCallMaxValue(self, alpha, beta):
		gameValue = self._getStaticValue()
		if gameValue or not self._checkMoves():
			return gameValue

		bestX, bestY = None, None
		for x, y in self._getNextMoves():
			self.gameMat[y][x][0] = +1.0
			returnedValue = self._minValue(alpha, beta)
			self.gameMat[y][x][0] = +0.0
			if (bestX == None and alpha <= returnedValue) or alpha < returnedValue:
				alpha = returnedValue
				bestX = x
				bestY = y

			if alpha >= beta:
				return bestX, bestY

		return bestX, bestY

	def _getStaticValue(self):
		for p in self.gameRefs:
			aux = 0
			for n in p:
				aux += n[0]
			if abs(aux) == 3.0:
				if aux > 0:
					# Machine won
					return 100.0
				# Player won
				return -100.0
		# Nobody won
		return 0.0

	def move(self):
		return self._firstCallMaxValue(-math.inf, math.inf)

	def _printGame(self):
		pos = 0
		for m in self.gameMat:
			for n in m:
				symbol = colorama.Fore.GREEN + str(pos + 1)
				if n[0] > 0.0:
					symbol = colorama.Fore.RED + 'X' 
				elif n[0] < 0.0:
					symbol = colorama.Fore.BLUE + 'O'

				print(symbol + colorama.Fore.RESET, end='\t')
				if (pos + 1) % 3 == 0:
					print()
				pos += 1
		print()

	def play(self):
		playerTurn = random.random() >= 0.5
		gameState = self._getStaticValue()
		while self._checkMoves() and not gameState:
			if playerTurn:
				self._printGame()
				print('Make a move: ', end='')
				askMoveFlag = True
				while askMoveFlag:
					try:
						position = int(input().strip()) - 1
						moveX = position %  3
						moveY = position // 3
						if self.gameMat[moveY][moveX][0] == 0.0:
							self.gameMat[moveY][moveX][0] = -1.0
							askMoveFlag = False
						else:
							print('No way. Choose a empty position: ', end='')
					except:
						print('No way. Try again: ', end='')
				playerTurn = False
			else:
				bestX, bestY = self.move()
				self.gameMat[bestY][bestX][0] = 1.0
				playerTurn = True

			gameState = self._getStaticValue()
		self._printGame()

		if gameState > 0.0:
			endMessage = 'Machine won.'
		elif gameState < 0.0:
			endMessage = 'You won. Please report this accomplishment to me as a program glitch as fast as possible.'
		else:
			endMessage = 'Draw.'

		print('Game\'s end.', endMessage)

if __name__ == '__main__':
	tictactoe().play()