import sys
import math
import random

"""
This is a simple minimax algorithm implementation in Python.
Check out 1.in file as example of how you're supposed to work with it.
"""

class minimax:
	def __init__(self, filepath, lexicographical=True):
		self.edges = {}
		self.staticvals = {}
		self.startKey = None
		self.lexicographical = lexicographical
		self.staticEvalsList = []
		with open(filepath, 'r') as file:
			for line in file:
				tokens = line.strip().split(' ')

				if tokens[0] == 'static':
					self.staticvals[tokens[1]] = float(tokens[2])

				elif tokens[0] == 'edge':
					divergent = tokens[1]
					incident = tokens[2]

					if not divergent in self.edges:
						self.edges[divergent] = []
					if not incident in self.edges:
						self.edges[incident] = []

					self.edges[divergent].append(incident)

				elif tokens[0] == 'start':
					startNode = tokens[1]
					if not startNode in self.edges:
						self.edges[startNode] = []
					self.startKey = startNode

				else:
					print('E: unknown token \'' + tokens[0] + '\'. Ignoring it.')

	def _getStaticValue(self, state):
		self.staticEvalsList.append(state)
		return self.staticvals[state] if state in self.staticvals else random.random()

	def _getNextMoves(self, state):
		return sorted(self.edges[state]) if self.lexicographical else self.edges[state]

	def _minValue(self, state, maxDepth):
		if state in self.staticvals or maxDepth == 0:
			return self._getStaticValue(state)
		v = +math.inf
		for s in self._getNextMoves(state):
			v = min(v, self._maxValue(s, maxDepth-1))
		return v

	def _maxValue(self, state, maxDepth):
		if state in self.staticvals or maxDepth == 0:
			return self._getStaticValue(state)
		v = -math.inf
		for s in self._getNextMoves(state):
			v = max(v, self._minValue(s, maxDepth-1))
		return v

	def _firstCallMaxValue(self, state, maxDepth):
		if state in self.staticvals or maxDepth == 0:
			return self._getStaticValue(state)
		v = -math.inf
		move = None
		for s in self._getNextMoves(state):
			v, move = max([v, move], [self._minValue(s, maxDepth-1), s])
		return v, move

	def move(self, maxDepth=-1):
		if self.startKey:
			return self._firstCallMaxValue(self.startKey, maxDepth)
		print('No start node specified. Please define it on input file (start ?X).')
		return None

if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print('usage:', sys.argv[0], '<input file>')
		exit(1) 
	bestScore, bestMove = minimax(sys.argv[1]).move()
	print('Best Score:', bestScore, '\tBest Move:', bestMove)