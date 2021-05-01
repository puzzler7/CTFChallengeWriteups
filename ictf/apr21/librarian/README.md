# ReDoS

**Categories:** Pwn

**Description:** Welcome to the ImaginaryCTF Library! Can you get the flag? Connect at `nc stephencurry.ctfchallenge.ga 5003`.

**Attachments:** `librarian`

This was the final challenge of Round 9 of ICTF. Opening the binary in Ghidra, we can see that it first asks for a random number as a password. However, the PRNG is not seeded, so the numbers are deterministic. I generated the first 10 random numbers with `crand.c` and used that in my script.

From there, we can see that the binary calls `gets` if a number not between 1 and 5 is entered, letting us perform a ROP. The stack is not executable, but there is no stack canary. From here, it's a simple ROP. Because the binary does not call system, we need to leak the libc that the binary is using.

To do this, we return to `puts`, printing the address of `gets`. We get `0x7fcfb9cf4af0` as the address. Plugging that into the [libc database](https://libc.blukat.me/) yields 3 different libc files. However, they all have the same offsets, so any of them will work.

Once we have leaked the libc base address, we know the relative offsets of the `system` function, and the string "/bin/sh". We then return to this, getting a shell, and we can simply cat the flag.

**Overview of ROP Chains:**
```
     main      -> puts(addr_of_gets) ->   main  ->  system("/bin/sh")
where we start    to find the libc/   to BOF again   gets a shell
                get the libc base addr
```

**Flag:** `ictf{w3lcome_t0_th3_ictf_l1brary!}`