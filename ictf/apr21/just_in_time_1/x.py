#!/usr/bin/env python3

from pwn import *
import time
import random

local = 1

def get_process():
	if local:
		p = process(['python3', 'lookatthetime.py'])
	else:
		p = remote("oreos.ctfchallenge.ga", 7331)
	return p

def test_time(t, val):
	random.seed(round(t, 2))
	return random.randint(0, 1000000000) == val

def exploit():
	start = round(time.time(), 2)
	offset = -10
	p = get_process()
	p.recvuntil(b'hint: ')
	val = int(str(p.recvline())[2:-3])
	print(val)
	win = 0
	while not win:
		win = test_time(start+offset, val)
		offset += .01
		offset = round(offset, 2)
		print(offset)
	for i in range(3):
		val = int(random.randint(0, 1000000000))
		print(val)
		p.sendline(str(val))
		print(p.recv())
	time.sleep(.1)
	print(p.recv())

if __name__ == '__main__':
	exploit()