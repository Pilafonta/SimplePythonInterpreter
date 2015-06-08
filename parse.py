'''
Peter LaFontaine
U50242700
9/22/14
'''
import re
from math import log,floor

#1a
def number(tokens):
    if re.match(r"^(-?[0-9]*)$", tokens[0]):
        return (int(tokens[0]), tokens[1:])


def variable(tokens):
	x = tokens[0]
	if x[0].isupper() == True or x[0].isdigit() == True:
		return None
	if re.match(r"[a-zA-Z0-9]+", tokens[0]):
		#print({"Variable": [tokens[0]]}, tokens[1:])
		return tokens[0], tokens[1:]


#1b
def formula(tokens):
	(e1, tokens) = left(tokens)
	if tokens != [] and tokens[0] == 'xor':
		(e2, tokens) = formula(tokens[1:])
		return ({'Xor':[e1,e2]}, tokens)
	
	return (e1,tokens)


def left(tokens):
	if tokens[0] == 'true':
		return ('True', tokens[1:])

	if tokens[0] == 'false':
		return ('False', tokens[1:])

	if tokens[0] == 'not' and tokens[1] == '(':
		(e1, tokens) = formula(tokens[2:])
		if tokens[0] == ')':
			return ({'Not':[e1]}, tokens[1:])
	
	if tokens[0] == '(':
		(e1, tokens) = formula(tokens[1:])
		if tokens[0] == ')':
			return ({'Parens':[e1]},tokens[1:])

	r = variable(tokens)
	if not r is None:
		(e5, tokens) = r
		return ({'Variable':[e5]}, tokens[0:])


#1c
def term(tokens):
	(e1, tokens) = factor(tokens)
	if tokens != [] and tokens[0] == '+':
		(e2, tokens) = term(tokens[1:])
		return ({'Plus':[e1,e2]}, tokens)
	
	return (e1,tokens)

def factor(tokens):

	#print('test2')
	(e1, tokens) = leftFactor(tokens)
	if tokens != [] and tokens[0] == '*':
		(e2, tokens) = factor(tokens[1:])
		return ({'Mult':[e1,e2]}, tokens)
	return (e1,tokens)


def leftFactor(tokens):
	if tokens[0] == 'log' and tokens[1] == '(':
		(e1,tokens) = term(tokens[2:])
		if tokens[0] == ')':
			return ({'Log':[e1]}, tokens[1:])


	if tokens[0] == '(':
		(e1, tokens) = term(tokens[1:])
		if tokens[0] == ')':
			return ({'Parens':[e1]},tokens[1:])

	r = number(tokens)
	if not r is None and tokens[0].isdigit() == True:
		(e3,tokens) = r
		return ({'Number':[e3]}, tokens[0:])

	j = variable(tokens)
	if not j is None and type(tokens[0]) == str:
		(e4,tokens) = j
		return({'Variable':[e4]}, tokens[0:])



#1d

def expression(tokens):
	if tokens[0] == 'true' or tokens[0] == 'false' \
	or tokens[0] == '(' or tokens[0] == 'not' or tokens[1] == 'xor':
		return formula(tokens)
	else:
		return term(tokens)

def program(tokens):
	if tokens:
		if tokens[0] == 'print':
			(e1,tokens) = expression(tokens[1:])
			if tokens[0] == ';':
				(e2,tokens) = program(tokens[1:])
				return ({'Print': [e1,e2]}, tokens)

		if tokens[0] == 'assign':
			(e1,tokens) = factor(tokens[1:])
			if tokens[0] == ':=':
				(e2,tokens) = expression(tokens[1:])
				if tokens[0] == ';':
					(e3,tokens) = program(tokens[1:])
					return ({'Assign':[e1,e2,e3]}, tokens)

		if tokens[0] == 'if':
			(e1,tokens) = expression(tokens[1:])
			if tokens[0] == '{':
				(e2,tokens) = program(tokens[1:])
				if tokens[0] == '}':
					(e3,tokens) = program(tokens[1:])
					return ({'If': [e1,e2,e3]},tokens)

		if tokens[0] == 'while':
			(e1,tokens) = expression(tokens[1:])
			if tokens[0] == '{':
				(e2,tokens) = program(tokens[1:])
				if tokens[0] == '}':
					(e3,tokens) = program(tokens[1:])
					return ({'While': [e1,e2,e3]},tokens)

	return ('End',tokens)
