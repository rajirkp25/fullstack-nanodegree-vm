#!/usr/bin/env python3
#
# An HTTP server that's a message board.

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

memory = []


class MessageHandler(BaseHTTPRequestHandler):

    def my_test(self):
        print("in self")

    def do_POST(self):
        # How long was the message?
        length = int(self.headers.get('Content-length', 0))
        if self.path.endswith("/restaurants/new"):
            # Read and parse the message
            data = self.rfile.read(length).decode()
            newrest = parse_qs(data)["newRestName"][0]
            print("newRestName-->", newrest)
            self.create_new_restaurant(newrest)

            # Send a 303 back to the root page
            self.send_response(301)  # redirect via GET
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', '/restaurants')
            self.end_headers()
            return

        if self.path.endswith("/edit"):
            # Read and parse the message
            data = self.rfile.read(length).decode()
            renameRest = parse_qs(data)["updateRestName"][0]
            restId = self.path.split("/")[2]
            print("updateRestName-->", renameRest, ' ', restId)
            self.rename_restaurant(restId, renameRest)

            # Send a 303 back to the root page
            self.send_response(301)  # redirect via GET
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', '/restaurants')
            self.end_headers()

            return

        if self.path.endswith("/delete"):
            restId = self.path.split("/")[2]
            print("DelRestID-->", restId)
            self.delete_restaurant(restId)
            # Send a 303 back to the root page
            self.send_response(301)  # redirect via GET
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', '/restaurants')
            self.end_headers()

    def do_GET(self):

        mesg = '''<!DOCTYPE html>
                    <title>My Restaurants Page</title>
                    <h1>Welcome to my Restaurants page</h1>
                    '''
        form = '''<form method="POST" action="/restaurants/new">
        <input name="newRestName" type ="text">
        <input type="submit" value="Create">
    </form>
    '''

        # First, send a 200 OK response.
        print("Get called")
        self.send_response(200)

        # Then send headers.
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        if self.path.endswith("/restaurants"):
            # self.send_response(200)
            # self.send_header('Content-type', 'text/html')
            self.end_headers()
            mesg += "<a href ='/restaurants/new'> Create New Restaurants </a>"
            self.get_restaurants(mesg)

            # print('after get_rest-->', mesg)

        if self.path.endswith("/restaurants/new"):
            print("new resturants link")
            self.end_headers()
            mesg += "<a href ='/restaurants'> View Restaurants </a> </br></br>"

            # Send the form with the messages in it.
            mesg += form
            # print(mesg)
            self.wfile.write(mesg.encode())
            return

        if self.path.endswith("/edit"):
            print("rest edit link")
            restID = self.path.split("/")[2]
            updRest = session.query(Restaurant).filter_by(id=restID).one()

            if updRest:
                mesg += "<a href ='/restaurants'> View Restaurants </a> </br></br>"
                form_edit = "<h2>Rename Restaurant %s</h2>" % updRest.name
                form_edit += "<form method='POST' action='/restaurants/%s/edit'>" % restID
                form_edit += "<input name='updateRestName' type ='text' placeholder='%s'>" % updRest.name
                form_edit += "<input type = 'submit' value = 'Rename' ></form>"
                mesg += form_edit
                self.end_headers()
                self.wfile.write(mesg.encode())
            return

        if self.path.endswith("/delete"):
            print("rest delete link")
            restID = self.path.split("/")[2]
            delRest = session.query(Restaurant).filter_by(id=restID).one()
            if delRest:
                mesg += "<a href ='/restaurants'> View Restaurants </a> </br></br>"
                form_del = "<h2>Are you sure you want to delete Restaurant %s</h2>" % delRest.name
                form_del += "<form method='POST' action='/restaurants/%s/delete'>" % restID
                # form_del += "<input name='updateRestName' type ='text' placeholder='%s'>" % delRest.name
                form_del += "<input type = 'submit' value = 'Delete' ></form>"
                mesg += form_del
                self.end_headers()
                self.wfile.write(mesg.encode())

                return

    def get_restaurants(self, mesg):
        print("in get_restaurants")
        restaurants = session.query(Restaurant).all()

        # rest_names = list()
        mesg += "<dl>"
        for restaurant in restaurants:
            # rest_names.append(row[0])
            mesg += "<dt>"
            print('rest name -->', restaurant.name, ' ', restaurant.id)
            mesg += restaurant.name
            mesg += "</br>"
            mesg += "<a href ='/restaurants/%s/edit' >Edit </a> " % restaurant.id
            mesg += "</br>"
            mesg += "<a href ='/restaurants/%s/delete' >Delete </a> " % restaurant.id
            mesg += "</dt>"
            mesg += "</br></br>"
        mesg += "</dl>"
        # print(mesg)

        self.wfile.write(mesg.encode())

    def create_new_restaurant(self, newRest):
        print("In create_new_restaurant-->", newRest)
        myNewResturant = Restaurant(name=newRest)
        session.add(myNewResturant)
        session.commit()

    def rename_restaurant(self, restId, renameRest):
        print("In rename_restaurant-->", renameRest)
        myUpdRest = session.query(Restaurant).filter_by(id=restId).one()
        myUpdRest.name = renameRest
        session.add(myUpdRest)
        session.commit()

    def delete_restaurant(self, restId):
        print("In delete_restaurant-->", restId)
        delRest = session.query(Restaurant).filter_by(id=restId).one()
        session.delete(delRest)
        session.commit()


def main():
    try:
        server_address = 8080
        httpd = HTTPServer(('', server_address), MessageHandler)
        print("Server running in port %s" % server_address)
        print("open link - localhost:8080/restaurants")
        print("to add a new restaurant - localhost:8080/restaurants/new")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("^C user interrupted, stopping server")
        httpd.socket.close()


if __name__ == '__main__':
    main()
