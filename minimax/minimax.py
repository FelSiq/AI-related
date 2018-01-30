import sys
import math
import random

"""
This is a simple minimax algorithm implementation in Python.
Check out 1.in file as example of how you're supposed to work with it.
"""

class minimax:
	def __init__(self, filepath):
		self.edges = {}
		self.staticvals = {}
		self.startKey = None
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

					self.edges[divergent].append(incident)

				elif tokens[0] == 'start':
					startNode = tokens[1]
					if not startNode in self.edges:
						self.edges[startNode] = []
					self.startKey = startNode

				else:
					print('E: unknown token \'' + tokens[0] + '\'. Ignoring it.')

	def _getStaticValue(self, state):
		return self.staticvals[state] if state in self.staticvals else random.random()

	def _getNextMoves(self, state):
		return self.edges[state]

	def _minValue(self, state, depth):
		if state in self.staticvals or depth == 0:
			return self._getStaticValue(state)
		v = +math.inf
		for s in self._getNextMoves(state):
			v = min(v, self._maxValue(s, depth-1))
		return v

	def _maxValue(self, state, depth):
		if state in self.staticvals or depth == 0:
			return self._getStaticValue(state)
		v = -math.inf
		for s in self._getNextMoves(state):
			v = max(v, self._minValue(s, depth-1))
		return v

	def move(self, maxDepth=-1):
		if self.startKey:
			return self._maxValue(self.startKey, maxDepth)
		print('No start node specified. Please define it on input file (start ?X).')
		return None

if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print('usage:', sys.argv[0], '<input file>')
		exit(1) 
	bestMove = minimax(sys.argv[1]).move()
	print(bestMove)