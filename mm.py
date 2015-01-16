#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 12:54:47 2015
Project	:Python-Project
Version	:0.0.1
@author	:macrobull (http://github.com/macrobull)

"""

import numpy as np
from model import *
from math import exp

def pdf0(d):
	return 1/(1+d)

def pdf1(d):
	return exp(-d)

def pdf2(d):
	if d == 0: return 0.4
	if d == 1: return 0.4
	if d == 2: return 0.2
	return 0

def pdf3(d):
	if d == 0: return 0.6
	if d == 1: return 0.2
	if d == 2: return 0.2
	return 0


def build_mm_priori():
	mm = np.zeros((32, 10))
	for h in range(32):
		for s in range(10):
			mm[h, s] = pdf3(hamming(h, hall80StateList[s])) # By statistics
	return mm

def build_rmm(mm):
	rmm = np.zeros((32, 10), dtype = np.uint8)
	for ch in range(32):
		for cs in range(10):
			p = q = 0
			for s in range(10):
				p1 = mm[ch, s] * pdf2((s - cs)%10) # By theory
				if p1 > p:
					p = p1
					q = s
			rmm[ch, cs] = q
	return rmm

def genCode(rmm):
	dim0, dim1 = rmm.shape
	arr = repr(rmm).replace('[','{').replace(']','}')
	arr = arr[arr.index('{'):arr.index('dtype')-2]
	print("""
	const uint8_t RMM[%(dim0)d, %(dim1)d] = %(arr)s;
	state = RMM[position, state];
	""" % locals())


mm = build_mm_priori()
print( (mm*100).astype(int) )
print('=' * 40)

rmm = build_rmm(mm)
print(rmm)
print('=' * 40)

if __name__ == '__main__':
	genCode(rmm)
