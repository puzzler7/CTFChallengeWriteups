# Blind Shell

**Categories:** Misc/Pyjail

**Description:** Normally once you have a shell, you win. Here, you already start with a shell - can you find your way to the flag?

**Attachments:** blind.py, netcat

This was one of the challenges I submitted, almost completely stolen from kksctf (making this an OSINT challenge, as a google search for "CTF Blind Shell" yields [this](https://ctftime.org/writeup/25338) writeup). I will note that all the code is my own.

To solve, we can notice that `cat flag.txt` is successful, meaning that the file exists. We can further notice that grepping for the flag format is successful, and that the flag is at the beginning of the file, with `grep ictf{ flag.txt` and `grep ^ictf{ flag.txt`. We can write a script to iterate through all printable characters, guess the next character until one is found, and then progress to the next character.

`x.py` in this directory does this. It's important to note that simply adding the character to the string to test won't work, as some characters have a special meaning in regex, so I test the new character inside brackets (`[]`) to make sure it gets interpreted literally.

**Flag:** `ictf{g01n8_1n_bl!nd?n0t_@_pr0bl3m!}`