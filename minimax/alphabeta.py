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

	def _minValue(self, state, depth, alpha, beta):
		self.visited[state] = True
		if state in self.staticvals or depth == 0:
			return self._getStaticValue(state)
		
		for s in self._getNextMoves(state):
			beta = min(beta, self._maxValue(s, depth-1, alpha, beta))
			if alpha >= beta:
				self.prunes += 1
				return beta

		return beta

	def _maxValue(self, state, depth, alpha, beta):
		self.visited[state] = True
		if state in self.staticvals or depth == 0:
			return self._getStaticValue(state)

		for s in self._getNextMoves(state):
			alpha = max(alpha, self._minValue(s, depth-1, alpha, beta))
			if alpha >= beta:
				self.prunes += 1
				return alpha

		return alpha

	def move(self, maxDepth=-1, statistics=False):
		if self.startKey:
			bestScore = self._maxValue(self.startKey, maxDepth, -math.inf, math.inf)
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
	bestMove = alphabeta(sys.argv[1]).move(statistics=True)
	print(bestMove)