from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import cgi

form = '''
  <form method="POST" enctype ="multipart/form-data" action="/hello">
    <input name="message" type ="text">
    <br>
    <input type="submit" value="Submit">
  </form>

'''


class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print('get called')
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = "<html><body><h1>Hello!!!<h1>"
                message += "<h2> What would you like me to say?</h2> "
                message += form
                message += "</body></html>"
                print(message)
                self.wfile.write(message.encode())
                print(message)
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = "<html><body><h1>&#161Hola!!!<h1> <a href ='/hello'> Back to Hello page </a>"

                message += "</body></html>"
                print(message)
                self.wfile.write(message.encode())

                return

        except IOError:
            self.send_error(404, 'File not found: %s' % self.path)

    def do_POST(self):
        try:
            print('post called')
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            print('after send headers')
            len1 = int(self.headers.get('Content-length', 0))
            print('cont len-->', len1)
            data = self.rfile.read(len1).decode()
            print('data-->', data)
            msgcont = parse_qs(data)['message'][0]

            print('msg-->', msgcont)
            op = ""
            op += "<html><body>"
            op += "<h2> How abt this: </h2>"
            op += "<h1>%s </h1>" % msgcont[0].decode()
            op += form
            op += "</body></html>"
            self.wfile.write(op.encode())
            print(op)
        except:
            print('IN exception ')
            raise


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print("server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping webserver")
        server.socket.close()


if __name__ == '__main__':
    main()
