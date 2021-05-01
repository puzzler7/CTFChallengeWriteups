# Just in Time 1

**Categories:** Misc

**Description:** Yet another guessy challenge... Can you guess all the random numbers in time?

**Attachments:** lookatthetime.py, netcat

This was one of the challenges I submitted, once again stolen from a previous CTF I've attended (although I cannot recall which one for the life of me). Once again, all code is mine.

To solve, we notice that the random numbers are seeded off of the time, and while we aren't given the seed, we do know the first number generated with the seed from the hint. While network delays and the `time.sleep(random.random())` mean that we can't also seed off of the time and get the same result, we can try times near the current time as the seed, until one of them generates the hint number. At this point, we can simply submit the other numbers, and get the flag.

**Flag:** `ictf{t1ck_t0ck_1t5_g3++ing_l@t3}`