#!/usr/bin/env python3

import sys
from Crypto.Util.number import *
import time

MEMSIZE = 2**16
regNames = ["r%d"%i for i in range(16)]
regNames.append('rip')
mem = {}
regs = {r:0 for r in regNames}
program = []
INPUT_BUFFER = []
OUTPUT_BUFFER = ""

DEBUG = 0

class IcicleError(Exception):
    pass

def prd(*args):
    if DEBUG:
        print(*args)

def reset():
    global mem, regs, program
    mem = {}
    regs = {r:0 for r in regNames}
    program = []

def c_insn():
    return program[regs["rip"]]

def runstr(s, inp=[], limit=600):
    global program, INPUT_BUFFER
    if inp != []:
        resetTest()
        INPUT_BUFFER = inp
    program = [line.strip() for line in s.split('\n')]
    prd(program)
    return run(inp != [], limit=limit)

def runfile(filename):
    global program
    with open(filename, 'r') as f:
        print("Running...")
        runstr(f.read())
        quit("Finished execution.", 0)

def run(test=False, limit=600):
    global regs, program, insns_map
    start = time.time()
    if test:
        insns_map['pr'] = prtest
        insns_map['readstr'] = readstrtest
        insns_map['readint'] = readinttest
    try:
        prd(regs["rip"])
        prd(program)
        while regs["rip"] < len(program):
            prd("Executing '"+c_insn()+"' at insn_pointer "+str(regs["rip"]))
            # prd(regs["r15"])
            execute(c_insn())
            if time.time()-start > limit:
                quit("Time limit of "+str(limit)+" seconds exceeded!", 1)
            regs["rip"] += 1
        if test:
            return OUTPUT_BUFFER
    except Exception as e:
        print("Unknown error occurred.")
        if DEBUG:
            raise e
        quit()

def parseInsn(insn):
    args = insn.split("#")[0].strip().split(" ")
    cmd = args[0]
    rest = " ".join(args[1:]).strip().split(", ")
    return [cmd]+rest

def execute(insn):
    if insn == '' or insn[-1] == ':' or insn[0] == "#":
        return
    args = parseInsn(insn)
    prd(args)
    insns_map[args[0]](*args[1:])

def quit(msg='', exitcode=1, test=False):
    if test:
        if exitcode == 0:
            print("ICICLE quitting with error code zero.")
            print("You shouldn't be seeing this.")
        if msg == '':
            msg = "Empty message in error"
        print("IcicleError:")
        print(msg)
        raise IcicleError(msg)
    if exitcode != 0:
        print("Error running line '", c_insn(), "' at insn pointer", regs["rip"])
    if msg == '':
        print("Quitting...")
    else:
        print(msg)
    exit(exitcode)

def setMem(addr, val):
    global mem
    if type(addr) != int:
        quit("Attempting to access invalid memory address "+str(addr))
    if addr < 0 or addr >= MEMSIZE:
        quit("Memory "+str(addr)+" out of bounds!")
    mem[addr] = val

def getMem(addr):
    global mem
    if type(addr) != int:
        quit("Attempting to access invalid memory address "+str(addr))
    if addr < 0 or addr >= MEMSIZE:
        quit("Memory "+str(addr)+" out of bounds!")
    if addr in mem:
        return mem[addr]
    mem[addr] = 0
    return 0

def getVal(val):
    if type(val) != str or len(val) == 0:
        quit("Bad value "+str(val)+" recieved!")
    if val.isdigit():
        return int(val)
    if val in regNames:
        return regs[val]
    if val[0] == '[' and val[-1] == ']':
        return getMem(getVal(val[1:-1]))
    if val[0] == '"' and val[-1] == '"':
        return val[1:-1]
    if val[0] == "'" and val[-1] == "'":
        return val[1:-1]
    quit("Bad value "+str(val)+" recieved!")

def assign(loc, val):
    global regs
    if type(loc) != str or len(loc) == 0:
        quit("Bad location "+str(loc)+" recieved!")
    if loc in regNames:
        regs[loc] = val
        return
    if loc[0] == '[' and loc[-1] == ']':
        setMem(getVal(loc[1:-1]), val)
    

def add(*args):
    a1 = getVal(args[1])
    a2 = getVal(args[2])
    if type(a1) != type(a2):
        a1 = str(a1)
        a2 = str(a2)
    assign(args[0], a1+a2)

def sub(*args):
    a1 = getVal(args[1])
    a2 = getVal(args[2])
    if type(a1) != int or type(a2) != int:
        quit("sub args not int!")
    assign(args[0], getVal(args[1])-getVal(args[2]))

def mult(*args):
    a1 = getVal(args[1])
    a2 = getVal(args[2])
    if type(a1) == str or type(a2) == str:
        quit("Both mult args are strings!")
    assign(args[0], getVal(args[1])*getVal(args[2]))

