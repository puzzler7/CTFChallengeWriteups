# ReDoS

**Categories:** Misc/Reversing

**Description:** I've made a Super Secure Server(tm) with no vulnerabilities whatsoever. Can you DOS my server to prove me wrong?

Note: do **NOT** DDOS the server.

**Points:** 75

**Attachments:** redos.py, netcat

This was one of the challenges I submitted, which was not stolen from a previous CTF, but inspired by a justCTF challenge that had a ReDoS vuln (but no similarities otherwise). In doing research for the challenge, I learned that at one point, the official email regex had a clause that suffered from catastrophic backtracking.

To solve, we notice that we have to generate a `TimeoutError`. The only way this can be done is by causing the `validateEmail()` function to take more than 10 seconds to run. As this function only contains a regex match, searching for regex vulnerabilities will pull up info about catastrophic backtracking. The email regex has a catastropic backtracking vuln in the clause `((gmail)+)*`. Repeating `gmail` in a failing regex will cause the regex to take exponential time to evaluate, increasing with the number of `gmail`s. Thus, to solve, make an account, enter the email `2@gmailgmailgmailgmailgmailgmailgmailgmailgmailgmailgmailgmailgmailgmailgmailgmailgmailgmailgmailgmailgmailgmailgmailgmailgmailgmail2.com` or similar, and wait for 10 seconds to get the flag.

One more note is that the admin password is literally "REDACTED", so users can login as admin (which, of course, doesn't get the flag).

**Flag:** `ictf{t1ck_t0ck_1t5_g3++ing_l@t3}`