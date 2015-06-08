'''
Peter LaFontaine
U50242700
9/22/14
'''
import math
import re

def vxor(v1, v2):
	if v1 == True  and v2 == True:  return False
	if v1 == True  and v2 == False: return True
	if v1 == False and v2 == True:  return True
	if v1 == False and v2 == False: return False

def vnot(v1):
	if v1 == True: return False
	if v1 == False: return True


def tokenize(termList, synStr):
	#print('test')
	regEx = '|'.join(termList)
	#print(synStr)
	tokens = [t for t in re.split(r"(\s|\*|\+|\(|\)|\,|\;|:=|regEx)",synStr)]
	return [t for t in tokens if not t.isspace() and not t == ""]

#2a
def evalTerm(env, t):
	if type(t) == dict:
		for label in t:
			children = t[label]
			if label == 'Number':
				return children[0]
			elif label == 'Log':
				f = children[0]
				v = evalTerm(env,f)
				x = math.log(v,2)
				return math.floor(x)
			elif label == 'Plus':
				f = children[0]
				v = evalTerm(env,f)
				f1 = children[1]
				v1 = evalTerm(env,f1)
				return v + v1
			elif label == 'Mult':
				f = children[0]
				v = evalTerm(env,f)
				f1 = children[1]
				v1 = evalTerm(env,f1)
				return v * v1
			elif label == 'Parens':
				f = children[0]
				v = evalTerm(env,f)
				return v
			elif label == 'Variable':
				n = children[0]
				if n in env:
					return env[n]
				
#2b
def evalFormula(env, t):
	

	if type(t) == dict:
		for label in t:
			children = t[label]
			if label == 'Xor':
				f = children[0]
				v = evalFormula(env, f)
				f1 = children[1]
				v1 = evalFormula(env,f1)
				return vxor(v,v1)
			elif label == 'Parens':
				f = children[0]
				v = evalFormula(env,f)
				return v
			elif label == 'Not':
				f = children[0]
				v = evalFormula(env,f)
				return vnot(v)
			elif label == 'Variable':
				n = children[0]
				if n in env:
					return env[n]
				else:
					return None
					exit()
			else:
				return evalTerm(env,t)


	elif type(t) == str:
		if t == 'True':
			return True
		if t == 'False':
			return False


#2c
def execProgram(env, s):
	

	if type(s) == dict:
		for label in s:
			if label == 'Print':
				children = s[label]
				f = children[0]
				x = children[1]
				v = evalFormula(env, f)
				(env, y) = execProgram(env, x)
				return (env, [v]+y)

			elif label == 'Assign':
				children = s[label]
				f = children[0]['Variable'][0]
				v = children[1]
				x = children[2]
				env[f] = evalFormula(env,v)
				(env, u) = execProgram(env, x)
				return (env,u)

			elif label == 'If':
				children = s[label]
				c = children[0]
				c1 = children[1]
				c2 = children[2]
				if c == False:
					env1 = env
					(env2,f1) = execProgram(env1,c2)
					return (env2,f1)
				else:
					env1 = env
					(env2, f1) = execProgram(env1,c1)
					(env3, f2) = execProgram(env2,c2)
					return (env3, f1+f2)

			elif label == 'While':
				children = s[label]
				c = children[0]
				c1 = children[1]
				c2 = children[2]
				if eval(env,c) == False:
					env1 = env
					(env2,f1) = execProgram(env1,c2)
					return (env2,f1)
				while eval(env,c):
					env1 = env
					(env2, f1) = execProgram(env1,c1)
					(env3, f2) = execProgram(env2,c2)
					return (env3, f1+f2)

	if type(s) == str:
			if s == 'End':
				return (env, [])


def eval(env, f):
	x = evalFormula(env,f)
	if x != None:
		return x
	return evalTerm(env,f)

#2d
tokList = ["log","xor","true","not","false","(",")","+","*","print","assign",
"End","if","while",",",";",":="," "]
def interpret(s):
	x = tokenize(tokList, s)
	(parse, ans) = program(x)
	(e1,b) = execProgram({}, parse)
	return b

