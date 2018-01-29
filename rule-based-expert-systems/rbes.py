import re

class RBES:
	def __init__(self, filepath):
		self.assertments = []
		self.rules = []
		self.getParenthesisRegex = re.compile(r'\(([^\(\)]+)\)')
		self.solveOperatorRegex = re.compile(r'[^*+]+[*+][^*+]+')
		
		getTokensRegex = re.compile(r'(A|R)\s*([^\n]+)\n?')

		for line in filepath:
			tokens = getTokensRegex.match(line)
			tokenType = tokens.group(1)
			tokenValue = tokens.group(2)

			if tokenType == 'A':
				self.assertments.append(tokenValue)
			elif tokenType == 'R':
				self.rules.append(tokenValue)
			else:
				print('E: unkown token type \'' + tokenType + 
					'\'. Must be \'A\' (Assertment) or \'R\' (Rule). Ignoring it.\n')

	def _booleanLogicCheck(self, rule, assertment):
		processedRule = re.sub('OR', '+', re.sub('AND', '*', '(' + rule + ')'))

		parenthesis = ['start.']
		while len(parenthesis):
			# While there is remaining parenthesis
			parenthesis = self.getParenthesisRegex.findall(processedRule)
			for p in parenthesis:
				# For each logic parenthesis, solve all operators
				operations = self.solveOperatorRegex.findall(p)
				while len(operations): 
					for o in operations:
						# For each operation, substitute it with a logical result value
						# Continue from here...
					# Try to get remaining operations of the same parenthesis
					operations = self.solveOperatorRegex.findall(p)


		return True

	def foward(self):
		# Algorithm (non-optimized)
		# For each rule
		#	For each assertment
		#		Get all matches of non-fired rules
		#	Check match list (respecting the rule order) and 
		#		fire the first one available, generating a new assertment.
		# Repeat with the updated assertment list until no new assertments was added.

		while match:
			match = None
			for r in self.rules:
				if not match:
					for a in self.assertments:
						if self._booleanLogicCheck(r, a):
							match = self._constructAssertment(r, a)
			self.assertments.append(match)
		return self.assertments


	def backward(self, hipothesis):


if __name__ == '__main__':