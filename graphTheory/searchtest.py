from graph import blindSearch, informedSearch, branchAndBound
import sys

def printSearchOutput(algorithm, outputDic):
	keys = sorted(outputDic.keys())
	print('\u256D', algorithm, sep='')
	for k in range(len(keys)):
		curKey = keys[k]
		print(('\u2514' if k == len(keys) - 1 else '\u251C') 
			+ '\u2500\u2500\u2500\u2500\u257C', curKey, ':', outputDic[curKey])

if __name__ == '__main__':

	if len(sys.argv) <= 4:
		print('usage: <graph filepath> <start> <end> <plot? 0/1> <plotDelay (optional)>')
		exit(1)

	start = sys.argv[2]
	end = sys.argv[3]
	plot = bool(int(sys.argv[4]))

	plotDelay = 0.025
	if len(sys.argv) >= 6:
		plotDelay = float(sys.argv[5])

	Ga = blindSearch(sys.argv[1], geometrical = True, directed=False)
	Gb = informedSearch(sys.argv[1], geometrical = True, directed=False)
	Gc = branchAndBound(sys.argv[1], geometrical = True, directed=False)
	Ga.print()

	if not (start in Ga.edgeList and end in Ga.edgeList):
		print('E: invalid start/end indexes for search.') 
		exit(2)

	print('\n')

	searches = {'BFS':False, 'DFS':False, 'HC':False, 'BS':False, 'BB':False, 'AStar':False}

	if searches['BFS']:
		printSearchOutput('BFS', Ga.bfs(start, end, prune=False, lexicographical=True, 
			statisticOutput=True, plot=plot, plotSpeed=plotDelay))
	if searches['DFS']:
		printSearchOutput('DFS', Ga.dfs(start, end, prune=True, lexicographical=True, 
			statisticOutput=True, plot=plot, plotSpeed=plotDelay))
	if searches['HC']:
		printSearchOutput('HC', Gb.hillClimbing(start, end, 
			statisticOutput=True, plot=plot, plotSpeed=plotDelay))
	if searches['BS']:
		printSearchOutput('BS', Gb.beamSearch(start, end, 
			statisticOutput=True, keptChildren=2, plot=plot, plotSpeed=plotDelay))
	if searches['BB']:
		printSearchOutput('B&B', Gc.branchAndBound(start, end, 
			statisticOutput=True, plot=plot, plotSpeed=plotDelay, prune=True))
	if searches['AStar']:
		printSearchOutput('A*', Gc.Astar(start, end, statisticOutput=True, plot=plot))
