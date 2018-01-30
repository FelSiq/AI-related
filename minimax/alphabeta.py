from minimax import minimax
import sys
import math
import random

"""
This is a simple minimax algorithm with alpha-beta prunning.
Check out 1.in file as example of how you're supposed to work with it.
"""

class alphabeta(minimax):
	def __init__(self, filepath):
		super().__init__(filepath)
		self.visited = {key : False for key in self.edges}
		self.prunes = 0

	def _minValue(self, state, maxDepth, alpha, beta):
		self.visited[state] = True
		if state in self.staticvals or maxDepth == 0:
			return self._getStaticValue(state)
		
		for s in self._getNextMoves(state):
			beta = min(beta, self._maxValue(s, maxDepth-1, alpha, beta))
			if alpha >= beta:
				self.prunes += 1
				return beta

		return beta

	def _maxValue(self, state, maxDepth, alpha, beta):
		self.visited[state] = True
		if state in self.staticvals or maxDepth == 0:
			return self._getStaticValue(state)

		for s in self._getNextMoves(state):
			alpha = max(alpha, self._minValue(s, maxDepth-1, alpha, beta))
			if alpha >= beta:
				self.prunes += 1
				return alpha

		return alpha

	def _firstCallMaxValue(self, state, maxDepth, alpha, beta):
		self.visited[state] = True
		if state in self.staticvals or maxDepth == 0:
			return self._getStaticValue(state)

		move = None
		for s in self._getNextMoves(state):
			returnedValue = self._minValue(s, maxDepth-1, alpha, beta)
			if alpha < returnedValue:
				alpha = returnedValue
				move = s

			if alpha >= beta:
				self.prunes += 1
				return alpha, move

		return alpha, move

	def move(self, maxDepth=-1, statistics=False):
		if self.startKey:
			bestScore = self._firstCallMaxValue(self.startKey, maxDepth, -math.inf, math.inf)
			if statistics:
				print('# of prunes:', self.prunes)
				print('Prunned node list:')
				for p in self.visited:
					if not self.visited[p]:
						print(p)
			return bestScore
		print('No start node specified. Please define it on input file (start ?X).')
		return None

if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print('usage:', sys.argv[0], '<input file>')
		exit(1) 
	bestScore, bestMove = alphabeta(sys.argv[1]).move(statistics=True)
	print('Best Score:', bestScore, '\tBest Move:', bestMove)