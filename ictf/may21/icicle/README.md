# ICICLE
## Imaginary Ctf Instruction Collection for Learning assEmbly

> Introducing ICICLE! It's a programming challenge, so I didn't want to use an existing language and give some people an unfair advantage, so I made my own! See the spec and implement an interpreter to run the provided file, and get the flag.

This month, I made a series of programming challenges in which players were tasked with writing an interpreter to match the provided spec. Two ICICLE challenges were released, and more are on the way (of varying types).

There are a number of files provided. `chall1.s` and `chall2.s` are the challenge files for the two released challenges. `old_icicle.py` and `icicle.py` are both ICICLE interpreters that can execute ICICLE files with `python3 icicle.py [filename]`. `old_icicle.py` was the first interpreter that I wrote, while `icicle.py` was my object-oriented rewrite, after seeing some of the interpreters people made. `spec_v2.md` is the spec for the language. `bf_interp.py` is a functional (but very slow) Brainfuck interpreter, with some parameters like cell size and tape length customizable.

The first challenge just takes a string, xors it with several words (the words "You should really write the interpreter instead of doing this reversing! This is the first in a series." encoded a few different ways), and prints the result, which should be the flag. This was relatively easy to reverse (and indeed, many people did). The first version of the spec did not include memory or jumps/instruction pointer.

The second challenge has several thousand lines to set up a linked list of linked lists. The length of each linked list is the ASCII code of a letter. The lengths are recursively measured, converted to a string, and printed. To my knowledge, only one person (StealthyDev) solved this without an interpreter.

Quick shoutout to @StealthyDev and @RobinJadoul on Discord for testing and providing great feedback on these.