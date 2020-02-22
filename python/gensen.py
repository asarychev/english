import sys
from random import random
from enum import Enum, unique
from lark import Lark

class Nominal:
	def __init__(self, p = 1, indef=.5, right=0.3, plural=.5, left=.5):
		''
		if random() < p:
			self.core = 'visit'
		else:
			self.core = None
			return

		self.the = random() < indef

		self.left = []
		while random() < left:
			self.left.append('visit')

		self.plural = random() < plural

		self.right = Nominal(right)

	def __str__(self):
		if self.the:
			res = 'the '
		elif not self.plural:
			res = 'a '
		else:
			res = ''

		for t in self.left:
			res += f"{t} "

		res += self.core

		if self.plural:
			res += 's'

		if self.right:
			res += f" of {self.right}"

		return res

	def __bool__(self):
		return self.core is not None

class VerbPhrase:
	def __init__(self, es):
		''
		self.es = es
		self.core = 'visit'

	def __str__(self):
		res = self.core
		if not self.es:
			res += 's'
		return res

class Sentence:
	def __init__(self):
		''
		self.p1 = Nominal()
		self.p2 = VerbPhrase(self.p1.plural)
		self.p3 = Nominal(.8)

	def __str__(self):
		res = f"{self.p1} {self.p2}".capitalize()
		if self.p3:
			res += ' '
			res += str(self.p3)

		return res + '.'

# print(sys.version)

@unique
class Parts(Enum):
	V = 1
	WHO = 2
	OF_WHAT = 3

class NP(list):
	''
	def __init__(self):
		self.plural = False

class VP(list):
	''

def parseNP(ss, of=False):
	res = NP()
	tt = []

	try:
		i = ss.index('of')
		tt = parseNP(ss[i+1:], of=True)
		if not tt:
			return None
		ss = ss[:i]
	except ValueError:
		pass

	art = ''

	if ss and ss[0] in ('a', 'the'):
		art = ss.pop(0)

	if not ss:
		return None

	n = ss.pop()

	if of:
		t = Parts.OF_WHAT.value
	else:
		t = Parts.WHO.value

	if n == 'visit':
		if art == '':
			return None
		res.append(t)
	elif n == 'visits':
		if art == 'a':
			return None
		res.plural = True
		res.append(-t)
	else:
		return None

	res.extend(tt)
	return res

def parseVP(ss, plural):
	if len(ss) != 1:
		return None

	v = ss.pop()
	if not v.startswith('visit'):
		return None
	else:
		return ['V']
	
def splitVP(s):
	s = str(s).lower()
	if s.endswith('.'):
		s = s[:-1]
	else:
		return

	ss = s.split()
	for i in range(1, len(ss)):
		p1 = parseNP(ss[:i])
		if not p1:
			continue

		for j in range(i+1, len(ss)):

			vp = ss[i:j]

			p2 = parseVP(vp, p1.plural)
			if p2 is None:
				continue

			p3 = parseNP(ss[j:])
			if p3 is None:
				continue

			yield p1 + p2 + p3

def parse(s):
	res = []
	for t in splitVP(s):
		print(t)

s = Sentence()

print(s)

parse('A visit of a visit visits a visit of visits of the visit.')