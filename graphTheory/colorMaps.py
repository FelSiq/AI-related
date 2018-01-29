from graph import graph
import sys
import copy 

"""
check it's neighbors and the neighbors and the neighbors and the neighbors... as long you find
a domain with a single value. (constraint propagation)
"""
class colorMaps(graph):
	def __init__(self, filepath=None, numColors=4, chooseNode=2, consider=2, rotateColors=True):
		super().__init__(filepath=filepath, directed=False)
		self.numColors = numColors
		keys = self.edgeList.keys()
		self.domain = {key : [True] * numColors for key in keys}
		self.color = {key : -1 for key in keys}
		self.constraintVisised = {key : False for key in keys}
		self.colorSeq = ['b', 'r', 'y', 'g']
		self.backtracks = 0
		self.constraints = 0
		self.chooseNode = chooseNode
		self.consider = consider
		self.rotateColors = rotateColors

	def _checkConstraints(self, curNode, c):
		if self.consider == 2:
			# Check only neighbors
			for n in self.edgeList[curNode]['adj']:
				self.constraints += 1
				if self.color[n] == c:
					return False
		elif self.consider == 3 or self.consider == 4:
			redoQueue = []
			retVal = True
			# Check neighbors of the neighbors with propagation
			for n in self.edgeList[curNode]['adj']:
				self.constraints += 1
				if not self.constraintVisised[n] and not self.domain[n][c] and (self.consider == 3 or (self.consider == 4 and sum(self.domain[n]) == 1)):
					self.constraintVisised[n] = True
					self.domain[n][c] = False
					if sum(self.domain[n]) == 0 and self.color[n] == -1:
						retVal = False
					redoQueue.append(n)
					if retVal:
						retVal = self._checkConstraints(n, c)

			while len(redoQueue):
				curItem = redoQueue.pop()
				self.constraintVisised[curItem] = False
				if retVal:
					self.domain[curItem][c] = True
			return retVal

		return True

	def _getNextNode(self, curNode=None):
		if self.chooseNode == 2:
			# Most constrained first
			keyBag = sorted(list(self.edgeList.keys()), key=lambda k : len(k), reverse=True)
		elif self.chooseNode == 3:
			# Less constrained first
			keyBag = sorted(list(self.edgeList.keys()), key=lambda k : len(k))
		else:
			# Almost 'random' selection
			keyBag = self.color.keys()

		nextNode = curNode
		for k in keyBag:
			if nextNode == curNode and self.color[k] == -1:
				nextNode = k
		return nextNode

	def _genNextColors(self, callColors):
		return [callColors.pop()] + callColors if self.rotateColors else callColors

	def _paintGraph(self, curNode, callColors):
		if self.color[curNode] != -1:
			for n in self.edgeList:
				self.edgeList[n]['color'] = self.colorSeq[self.color[n]]
			return True

		for c in callColors:
			if self._checkConstraints(curNode, c):
				self.color[curNode] = c
				if self._paintGraph(
					curNode=self._getNextNode(curNode), 
					callColors=self._genNextColors(callColors)):
					return True
				self.color[curNode] = -1
		self.backtracks += 1
		return False

	def paintGraph(self, plot=True, statistics=True):
		retVal = self._paintGraph(self._getNextNode(), callColors=list(range(self.numColors)))
		print('Status:', 'concluded successfully.' if retVal else 'failed.')
		print('# of checks (contraints):', self.constraints)
		print('Colors:', self.color)
		if statistics:
			print('# of backtrackings:', self.backtracks)
		if plot:
			cm.plot(time=5.0)
		return retVal

if __name__ == '__main__':
	if len(sys.argv) <= 2:
		print('usage:' + sys.argv[0] + ' <filepath> <# of colors>')
		exit(1)
	cm = colorMaps(filepath=sys.argv[1], numColors=int(sys.argv[2]), chooseNode=3, consider=2)
	cm.paintGraph('H')
