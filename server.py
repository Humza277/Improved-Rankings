# Created by Humza Malak & Alon Solomon
from http.server import SimpleHTTPRequestHandler,HTTPServer
import datetime
import re
from urllib.parse import urlparse, parse_qs, unquote
import gbs
import json

port = 8000

#Define regular expression for the xhr request
BEST_RE = re.compile("/best(.*)")

class Handler(SimpleHTTPRequestHandler):
    # Overriding the get method handler
    def do_GET(self):
        print(self.path)

        # If this is the xhr request for top fields
        if BEST_RE.match(self.path):
            # Decode the url
            url = unquote(self.path)
            # Get the query part of the url
            query  = urlparse(url).query
            # Get the parameters
            params = parse_qs(query)
            # Use gbs module to get the scores
            # for the requested parameters.
            result = gbs.g_best_score(
                int(params['n'][0]) ,
                params['u'][0]      ,
                int(params['s'][0]) ,
                int(params['e'][0]) ,
                params['r'][0]      ,
                params['a'][0].split(','))
            print(result)
            # Send response code
            self.send_response(200)
            # Send header
            self.send_header('Content-type','text/html')
            # End headers section
            self.end_headers()
            # Sends the result of the gbs script
            self.wfile.write(bytes(json.dumps(result), encoding="utf-8"))

        # If this is the xhr request for univ fields
        elif "/uvs" in self.path :
            # Decode the url
            url = unquote(self.path)
            # Get region argument
            reg = url.split('=')[-1]
            # Send response code
            self.send_response(200)
            # Send header
            self.send_header('Content-type','text/html')
            # End headers section
            self.end_headers()
            # Get then send the universities
            result = gbs.g_uvs(reg)
            self.wfile.write(bytes(json.dumps(result), encoding="utf-8"))
        # if this is not an xhr request, use the default handler
        else :
            super().do_GET()

server = HTTPServer(('', port), Handler)
print ('Started httpserver on port ', port)

# Wait forever for incoming http requests
server.serve_forever()