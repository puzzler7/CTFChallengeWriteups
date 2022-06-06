# Unintended Solves for RIaaS and CaaS

### RIaaS

During this CTF, many of the websites and remote hosts went up and down very quickly, with mods frequently pinging everyone to update the links. During the frenzy that was the second wave of challenges, one of these messages was that RIaaS was being hosted on [https://RIaaS--abhinavkumar65.repl.co:8000/](https://RIaaS--abhinavkumar65.repl.co:8000/) (link now dead).

However, unless you pay for the pro version, Replit hosts all of your projects as open source. Thus, I was just able to go to Abhinav's Replit profile [here](https://replit.com/@ABHINAVKUMAR65), open the corresponding project, and view the flag file at [https://replit.com/@ABHINAVKUMAR65/RIaaS?v=1#flag](https://replit.com/@ABHINAVKUMAR65/RIaaS?v=1#flag) (link now dead).

I notified the mods of this, who took down the website immediately and re-hosted it on a traditional server. However, I wasn't done.

### CaaS

CaaS was a simple website that allowed you to view the data at a given URI. This included `file://` URIs, meaning that if you knew the path to a file on the server (like `file:///etc/passwd`), the website would leak it to you. However, I didn't know what path the files were at.

The intended was apparently to just guess that the directory was called `/chall` (to quote the challenge dev, "[because] /chall is obvious"). However, you could also bypass this, as `/proc/self/cwd` points to your current working directory. I did neither of these things when I first looked at the challenge, and resolved to come back to it later.

How does this relate to the RIaaS source leak? Well, the files there included configuration and setup files, like the Dockerfile used to host the website.

```docker
FROM python:slim

RUN mkdir -p /chall && mkdir -p /chall/templates && pip3 install flask
WORKDIR /chall

COPY main.py flag /chall/
COPY templates /chall/templates

EXPOSE 8000
ENTRYPOINT ["python", "main.py"]
```

This says that the files are hosted at `/chall`. That, combined with the fact that the provided file is called `challenge-redacted.py` means that the actual challenge source is likely at `/chall/challenge.py`. Requesting the URI `file:///chall/challenge.py` yields the following source:

```py
from flask import Flask, request, render_template, render_template_string, redirect
import subprocess
import urllib
app = Flask(__name__)
def blacklist(inp):
    blacklist = ['{{','}}','import','os','system','[','\x5f',']']
    for b in blacklist:
        inp = inp.replace(b, '')
    return inp
@app.route('/')
def main():
    return redirect('/curl')

@app.route('/curl',methods=['GET','POST'])
def curl():
    if request.method == 'GET':
        return render_template('curl.html')
    elif request.method == 'POST':
        inp = request.values['curl']
        #print(inp)
        
        #p = subprocess.Popen(["python3", "admin.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #print('a')
        def admin():
            return inp
        print(admin()) 
        webUrl = urllib.request.urlopen(f'{inp}')
        data = webUrl.read()
        #print(data)
        #data = data.replace(b'\n',b'\r')
        return f'Am Admin, Going to visit "{inp}" fingers crossed, Result:{data}</p>'
@app.route('/such_a_1337_flag_file_th4t_n0_one_c4n_defnitely_f1nd_hahahaha_lollll_nooob_xDDDDDDd.txt')
def flag():
    return render_template('such_a_1337_flag_file_th4t_n0_one_c4n_defnitely_f1nd_hahahaha_lollll_nooob_xDDDDDDd.txt')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

From there, we can see the secret endpoint to visit - `/such_a_1337_flag_file_th4t_n0_one_c4n_defnitely_f1nd_hahahaha_lollll_nooob_xDDDDDDd.txt`, which yields the flag `n00bz{4rb1t4ry_f1le_re4d_us1ng_curl_ftw!}`.
