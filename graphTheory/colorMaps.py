from graph import graph
import sys

class colorMaps(graph):
	def __init__(self, filepath=None, numColors=4):
		super().__init__(filepath)
		self.numColors = numColors
		keys = self.edgeList.keys()
		self.domain = {key : [True] * numColors for key in keys}
		self.color = {key : 0 for key in keys}
		self.colorSeq = ['blue', 'red', 'yellow', 'green']

	def _startColorQueue(self, startAt):
		queue = []

		keys = list(self.edgeList.keys())
		startNode = keys[0]
		if startAt == 0: # Random
			startNode = keys[random.randint(0, len(keys)-1)]
		elif startAt == 1 or startAt == 2: # Less constrained
			neighbors = len(self.edgeList[startNode]['adj'])
			n = len(self.edgeList)
			for i in range(n):
				curNeighbors = len(self.edgeList[keys[i]]['adj'])
				if (startAt == 1 and neighbors > curNeighbors) or (startAt == 2 and neighbors < curNeighbors):
					neighbors = curNeighbors
					startNode = keys[i]
		else:
			print('W: unkown \'startAt\' parameter. Starting on node with index 0.')

		queue.append(startNode)
		return queue

	def _checkConstraints(self, curNode, constraints, c):
		# Constraints:
		# 1 = Nothing
		# 2 = Neighbors
		# 3 = Propagate to neighbors til 1 constraint
		# 4 = Propagate to neighbors
		# 5 = Everything
		retValue = True

		if constraints == 1:
			retValue = True
		elif constraints == 2:
			neighbors = self.edgeList[curNode]['adj']
			for n in neighbors:
				if sum(self.domain[n]) == 1 and self.domain[n][c]:
					retValue = False
		elif constraints == 3:
			retValue = True
		elif constraints == 4:
			retValue = True
		elif constraints == 5:
			retValue = True
		else:
			print('E: unkown constraint ID \'', constraints, '\'.')
			retValue = False
		return retValue


	def _insertAtColorQueue(self, queue, curNode, c, startAt):
		# Start @:
		# 1 = Random
		# 2 = Less constrained
		# 3 = Most constrained
		neighbors = self.edgeList[curNode]['adj']
		for n in neighbors:
			self.domain[n][c] = False
			queue.push(n)
		self.domain[curNode][c] = False
		self.color[curNode] = c


	def _translateColor(self, color):
		return self.colorSeq[color]

	def paintGraph(self, constraints=3, startAt=2):
		queue = self._startColorQueue(startAt)
		while len(queue):
			curNode = queue.pop()
			for c in range(self.numColors):
				if self._checkConstraints(curNode, constraints, c):
					self._insertAtColorQueue(queue, curNode, c, startAt)

		for k in self.edgeList:
			self.edgeList[k]['color'] = self._translateColor(self.color[k])

if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print('usage:' + sys.argv[0] + ' <filepath>')
		exit(1)
	cm = colorMaps(filepath=sys.argv[1], numColors=4)
	cm.paintGraph(constraints=2, startAt=1)
	cm.plot()