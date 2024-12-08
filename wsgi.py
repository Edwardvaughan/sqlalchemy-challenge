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
Station = Base.classes.station.name
Measurement = Base.classes.measurement

#Flask Setup
wsgi = Flask (__name__)

#Flask Routes
        
#Define the homepage route

@wsgi.route ('/')

def hello ():
    return 'Hello'

hello ()

if __name__ == 'main':
    from waitress import serve
    serve (app, host = '0.0.0.0', port = 8080)

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
    Stations = session.query (Station)

    session.close ()

#Convert names to a list
    names_list = [name for name in Stations]

    print (names_list)

    return

station ()

#Define the /api/v1.0/precipitation route
@wsgi.route ('/api/v1.0/precipitation')
   
def precipitation ():

    session = Session (engine)

#Calculate the date one year from the last date in the dataset
    most_recent_date = session.query (func.max (Measurement.date)).scalar ()
    one_year_previous = dt.datetime.strptime (most_recent_date, "%Y-%m-%d") - dt.timedelta (days = 365)

#Perform a query to retrieve the date and precitation scores
    precipitation_data = session.query (Measurement.date, Measurement.prcp).filter (Measurement.date >= one_year_previous)

    session.close ()

#Convert precipition_data to a dictionary
    prcp_data = {(date, prcp) for (date, prcp) in precipitation_data}

    print (prcp_data)

    return

precipitation ()

#Define the /api/v1.0/tobs route
@wsgi.route ('/api/v1.0/tobs')

def tobs ():

    session = Session (engine)

#Most active station
    active_stations = session.query (Measurement.station, func.count (Measurement.station)).group_by (Measurement.station).order_by (func.count (Measurement.station))
    most_active_station = active_stations [0][0]

#Calculate the date one year from the last date in the dataset
    most_recent_date = session.query (func.max (Measurement.date)).scalar ()
    one_year_previous = dt.datetime.strptime (most_recent_date, "%Y-%m-%d") - dt.timedelta (days = 365)

#Query the last 12 months of temperature observation data for this station
#temperature_data = session.query (Measurement.station == most_active_station, Measurement.date >= one_year_previous, Measurement.tobs)

#tobs_data = session.query ([{'Station': Measurement.most_active_station, 'Date': Measurement.date, 'Temperature': Measurement.tobs} for (Measurement.most_active_station, Measurement.date, Measurement.tobs) in temperature_data])

    session.close ()
    
#print (tobs_data)

    return

tobs ()

#Define the /api/v1.0/<start> route
@wsgi.route ('/api/v1.0/calc_temps_start')

def calc_temps_start (start):

    input (start)

    session = Session (engine)

    start_date = dt.datetime.strptime (start, "%Y-%m-%d")

#Calculate highest, lowest and average temperature for dates greater than or equal to the start date
    temperature_statistics = session.query (func.min (Measurement.tobs), func.max (Measurement.tobs), func.avg (Measurement.tobs)).filter (Measurement.date >= start_date)

    session.close ()

    temp_data = {"TMIN": temperature_statistics [0][0], "TMAX": temperature_statistics [0][1], "TAVG": temperature_statistics [0][2]}
    
    print (temp_data)

    return

calc_temps_start ('2017-04-25')

#Define the /api/v1.0/<start>/<end> route
@wsgi.route ('/api/v1.0/cal_temps_start_end')

def calc_temps_start_end (start, end):

    input (start)
    input (end)

    session = Session (engine)

    start_date = dt.datetime.strptime (start, "%Y-%m-%d")
    end_date = dt.datetime.strptime (end, "%Y-%m-%d")

#Calculate highest, lowest and average temperature for date between start and end dates inclusive
    temperature_statistics = session.query (func.min (Measurement.tobs), func.max (Measurement.tobs), func.avg (Measurement.tobs)).filter (Measurement.date >= start_date, Measurement.date <= end_date).all ()

    session.close ()

    temp_data = {"TMIN": temperature_statistics [0][0], "TMAX": temperature_statistics [0][1], "TAVG": temperature_statistics [0][2]}

    print (temp_data)

    return

calc_temps_start_end ('2017-04-25', '2017-04-26')

#Run the app
if __name__ == "__main__":
   print ('This program is running as the main module')
   wsgi.run (debug = True)