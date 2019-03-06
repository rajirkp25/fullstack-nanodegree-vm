#!/usr/bin/env python3
#
# An HTTP server that's a message board.

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

memory = []

form = '''<!DOCTYPE html>
  <title>Message Board</title>
  <form method="POST">
    <textarea name="message"></textarea>
    <br>
    <button type="submit">Post it!</button>
  </form>
  <pre>
{}
  </pre>
'''


class MessageHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        # How long was the message?
        length = int(self.headers.get('Content-length', 0))

        # Read and parse the message
        data = self.rfile.read(length).decode()
        message = parse_qs(data)["message"][0]
        print("data-->", data)
        # Escape HTML tags in the message so users can't break world+dog.
        message = message.replace("<", "&lt;")

        # Store it in memory.
        memory.append(message)

        # Send a 303 back to the root page
        self.send_response(303)  # redirect via GET
        self.send_header('Location', '/hello')
        self.end_headers()

    def do_GET(self):
        # First, send a 200 OK response.
        print("Get called")
        self.send_response(200)

        # Then send headers.
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        mesg = "<h1> hi <h1>"
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            mesg = "<h1>Hello!!!<h1>"

        if self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            mesg = "<h1>&#161Hola!!!<h1>"

        # Send the form with the messages in it.
        mesg += form.format("\n".join(memory))
        self.wfile.write(mesg.encode())


def main():
    try:
        server_address = 8080
        httpd = HTTPServer(('', server_address), MessageHandler)
        print("Server running in port %s" % server_address)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("^C user interrupted, stopping server")
        httpd.socket.close()


if __name__ == '__main__':
    main()
