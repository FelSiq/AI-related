import math
import random

class minimax:
	def _getStaticValue(self, state):
		return random.randint()

	def _getNextMoves(self, state):
		return 

	def _minValue(self, state, depth):
		if state == self.endGameState or depth == 0:
			return self._getStaticValue(state)
		v = math.inf
		for s in self._getNextMoves(state):
			v = min(v, self._maxValue(s, depth-1))
		return v

	def _maxValue(self, state, depth):
		if state == self.endGameState or depth == 0:
			return self._getStaticValue(state)
		v = -math.inf
		for s in self._getNextMoves(state):
			v = max(v, self._minValue(s, depth-1))
		return v

	def move(self, state, depth):
		return self._maxValue(self, state, depth)

if __name__ == '__main__':
	bestMove = minimax().move(0, 5)
	print(bestMove)