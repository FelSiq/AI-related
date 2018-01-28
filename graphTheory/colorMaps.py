import graph

class colorMaps(graph):
	def _startColorQueue(self, startAt):
		queue = []

		keys = self.edgeList.keys()
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

	def _checkConstraints(curNode, constraints, c):

	def _insertAtColorQueue(queue, curNode, c, startAt):

	def paintGraph(self, numColors=4, constraints=3, startAt=2):
		# Constraints:
		# 1 = Nothing
		# 2 = Neighbors
		# 3 = Propagate to neighbors til 1 constraint
		# 4 = Propagate to neighbors
		# 5 = Everything

		# Start @:
		# 0 = Random
		# 1 = Less constrained
		# 2 = Most constrained
		queue = self._startColorQueue(startAt)
		while len(queue):
			curNode = queue.pop()
			for c in range(numColors):
				if self._checkConstraints(curNode, constraints, c):
					self._insertAtColorQueue(queue, curNode, c, startAt)