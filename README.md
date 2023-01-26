# Yahpot
### Yet Another HTTP(S) HoneyPot

Simple (under 90 loc), yet functional honeypot with syslog and file-based logging. 

### Usage
`yahpot.py [-h] [-t {http,https}] [-d DECOY] [-f FILE] [-l LOG] [-p PORT] [-k KEYFILE] [-c CERTFILE]`

### Examples
Http server on port 8080 with apache2 welcome page, logging to `yahpotlog`:

`yahpot.py -t http -d apache2/localhost/index.html -l yahpot.log -p 8080`

Https server on port 443 with apache2 welcome page, logging to `/var/log/syslog`:

`yahpot.py -t https -d apache2/localhost/index.html -l syslog -k key.pem -c cert.pem`

### Queries
In `queries` directory there are few KQL (Kusto Query Language) queries I'm using for analyzing Yahpot logs in Microsoft Sentinel.

### Tools
Directory `tools` contains useful scripts for parsing Yahpot log files and more.
#### yah2otx
Parsing Yahpot logs and sending malicious IP IOC to OTX. Local `sqlite3` database is created to keep track of parsed ip addresses. 
If `pulse` doesn't exist, it will be created.
**Be aware** that in order to use `yah2otx` you need to set environment variable `OTX_API_KEY` for Open Threat eXchange access.

##### Usage
`yah2otx.py [-h] -l {syslog,ylog} logfile pulse`

##### Examples
Parse `syslog` file and upload IOCs to pulse named `Web hits`:

`yah2otx.py -l syslog /var/log/syslog "Web hits"`

Parse `yahpotlog` file and upload IOCs to pulse named `New web hits`:

`yah2otx.py -l ylog yahpot.log "New web hits"`




