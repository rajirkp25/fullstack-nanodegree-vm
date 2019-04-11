# Udactiy Catalog App

## Section 0: Intro
This is a catalog app built with python and flask. It supports oauth login with google and facebook.

## Section 1: Set Up Environment
To run this application, install Vagrant. Follow the Getting Started guide by Vagrant (https://www.vagrantup.com/docs/getting-started/). After successfully installing Vagrant, start the virtual machine by ```vagrant up``` To access the VM run ``vagrant ssh```.

## Section 2: Requirements
- Flask == 0.10.1
- SQLAlchemy == 0.8.4 
- httplib2 == 0.9.2
- urllib3 == 0.9.2
- google_api_python_client == 1.4.1
- Requests == 2.7.0

## Section 3: Installation
Clone the repo or download the package and place the repo in the Vagrant machine environment.
Then run
```
python database_setup.py
python lotsofcategories.py
python server.py
```

## Section 4: Set Up
To setup the database and to create some content to interact with, run
```
python database_setup.py
python lotsofcategories.py
```

## Section 5: How to run
To run the application execute ```python server.py```. The application will be available in the browser at localhost with port 5000 by default.

## Section 6: Usage
With this application you can create, edit and delete items of various categories. To do this, you have to login first with your Google or facebook account via oauth. 