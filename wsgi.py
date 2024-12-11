#Import the dependencies

import datetime as dt

from flask import Flask

import sqlalchemy

from sqlalchemy.ext.automap import automap_base

from sqlalchemy.orm import Session

from sqlalchemy import create_engine, func, MetaData, Table

#Database Setup

#create an engine to connect to the database
engine = create_engine ("sqlite:///C://Users/edwar/Downloads/hawaii.sqlite")

#Reflect an existing database into a new model
metadata = MetaData ()

station = Table ("station", metadata, autoload_with = engine)

measurement = Table ("measurement", metadata, autoload_with = engine)

#Reflect the tables
Base = automap_base ()

Base.prepare (autoload_with = engine)

#Save references to each table#
Station = Base.classes.station

Measurement = Base.classes.measurement

session = Session (engine)

#Flask Setup
wsgi = Flask (__name__)

#Flask Routes
        
#Define the homepage route

@wsgi.route ('/')

def hello ():

    print ('Hello')

hello ()

if __name__ == 'main':
    
    from waitress import serve
    
    serve (wsgi, host = '0.0.0.0', port = 8080)

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

    session = Session (engine)

#Stations:
    Names = session.query (Station.name)

    session.close ()

#Convert names to a list
    names_list = [name for name in Names]

    print (names_list)

    return

station ()

#Define the /api/v1.0/precipitation route
@wsgi.route ('/api/v1.0/precipitation')

def precipitation_header ():

    print ()

    print ()

    print ('PRECIPITATION DATA')

    print ()

    print ()

    return

precipitation_header ()
   
def precipitation ():

    session = Session (engine)

    precipitation_data = session.query (Measurement.station, Measurement.date, Measurement.prcp).filter (Measurement.date > '2016-04-23').all ()

    session.close ()

#Convert precipitation_data to a list of dictionaries
    prcp_data = [{station: {date: prcp}} for (station, date, prcp) in precipitation_data]

    print (prcp_data)

    return

precipitation ()

#Define the /api/v1.0/tobs route
@wsgi.route ('/api/v1.0/tobs')

def temperature_header ():

    print ()

    print ()

    print ('TEMPERATURE DATA')

    print ()

    print ()

    return

temperature_header ()

def tobs ():

    session = Session (engine)

    temperature_data = session.query (Measurement.station, Measurement.date, Measurement.tobs).filter (Measurement.date > '2016-04-23').all ()

    session.close ()

#Convert temperature_data to a list of dictionaries
    tobs_data = [{station: {date: tobs}} for (station, date, tobs) in temperature_data]

    print (tobs_data)

    return

tobs ()

#Define the /api/v1.0/<start> route
@wsgi.route ('/api/v1.0/calc_temps_start')

def calc_temps_start (start):

    start = input ('Input start date ')

    start_date = dt.datetime.strptime (start, "%Y-%m-%d")

#Calculate highest, lowest and average temperature for dates greater than or equal to the start date

    session = Session (engine)

    temperature_statistics = session.query (func.min (Measurement.tobs), func.max (Measurement.tobs), func.avg (Measurement.tobs)).filter (Measurement.date >= start_date)

    session.close ()

    temp_data = {"TMIN": temperature_statistics [0][0], "TMAX": temperature_statistics [0][1], "TAVG": temperature_statistics [0][2]}
    
    print (temp_data)

    return

calc_temps_start ('2016-08-24')

#Define the /api/v1.0/<start>/<end> route
@wsgi.route ('/api/v1.0/cal_temps_start_end')

def calc_temps_start_end (start, end):

    start = input ('Input start date ')

    end = input ('Input end date ')

    start_date = dt.datetime.strptime (start, "%Y-%m-%d")

    end_date = dt.datetime.strptime (end, "%Y-%m-%d")

#Calculate highest, lowest and average temperature for date between start and end dates inclusive

    session = Session (engine)

    temperature_statistics = session.query (func.min (Measurement.tobs), func.max (Measurement.tobs), func.avg (Measurement.tobs)).filter (Measurement.date >= start_date, Measurement.date <= end_date).all ()

    session.close ()

    temp_data = {"TMIN": temperature_statistics [0][0], "TMAX": temperature_statistics [0][1], "TAVG": temperature_statistics [0][2]}

    print (temp_data)

    return

calc_temps_start_end ('2016-08-24', '2017-08-23')

#Run the app
if __name__ == "__main__":

   print ('This program is running as the main module')
   
   wsgi.run (debug = True)