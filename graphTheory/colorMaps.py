from graph import graph
import sys
import copy 

class colorMaps(graph):
	def __init__(self, filepath=None, numColors=4, chooseNode=2, consider=2, rotateColors=True):
		super().__init__(filepath=filepath, directed=False)
		self.numColors = numColors
		keys = self.edgeList.keys()
		self.domain = {key : [True] * numColors for key in keys}
		self.color = {key : -1 for key in keys}
		self.colorSeq = ['b', 'r', 'y', 'g']
		self.backtracks = 0
		self.chooseNode = chooseNode
		self.consider = consider
		self.rotateColors = rotateColors

	def _checkConstraints(self, curNode, c):
		if self.consider == 2:
			# Check only neighbors
			for n in self.edgeList[curNode]['adj']:
				if self.color[n] == c:
					return False
		return True

	def _getNextNode(self, curNode=None):
		nextNode = curNode
		if self.chooseNode == 2:
			# Most constrained first
			keyBag = sorted(list(self.edgeList.keys()), key=lambda k : len(k), reverse=True)
		elif self.chooseNode == 3:
			# Less constrained first
			keyBag = sorted(list(self.edgeList.keys()), key=lambda k : len(k))
		else:
			# Almost 'random' selection
			keyBag = self.color.keys()

		for k in keyBag:
			if self.color[k] == -1:
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
		if statistics:
			print('# of backtrackings:', self.backtracks)
		if plot:
			cm.plot(time=5.0)
		return retVal

if __name__ == '__main__':
	if len(sys.argv) <= 2:
		print('usage:' + sys.argv[0] + ' <filepath> <# of colors>')
		exit(1)
	cm = colorMaps(filepath=sys.argv[1], numColors=int(sys.argv[2]), chooseNode=3)
	cm.paintGraph('H')
