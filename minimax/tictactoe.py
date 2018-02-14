import colorama
import random
import math

class tictactoe:
	def __init__(self):
		self.gameMat = None
		self.gameRefs = None
		self.visitedStatesNum = 0
		self.staticEvaluationsNum = 0
		self._clearGame()
		self.prune = True
		self.depthImpact = 10
		self.humanPlayer = True

	def _clearGame(self):
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
		self.visitedStatesNum = 0
		self.staticEvaluationsNum = 0

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

	def _minValue(self, alpha, beta, depth):
		self.visitedStatesNum += 1
		gameValue = self._getStaticValue(depth)
		if gameValue or not self._checkMoves():
			return gameValue
		
		for x, y in self._getNextMoves():
			self.gameMat[y][x][0] = -1.0
			beta = min(beta, self._maxValue(alpha, beta, depth+1))
			self.gameMat[y][x][0] = +0.0
			if self.prune and alpha >= beta:
				return beta

		return beta

	def _maxValue(self, alpha, beta, depth):
		self.visitedStatesNum += 1
		gameValue = self._getStaticValue(depth)
		if gameValue or not self._checkMoves():
			return gameValue

		for x, y in self._getNextMoves():
			self.gameMat[y][x][0] = +1.0
			alpha = max(alpha, self._minValue(alpha, beta, depth+1))
			self.gameMat[y][x][0] = +0.0
			if self.prune and alpha >= beta:
				return alpha

		return alpha

	def _firstCallMaxValue(self, alpha, beta, depth):
		self.visitedStatesNum += 1
		gameValue = self._getStaticValue(depth)
		if gameValue or not self._checkMoves():
			return gameValue

		bestX, bestY = None, None
		for x, y in self._getNextMoves():
			self.gameMat[y][x][0] = +1.0
			returnedValue = self._minValue(alpha, beta, depth+1)
			self.gameMat[y][x][0] = +0.0
			if (bestX == None and alpha <= returnedValue) or alpha < returnedValue:
				alpha = returnedValue
				bestX = x
				bestY = y

			if self.prune and alpha >= beta:
				return bestX, bestY

		return bestX, bestY

	def _firstCallMinValue(self, alpha, beta, depth):
		self.visitedStatesNum += 1
		gameValue = self._getStaticValue(depth)
		if gameValue or not self._checkMoves():
			return gameValue

		bestX, bestY = None, None
		for x, y in self._getNextMoves():
			self.gameMat[y][x][0] = -1.0
			returnedValue = self._maxValue(alpha, beta, depth+1)
			self.gameMat[y][x][0] = +0.0
			if (bestX == None and beta >= returnedValue) or beta > returnedValue:
				beta = returnedValue
				bestX = x
				bestY = y

			if self.prune and alpha >= beta:
				return bestX, bestY

		return bestX, bestY

	def _getStaticValue(self, depth):
		self.staticEvaluationsNum += 1
		for p in self.gameRefs:
			aux = 0
			for n in p:
				aux += n[0]
			if abs(aux) == 3.0:
				if aux > 0:
					# Machine 1 won
					return self.depthImpact - depth
				# Player won or Machine 2 won
				return -self.depthImpact + depth
		# Nobody won
		return 0.0

	def move(self, maximize):
		if maximize:
			return self._firstCallMaxValue(-math.inf, math.inf, 0)
		return self._firstCallMinValue(-math.inf, math.inf, 0)

	def _printGame(self):
		pos = 0
		print(colorama.Fore.GREEN + '\u250F', '\u2501' * 11, 
			'\u2513' + colorama.Fore.RESET, sep='')
		for m in self.gameMat:
			print(end=colorama.Fore.GREEN + '\u2503 ' + 
				colorama.Fore.RESET)
			for n in m:
				symbol = colorama.Fore.GREEN + str(pos + 1)
				if n[0] > 0.0:
					symbol = colorama.Fore.RED + 'X' 
				elif n[0] < 0.0:
					symbol = colorama.Fore.BLUE + 'O'

				print(symbol + colorama.Fore.RESET, end=' ')
				if (pos + 1) % 3 == 0:
					print(colorama.Fore.GREEN + '\u2503' + 
						colorama.Fore.RESET)
				else:
					print(end='  ')
				pos += 1
		print(colorama.Fore.GREEN + '\u2517', '\u2501' * 11, 
			'\u251B' + colorama.Fore.RESET, sep='')

	def play(self, statistics=False, prune=True, depthImpact=10, humanPlayer=True, gameNumber=1, displayMessages=True, reprintGame=True):
		self.prune = prune
		self.humanPlayer = humanPlayer
		self.depthImpact = depthImpact

		player1Wins = 0
		player2Wins = 0
		totalGames = 0

		while gameNumber > 0:
			self._clearGame()
			gameNumber -= 1
			totalGames += 1
			if displayMessages:
				print('Games remaining: ', gameNumber, '(' + str(totalGames) + ' games played so far)')
			playerTurn = random.random() >= 0.5

			if displayMessages:
				if playerTurn:
					startMessage = 'Human goes first.' if self.humanPlayer else 'Machine 2 (O\'s) starts.'
				else:
					startMessage = 'Machine starts.' if self.humanPlayer else 'Machine 1 (X\'s) starts.'
				print('The tic-tac-toe gods plays an die.', startMessage)

			gameState = self._getStaticValue(0)
			while self._checkMoves() and not gameState:
				if playerTurn:
					if reprintGame:
						self._printGame()
					if self.humanPlayer:
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
					else:
						bestX, bestY = self.move(maximize=False)
						self.gameMat[bestY][bestX][0] = -1.0
					playerTurn = False
				else:
					bestX, bestY = self.move(maximize=True)
					self.gameMat[bestY][bestX][0] = 1.0
					playerTurn = True

				gameState = self._getStaticValue(0)

			if displayMessages:
				self._printGame()

			if gameState > 0.0:
				player1Wins += 1
				if self.humanPlayer:
					endMessage = 'Machine won.'
				else:
					endMessage = 'Machine 1 (X\'s) won.'
			elif gameState < 0.0:
				player2Wins += 1
				if self.humanPlayer:
					endMessage = 'You won. Please report this accomplishment to me as a program glitch as fast as possible.'
				else:
					endMessage = 'Machine 2 (O\'s) won.'
			else:
				endMessage = 'Draw.'

			if statistics and displayMessages:
				print('Game statistics:')
				print('# of Static evaluations:', self.staticEvaluationsNum)
				print('# of visited States:', self.visitedStatesNum)

		if displayMessages:
			print('Game\'s end.', endMessage)
		
		if statistics:
			print('Final statistics:')
			print('Total games: ', totalGames)
			print('Machine' + ('' if self.humanPlayer else ' 1') + ' total wins:', 
				player1Wins, '('+ str(100 * player1Wins/totalGames) +'%)')
			print(('Human Player' if self.humanPlayer else 'Machine 2') + ' total wins:', 
				player2Wins, '('+ str(100 * player2Wins/totalGames) +'%)')

if __name__ == '__main__':
	# tictactoe().play(depthImpact=10, statistics=True, gameNumber=100, 
		# humanPlayer=False, reprintGame=False, displayMessages=False)
	tictactoe().play()