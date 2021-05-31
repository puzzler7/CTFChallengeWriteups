# Brainfuck interpreter

main:
mov r13, 4294967296 # cell size
# bf is usually 8 bit cells, but this allows for configuration
# for 8 bit, replace the number above with 256

mov r12, 30000 # tape size
mov r11, 0 # tape pointer
intstr r9, 10 #newline, for debug prints
pr "Enter brainfuck code: "
readstr r0
rev r0, r0
strint r0, r0
# using r0 as insns to execute, and r1 as insns that have been executed

# [43, 44, 45, 46, 60, 62, 91, 93] for +,-.<>[]
loop:
jz r0, end
mod r2, r0, 256 #r2 is current insn
div r0, r0, 256
mult r1, r1, 256
add r1, r1, r2

# prints each instruction as it's executed
# intstr r2, r2
# pr r2
# pr r9
# strint r2, r2

sub r2, r2, 43
jnz r2, notplus
#plus
add [r11], [r11], 1
mod [r11], [r11], r13
j loop
notplus:
sub r2, r2, 1
jnz r2, notcomma
#comma
readstr [r11]
strint [r11], [r11]
mod [r11], [r11], r13
j loop
notcomma:
sub r2, r2, 1
jnz r2, notminus
#minus
sub [r11], [r11], 1
mod [r11], [r11], r13
j loop
notminus:
sub r2, r2, 1
jnz r2, notdot
#dot
intstr [r11], [r11]
pr [r11]
strint [r11], [r11]
j loop
notdot:
sub r2, r2, 14
jnz r2, notlt
#less than
sub r11, r11, 1
mod r11, r11, r12 #memory wraps around if you walk off the tape

j loop
notlt:
sub r2, r2, 2
jnz r2, notgt
#greater than
add r11, r11, 1
mod r11, r11, r12

j loop
notgt:
sub r2, r2, 29
jnz r2, notrb
#right bracket
jnz [r11], loop
# need to skip the loop if zero
mov r10, 1
moveforward:
mod r2, r0, 256
div r0, r0, 256
mult r1, r1, 256
add r1, r1, r2
sub r2, r2, 91
jnz r2, notrbloop
add r10, r10, 1
j moveforward
notrbloop:
sub r2, r2, 2
jnz r2, moveforward
sub r10, r10, 1
jz r10, loop
j moveforward

notrb:
sub r2, r2, 2
jnz r2, unknown
#left bracket
jz [r11], loop
# need to loop again if not zero
mov r10, 0
movebackward:
mod r2, r1, 256
div r1, r1, 256
mult r0, r0, 256
add r0, r0, r2
sub r2, r2, 91
jnz r2, notrbback
sub r10, r10, 1
jz r10, loop
notrbback:
sub r2, r2, 2
jnz r2, movebackward
add r10, r10, 1
j movebackward

unknown:
pr "Unknown insn ("
add r2, r2, 93
intstr r2, r2
pr r2
pr ") recieved."
intstr r2, 10
pr r2
j loop


end:
pr r9
pr "Finished Execution"