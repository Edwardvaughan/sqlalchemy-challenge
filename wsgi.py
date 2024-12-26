#Import the dependencies

import datetime as dt

from flask import Flask

import sqlalchemy

from sqlalchemy.ext.automap import automap_base

from sqlalchemy.orm import Session

from sqlalchemy import create_engine, MetaData, Table, text, URL

#Database Setup

#create an engine to connect to the  database

URL = "sqlite:///C://Users/edwar/Downloads/hawaii.sqlite"

engine = create_engine (URL)

#Reflect an existing database into a new model
metadata = MetaData ()

station = Table ("station", metadata, autoload_with = engine)

measurement = Table ("measurement", metadata, autoload_with = engine)

#Reflect the tables
Base = automap_base ()

Base.prepare (autoload_with = engine)

#Save references to each table
Station = Base.classes.station

Measurement = Base.classes.measurement

session = Session (engine)

#Flask Routes

wsgi = Flask (__name__)
        
#Define the homepage route

@wsgi.route ('/')

def hello ():

    print ('Hello')

hello ()

def home ():
    
    print ("Climate App")
    
    print ("Routes:")
    
    print ("/api/v1.0/station")
    
    print ("/api/v.1.0/precipitation")
    
    print ("/api/v1.0/tobs")
    
    print ("/api/v1.0/start")
    
    print ("/api/v1.0/start/end")
    
    return

home ()   

#Define the /api/v1.0/station route
@wsgi.route ('/api/v1.0/station')

def station ():

    with engine.connect () as Connection:

        result = Connection.execute (text ('SELECT station, name FROM Station')).fetchall ()

        for row in result:

            print (row)

    return

station ()

#Define the /api/v1.0/precipitation route
@wsgi.route ('/api/v1.0/precipitation')

def header (heading):

    print ()

    print ()

    print (heading)

    print ()

    print ()

    return

header ('PRECIPITATION DATA')
   
def precipitation ():

    with engine.connect () as Connection:

        result = Connection.execute (text ("SELECT station, date, prcp FROM Measurement WHERE date >= '2016-4-23';")).fetchall ()

        for row in result:
        
            print (row)

    return

precipitation ()

header ('TEMPERATURE DATA')

#Define the /api/v1.0/tobs route
@wsgi.route ('/api/v1.0/tobs')

def temperature ():

    with engine.connect () as Connection:

        result = Connection.execute (text ("SELECT station, date, tobs FROM Measurement WHERE date >= '2016-4-23';")).fetchall ()

        for row in result:
        
            print (row)

    return

temperature ()

#Run the app
if __name__ == "__main__":

   print ('This program is running as the main module')