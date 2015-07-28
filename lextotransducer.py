"""
Logic:
push all keys onto a list
pop the first key off into a new list
grab its first element
iterate through the stack and grab any keys with the
same first element into that list
once complete, repeat steps
-- now all parsed into first elements
successively do that through each list (2nd -> last element)
	when reach last element of that key add its value from the lexR dictionary to the rule (final state)
"""

"""
Code Comments:
1. My lex to transducer has a start category of the empty string, denoted ''
2. My rules are named as the string up to the index of the parse thus far -- therefore, the tuple on the
right hand side of my rules contains elements of the following type: (terminalNode, rule). For example,
('r', ('E', 'rE'), ()) refers to: "rule('r') -> terminalNode('E') rule('rE')" with an output of nothing.
"""

"""
helper calculates the probabilty to make lexToTransducer a probabilistic transducer
"""


lexR = {
('r', 'E', 'd') : [('read', 'Jc*,Jd*', '12A,2B,2C,6A,12A,13A,15A,15B,16B', 88000),
('red', 'M6%,OE%', '1', 86272)] ,
('r', 'i', 'd') : [('read', 'J5*,Ki%', '12A,2B,2C,6A,12A,13A,15A,15B,16B', 88000),
('reed', 'M6%', '1', 8336)] ,
}

def lexToTransducer(lexR):
	transducer = [ [], #Lexicon
					[], #Rules Declarations
					[], #Rules
					'' ] #Start Rule
	
	keysList = lexR.keys()
	listOfWork = [(keysList, 0)] #initialize stack of work to do
	while len(listOfWork) > 0: #while there are still prefixes to parse
		wkList = listOfWork[0][0]
		while len(wkList) > 0:
			nextLvl = []
			checkKey = wkList.pop()
			checkIndex = listOfWork[0][1]			
			if len(checkKey) == checkIndex:
				output = lexR[checkKey]
				ruleName = ''.join(checkKey)
				transducer[2].append((ruleName, (), output))
				if ruleName not in transducer[1]:
					transducer[1].append(ruleName)
			else:
				nextLvl.append(checkKey)	
				prefixVal = checkKey[checkIndex]
				ruleName = ''.join(checkKey[0:checkIndex])
				nextCheckIndex = checkIndex + 1
				nextRule = ''.join(checkKey[0:nextCheckIndex])
				if ruleName not in transducer[1]:
					transducer[1].append(ruleName)
				transducer[2].append((ruleName, (prefixVal, nextRule), ()))
				if prefixVal not in transducer[0]:
					transducer[0].append(prefixVal)
				for k in wkList: #now add anymore with same value at tpleIndexCounter
					if len(k) == checkIndex:
						output = lexR[k]
						ruleName = ''.join(k)
						transducer[2].append((ruleName, (), output))
						if ruleName not in transducer[1]:
							transducer[1].append(ruleName)
					else:
						if k[checkIndex] == prefixVal:
							nextLvl.append(k)
							wkList.remove(k)
				listOfWork.append((nextLvl, checkIndex+1)) #finished grabbing all keys with same value at tpleIndexCounter, add it to list of work
		listOfWork.pop(0) #finished parsing that level, remove it from the stack
	return transducer



