import sys
import re

class RBES:
	def __init__(self, filepath):
		self.assertions = []
		self.rules = []
		self.getParenthesisRegex = re.compile(r'\(([^\(\)]+)\)')
		self.solveOperatorRegex = re.compile(r'([^*+]+)([*+])([^*+]+)')
		self.separateResultRegex = re.compile(r'([^=]+)=([^\n]+)')
		self.substituteVariableRegex = re.compile(r'([^\(\?01*+]*)(\?[^\s]+)([^*+\)01]*)')
		
		getTokensRegex = re.compile(r'(A|R)\s*([^\n]+)\n?')

		with open(filepath, 'r') as file: 
			for line in file:
				tokens = getTokensRegex.match(line)
				if tokens:
					tokenType = tokens.group(1)
					tokenValue = tokens.group(2)

					if tokenType == 'A':
						self.assertions.append(tokenValue)
					elif tokenType == 'R':
						tokenValue = re.sub(r'\s+', ' ', re.sub('THEN', '=', 
							re.sub('OR', '+', re.sub('AND', '*', tokenValue))))
						self.rules.append(tokenValue)
					else:
						print('E: unkown token type \'' + tokenType + 
							'\'. Must be \'A\' (Assertion) or \'R\' (Rule). Ignoring it.\n')

	def _booleanLogicCheck(self, rule):
		aux = self.separateResultRegex.match(rule)
		requeriments = '(' + aux.group(1) + ')'
		outcome = aux.group(2)

		# Process rule with assertion
		tokens = 'start'
		who = ''
		while tokens:
			tokens = self.substituteVariableRegex.search(requeriments)
			if tokens:
				prefix = re.sub(r'[*+01()]', '', tokens.group(1))
				variable = tokens.group(2)
				sufix = re.sub(r'[*+01()]', '', tokens.group(3))

				subFlag = False
				for a in self.assertions:
					if not subFlag:
						findAssertion = re.search(re.sub(r'\s', '\s*', prefix + r'(.*)' + sufix), a)
						if findAssertion:
							subFlag = True
							who = findAssertion.group(1)
							requeriments = self.substituteVariableRegex.sub('1', requeriments, count=1)
				if not subFlag:
					requeriments = self.substituteVariableRegex.sub('0', requeriments, count=1) 

		# Solve boolean logic expression
		parenthesis = 'start'
		while parenthesis:
			# While there is remaining parenthesis
			parenthesis = self.getParenthesisRegex.search(requeriments)
			if parenthesis:
				parenthesis = parenthesis.group(1)
				# For each logic parenthesis, solve all operators
				operation = self.solveOperatorRegex.search(parenthesis)
				while operation: 
					# For each operation, substitute it with a logical result value
					operandA = bool(int(operation.group(1)))
					operator = operation.group(2)
					operandB = bool(int(operation.group(3)))

					result = '0'
					if operator == '+':
						# OR operator
						result = '1' if (operandA or operandB) else '0'
					elif operator == '*':
						# AND Operator
						result = '1' if (operandA and operandB) else '0'
					else:
						print('E: unknown operator \'' + operator + '\'.')

					# Subtitute on the current string
					parenthesis = self.solveOperatorRegex.sub(result, parenthesis, count=1)
					# Try to get remaining operations of the same parenthesis
					operation = self.solveOperatorRegex.search(parenthesis)
				requeriments = self.getParenthesisRegex.sub(parenthesis, requeriments, count=1)

		veracity = bool(int(requeriments))
		newAssertions = re.split(r'\*', re.sub(r'\s*\?[^\s]+\s*', who, outcome))

		return veracity, newAssertions

	def _constructAssertion(self, rule, assertion):
		return 'Test.'

	def foward(self, verbose=False):
		# Algorithm (non-optimized)
		# For each rule
		#	For each assertion
		#		Get all matches of non-fired rules
		#	Check match list (respecting the rule order) and 
		#		fire the first one available, generating a new assertion.
		# Repeat with the updated assertion list until no new assertions was added.

		defunct = [False] * len(self.rules)
		match = True
		i = 0
		while match:
			match = False

			if verbose:
				print('Iteration', i, ':', end=' ')
				i += 1
			for i in range(len(self.rules)):
				if not match and not defunct[i]:
					match, newAssertions = self._booleanLogicCheck(self.rules[i])
					if match:
						defunct[i] = True
						if verbose:
							print('Fired rule ', i)
			if match:
				for n in newAssertions:
					if not n in self.assertions: 
						self.assertions.append(n)
			elif verbose:
				print('No rules fired.')
		return self.assertions


	def backward(self, hipothesis):
		None

	def print(self):
		i = 0
		for a in self.assertions:
			print('A' + str(i) + ':', a)
			i += 1
		i = 0
		for r in self.rules:
			print('R' + str(i) + ':', r)
			i += 1


if __name__ == '__main__':
	system = RBES(sys.argv[1])
	print(system.foward(verbose=True))