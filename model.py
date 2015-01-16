#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 10:06:28 2015
Project	:Python-Project
Version	:0.0.1
@author	:macrobull (http://github.com/macrobull)

"""



import numpy as np
from math import log


def digify(xs, ys, dual = True):
	rx, ry = [xs[0]], [ys[0]]
	for i in range(1, len(xs)):
		pred = ys[i] != ys[i-1]
		if np.iterable(pred): pred = np.any(pred)
		if pred:
			if dual:
				rx.append(xs[i])
				ry.append(ys[i-1])
			rx.append(xs[i])
			ry.append(ys[i])
	if dual:
		rx.append(xs[-1])
		ry.append(ys[-1])
	return np.array(rx), np.array(ry)

def multiRadix(codecs, col = 7, reverse = False, radix = 2, size = 32):
	for c in codecs:
		y = 0
		if not reverse: c = reversed(c)
		for i in c:
			y = y * radix + i

		if col == 0:
			yield y
			continue

		r = ''
		if col & 1:
			r += '0b'+ bin(y)[2:].zfill(int(log(size-1)/log(2))+1) + '\t'
		if col & 2:
			r += '0x'+ hex(y)[2:].zfill(int(log(size-1)/log(16))+1).upper() + '\t'
		if col & 4:
			r += str(y).zfill(int(log(size-1)/log(10))+1) + '\t'
		yield r.rstrip()


## Motor models

def stepBy1(ts):
	STATES = 10
	STEPS = 80
	DP = -4
	ts = (ts * STEPS)
	r = []
	for i in range(5):
		ms = ts % STATES
		r.append([1 if 0<=m<4 else -1 if 5<=m<9 else 0 for m in ms])
		ts += DP
	return np.array(r).T


def stepBy2(ts):
	STATES = 5
	STEPS = 40
	DP = -2
	ts = (ts * STEPS)
	r = []
	for i in range(5):
		ms = ts % STATES
		r.append([1 if 0<=m<2 else -1 if 3<=m<5 else 0 for m in ms])
		ts += DP
	return np.array(r).T


def hall80(ts):
	STATES = 10
	STEPS = 80
	DP = 6
	ts = (ts * STEPS)
	r = []
	for i in range(5):
		ms = ts % STATES
		r.append((ms<5).astype(int))
		ts += DP
	return np.array(r).T

def hall80_bad(ts):
	STATES = 10
	STEPS = 80
	DP = 6
	ts = (ts * STEPS)
	r = []
	for i in range(5):
		ms = (ts + (np.random.rand()-0.5) * 2) % STATES
		if i==1 or i== 3:
			r.append((ms<6+(np.random.rand()-0.5) * 2).astype(int))
		else:
			r.append((ms<5+(np.random.rand()-0.5) * 2).astype(int))
		ts += DP
	return np.array(r).T

def hall60(ts):
	STATES = 10
	STEPS = 60
	DP = 4
	ts = (ts * STEPS)
	r = []
	for i in range(5):
		ms = ts % STATES
		r.append((ms<5).astype(int))
		ts += DP
	return np.array(r).T

def initHall80StateList():
	ts = np.linspace(0, 1/8, 20, endpoint = False)
	cs = hall80(ts)
	cs = multiRadix(cs, col = 0)
	_, r = digify(ts, list(cs), dual = False)
	return list(r)

hall80StateList = initHall80StateList()

def initStepBy1StateList():
	ts = np.linspace(0, 1/8, 20, endpoint = False)
	ss = stepBy1(ts)
	_, r = digify(ts, ss, dual = False)
	return list(r)

stepBy1StateList = initStepBy1StateList()

#
#def stepEncode(ss, reverse = False):
#	r = 0
#	if not reverse: ss = reversed(ss)
#	for s in ss:
#		r = r*3 + s + 1
#	return r

def hamming(a, b):
	s = 0
	d = a ^ b
	while d:
		s += 1 & d
		d = d >> 1
	return s

if __name__ == '__main__':

	mm = np.zeros((32, 10)) #Probability model

	for i in range(10):
		print(stepBy1StateList[i], hall80StateList[i])
		mm[hall80StateList[i], stepBy1StateList[i]] = 1