def div(*args):
    a1 = getVal(args[1])
    a2 = getVal(args[2])
    if type(a1) != int or type(a2) != int:
        quit("div args not int!")
    assign(args[0], getVal(args[1])//getVal(args[2]))

def mod(*args):
    a1 = getVal(args[1])
    a2 = getVal(args[2])
    if type(a1) != int or type(a2) != int:
        quit("mod args not int!")
    assign(args[0], getVal(args[1])%getVal(args[2]))

def andd(*args):
    a1 = getVal(args[1])
    a2 = getVal(args[2])
    if type(a1) != int or type(a2) != int:
        quit("and args not int!")
    assign(args[0], getVal(args[1])&getVal(args[2]))

def orr(*args):
    a1 = getVal(args[1])
    a2 = getVal(args[2])
    if type(a1) != int or type(a2) != int:
        quit("or args not int!")
    assign(args[0], getVal(args[1])|getVal(args[2]))

def xor(*args):
    a1 = getVal(args[1])
    a2 = getVal(args[2])
    if type(a1) == int and type(a2) == int:
        assign(args[0], getVal(args[1])^getVal(args[2]))
    else:
        a1 = long_to_bytes(a1).decode() if type(a1) == int else a1
        a2 = long_to_bytes(a2).decode() if type(a2) == int else a2
        assign(args[0], xorstr(a1, a2))

def xorstr(s1, s2):
    l = max(len(s1), len(s2))
    s1 = s1.encode()
    s2 = s2.encode()
    ret = ''
    for i in range(l):
        ret += chr(s1[i%len(s1)]^s2[i%len(s2)])
    return ret

def readint(*args):
    try:
        assign(args[0], int(input()))
    except ValueError as e:
        quit("Bad int input!")

def readstr(*args):
    assign(args[0], input())

def pr(*args):
    print(getVal(args[0]), end='', flush=True)

def resetTest():
    global INPUT_BUFFER, OUTPUT_BUFFER
    reset()
    INPUT_BUFFER = []
    OUTPUT_BUFFER = ""

def prtest(*args):
    global OUTPUT_BUFFER
    OUTPUT_BUFFER += str(getVal(args[0]))

def readinttest(*args):
    global INPUT_BUFFER
    if len(INPUT_BUFFER) == 0:
        quit("No more inputs!")
    try:
        assign(args[0], int(INPUT_BUFFER[0]))
        INPUT_BUFFER = INPUT_BUFFER[1:]
        # OUTPUT_BUFFER += "\n"
    except ValueError as e:
        quit("Bad int input!")

def readstrtest(*args):
    global INPUT_BUFFER
    if len(INPUT_BUFFER) == 0:
        quit("No more inputs!")
    assign(args[0], INPUT_BUFFER[0])
    INPUT_BUFFER = INPUT_BUFFER[1:]
    # OUTPUT_BUFFER += "\n"

def strint(*args):
    a1 = getVal(args[1])
    if type(a1) != str:
        quit("Attempting to convert non-string to int!")
    assign(args[0], bytes_to_long(bytes([ord(i) for i in a1])))

def intstr(*args):
    a1 = getVal(args[1])
    if type(a1) != int:
        quit("Attempting to convert non-int to string!")
    try:
        b = bytes.fromhex(hex(a1)[2:])
    except ValueError as e:
        if 'non-hexadecimal' not in str(e):
            raise e
        b = bytes.fromhex('0'+hex(a1)[2:])
    assign(args[0], ''.join([chr(i) for i in b]))

def revint(i):
    sign = 0 if not i else (1 if i>0 else -1)
    return sign*int(str(abs(i))[::-1])

def rev(*args):
    a1 = getVal(args[1])
    if type(a1) == int:
        ret = revint(a1)
    else:
        ret = a1[::-1]
    assign(args[0], ret)

def mov(*args):
    assign(args[0], getVal(args[1]))

def jump(*args):
    for i, insn in enumerate(program):
        if insn == args[0]+':':
            regs["rip"] = i
            return
    quit("Could not find label "+args[0]+"!")


def jz(*args):
    if getVal(args[0]) == 0:
        jump(args[1])

def jnz(*args):
    if getVal(args[0]) != 0:
        jump(args[1])

def jl(*args):
    if getVal(args[0]) < getVal(args[1]):
        jump(args[2])

insns_map = {"add": add,
             "sub": sub, 
             "mult": mult, 
             "div": div, 
             "mod": mod,
             "xor": xor, 
             "and": andd,
             "or": orr,
             "rev": rev,
             "mov": mov,
             "strint": strint,
             "intstr": intstr,
             "pr": pr,
             "readstr": readstr,
             "readint": readint,
             "j": jump,
             "jnz": jnz,
             "jz": jz,
             "jl": jl,
             } # also labels

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        quit("Usage: ./icicle.py [filename]", 0)

    reset()
    runfile(args[1])

