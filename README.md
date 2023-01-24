# yahpot
Yet Another HTTP(S) HoneyPot

Simple, under 90 line, yet functional honeypot with syslog and file-based logging. 

usage: yahpot.py [-h] [-t {http,https}] [-d DECOY] [-f FILE] [-l LOG] [-p PORT] [-k KEYFILE] [-c CERTFILE]

Yet Another HTTP(S) HoneyPot

options:
  -h, --help            show this help message and exit
  -t {http,https}, --type {http,https}
                        Type of server - 'http|https'
  -d DECOY, --decoy DECOY
                        Decoy to use - (see /templates/ directory)
  -f FILE, --file FILE  File to write log to (default 'yahpot.log')
  -l LOG, --log LOG     Log mode - 'file|syslog|all' (default: 'file')
  -p PORT, --port PORT  Port (default 80|443)
  -k KEYFILE, --keyfile KEYFILE
                        Path to key file (only for use with 'https', default: key.pem
  -c CERTFILE, --certfile CERTFILE
                        Path to cert file (only for use with 'https', default: cert.pem
