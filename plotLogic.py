#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 10:06:28 2015
Project	:Python-Project
Version	:0.0.1
@author	:macrobull (http://github.com/macrobull)

"""

from pylab import *

from model import *

import mm


XMAX = 2/8
rcParams['axes.color_cycle'] = rcParams['axes.color_cycle'][:5]

def expected(sp = 111, bg = False):
	if bg:
		kwargs = dict(lw = 2.0, alpha = 0.4)
	else:
		subplot(sp, title='Expected')
		kwargs = dict()

	hs = hall80(ts)
	for i, ys in enumerate(hs.T):
		t1, y1 = digify(ts, ys)
		plot(t1, y1*2 + i*5 - 30, label = 'Hall_{}'.format(i), **kwargs)

	ss = stepBy1(ts)
	for i, ys in enumerate(ss.T):
		t1, y1 = digify(ts, ys)
		plot(t1, y1*2 + i*5, label = 'State_{}'.format(i), **kwargs)

	if not bg:
		h1 = multiRadix(hs, col = 2)
		t1, h1 = digify(ts, list(h1), dual = False)
		p = np.where(t1>=XMAX)[0][0] + 2
		xticks(t1[:p], h1[:p], rotation = 70)
		xlim(0, XMAX)
		legend(loc = 'best')

def simulation(hall_func = hall80, sp = 111, poster = False):
	subplot(sp, title=hall_func.__name__)

	hs = hall_func(ts)
	for i, ys in enumerate(hs.T):
		t1, y1 = digify(ts, ys)
		plot(t1, y1*2 + i*5 - 30, label = 'Hall_{}'.format(i))

	if poster:
		mm1 = zeros(mm.mm.shape, dtype = int)
		hs1 = list(multiRadix(hs, col = 0))
		for i in range(len(ts)):
			mm1[hs1[i], int(ts[i]%(1/8)*(10*8))] += 1
		global mm1, rmm
		rmm = mm.build_rmm(mm1)
	else:
		rmm = mm.rmm

	state = 0
	ps = []
	for i in range(len(ts)):
		h = list(multiRadix([hs[i]], col = 0))[0]
		state = rmm[h, state]
		ps.append(state)

	ss = np.array(stepBy1StateList)[ps]
	for i, ys in enumerate(ss.T):
		t1, y1 = digify(ts, ys)
		plot(t1, y1*2 + i*5, label = 'State_{}'.format(i))

	h1 = multiRadix(hs, col = 2)
	t1, h1 = digify(ts, list(h1), dual = False)
	p = np.where(t1>=XMAX)[0][0] + 2
	xticks(t1[:p], h1[:p], rotation = 70)
	xlim(0, XMAX)
#	legend(loc = 'best')



ts = linspace(0, 2, 480, endpoint = False)

#figure()
#expected()
figure()
#simulation(sp = 121)

hs_bad = hall80_bad(ts)

simulation(lambda ts:hs_bad, sp = 121)
expected(bg = True)
simulation(lambda ts:hs_bad, sp = 122, poster = True)
expected(bg = True)



show()