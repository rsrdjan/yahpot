#!/usr/bin/env python3

import argparse, syslog, sys, ssl
from http.server import HTTPServer, BaseHTTPRequestHandler

loggingfilepath = "yahpot.log"

class YahpotServer(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = "/templates/" + args.decoy
            self.send_response(200)
        try:
            fileToServe = open(self.path[1:]).read()
        except:
            fileToServe = "File not found"
            self.send_response(404)
        
        self.send_header("Content-type","text/html")
        self.end_headers()
        self.wfile.write(bytes(fileToServe,"utf-8"))
    
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)
        self.wfile.write(bytes(self.path,"utf-8"))

class YahpotServerFileLog(YahpotServer):
    def log_message(self, format: str, *args):
        open(loggingfilepath,'a').write("%s -- [%s] %s\n" % (self.address_string(),self.log_date_time_string(), format%args))
        
class YahpotServerSysLog(YahpotServer):
    def log_message(self, format: str, *args):
        syslog.syslog("yahpot %s -- [%s] %s\n" % (self.address_string(),self.log_date_time_string(), format%args))

class YahpotServerAllLog(YahpotServer):
    def log_message(self, format: str, *args):
        open(loggingfilepath,'a').write("%s -- [%s] %s\n" % (self.address_string(),self.log_date_time_string(), format%args))
        syslog.syslog("yahpot %s -- [%s] %s\n" % (self.address_string(),self.log_date_time_string(), format%args))


if __name__ == "__main__":

    # Parser options
    parser = argparse.ArgumentParser(description="Yet Another HTTP(S) HoneyPot")
    parser.add_argument("-t", "--type", help="Type of server - 'http|https'", choices=['http','https'], default="http", required=False)
    parser.add_argument("-d", "--decoy", help="Decoy to use - (see /templates/ directory)", type=str, default="apache2/localhost/index.html", required=False)
    parser.add_argument("-f", "--file", help="File to write log to (default 'yahpot.log')", type=str, default="yahpot.log", required=False)
    parser.add_argument("-l", "--log", help="Log mode - 'file|syslog|all' (default: 'file')", type=str, default="file", required=False)
    parser.add_argument("-p", "--port", help="Port (default 80|443) ", type=int, required=False)
    parser.add_argument("-k", "--keyfile", help="Path to key file (only for use with 'https', default: key.pem", type=str, default="key.pem", required=False )
    parser.add_argument("-c", "--certfile", help="Path to cert file (only for use with 'https', default: cert.pem", type=str, default="cert.pem", required=False)
    args = parser.parse_args()

    # Defaults
    hostName = "localhost"
    if not args.port:
        if args.type == "http":
            args.port = 80
        if args.type == "https":
            args.port = 443
    loggingfilepath = args.file
    if args.log == "file":
        webServer = HTTPServer((hostName,args.port),YahpotServerFileLog)
    if args.log == "syslog":
        webServer = HTTPServer((hostName, args.port), YahpotServerSysLog)
    if args.log == "all":
        webServer = HTTPServer((hostName,args.port), YahpotServerAllLog)
    if args.type == "https":
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(args.certfile, args.keyfile)
            webServer.socket = context.wrap_socket(webServer.socket, args.keyfile, args.certfile)
        except FileNotFoundError:
            print("[!] Key or cert file doesn't exist. Use -h or --help for options.")
            sys.exit()

    print("[+] Server started: http://%s:%s" % (webServer.server_name,webServer.server_port))
    print("[+] Serving decoy %s" % args.decoy)
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()

    print("[!] Server stopped. Exiting.")
