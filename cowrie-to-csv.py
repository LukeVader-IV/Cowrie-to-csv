import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os

class bad_actor:
    def __init__(self, ip):
        self.ip = ip
        self.attempts = 0
        self.success=False
        self.total_connect=0.0

    def __str__(self):
        return f"{self.ip} - attempts: {self.attempts}, connect success: {self.success}, total connection time: {self.total_connect}\n"
    
    def __hash__(self):
        return hash(self['src_ip'])

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/csv')
        self.end_headers()

        content = to_csv(parse_data()).encode("utf-8")
        self.wfile.write(content)

def parse_data():
    actors : list[bad_actor] = []
    act : bad_actor
    new=False

    # The whole file is not valid json, each line must be treated as a separate json object
    for index, line in enumerate(open("/app/cowrie.json", 'r')):
        try:
            line_data=json.loads(line)
        
            if line_data['eventid'] == "cowrie.session.connect":
                found=False
                for x in actors:
                    if line_data['src_ip'] == x.ip:
                        act=x
                        found=True
                        new=False
                        break
                if not found:
                    new=True
                    act = bad_actor(line_data['src_ip'])

            elif line_data['eventid'] == "cowrie.login.failed":
                act.attempts+=1
            elif line_data['eventid'] == "cowrie.login.success":
                act.attempts+=1
                print("A user at address " + line_data['src_ip'] + " successfully logged in with username \"" + line_data['username'] + "\" and password \"" + line_data['password'] + "\"")
            elif line_data['eventid'] == "cowrie.command.input":
                print("\t" + line_data['input'])
                executions = True
            elif line_data['eventid'] == "cowrie.session.closed":
                act.total_connect +=line_data['duration']
                if new:
                    actors.append(act)
        except:
            print(f"Error parsing json content in line {index}:\n{line}")
            pass
    return actors

def to_csv(actors_list:list[bad_actor]):
    csv = "ip,attempted_connections,IDS,system_time\n"
    for actor in actors_list:
        csv+= actor.ip + "," + str(actor.attempts) + "," + str(actor.attempts > 0) + "," + str(actor.total_connect) +"\n"
    return csv

def main():
    ip = os.environ.get('IP', "0.0.0.0")
    serverPort = int(os.environ.get('PORT', 8000))

    httpd = HTTPServer((ip, serverPort), RequestHandler)

    print('Starting server...')
    httpd.serve_forever()

if __name__ == '__main__':
    main()