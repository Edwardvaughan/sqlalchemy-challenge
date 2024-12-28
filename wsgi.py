#Import the dependencies
import datetime as dt

from flask import Flask

import sqlalchemy

from sqlalchemy.ext.automap import automap_base

from sqlalchemy.orm import Session

from sqlalchemy import create_engine, func, MetaData, Table, text, URL

#Database Setup

#create an engine to connect to the  database
URL = 'sqlite:///C://Users/edwar/Downloads/hawaii.sqlite'

engine = create_engine (URL)

#Reflect an existing database into a new model
metadata = MetaData ()

station = Table ('station', metadata, autoload_with = engine)

measurement = Table ('measurement', metadata, autoload_with = engine)

#Reflect the tables
Base = automap_base ()

Base.prepare (autoload_with = engine)

#Save references to each table
Station = Base.classes.station

Measurement = Base.classes.measurement

#Flask Setup
wsgi = Flask (__name__)

#Flask routes
        
#Define the homepage route
@wsgi.route ('/')

#Hello
def hello ():

    print ('Hello')

def home ():
    
    print ('Climate App')
    
    print ('Routes:')
    
    print ('/api/v1.0/station')
    
    print ('/api/v.1.0/precipitation')
    
    print ('/api/v1.0/tobs')
    
    print ('/api/v1.0/start')
    
    print ('/api/v1.0/start/end')
    
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

#Header

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

        result = Connection.execute (text ("SELECT station, date, prcp FROM Measurement WHERE date >= '2016-04-23';")).fetchall ()

        for row in result:
        
            print (row)

    return

precipitation ()

header ('TEMPERATURE DATA')

#Define the /api/v1.0/tobs route
@wsgi.route ('/api/v1.0/tobs')

def temperature ():

    with engine.connect () as Connection:

        result = Connection.execute (text ("SELECT station, date, tobs FROM Measurement WHERE date >= '2016-04-23';")).fetchall ()

        for row in result:
        
            print (row)

    return

temperature ()

#Define the /api/v1.0/<start> route
@wsgi.route ('/api/v1.0/string:start>')

def calc_temps_start (start):

    start = input ('Input start date ')

    start_date = dt.datetime.strptime (start, '%Y-%m-%d')

    session = Session (engine)

#Calculate lowest. highest and average temperature for dates greater then or equal to the stafrt date
    temperature_statistics = session.query (func.min (Measurement.tobs),

                                            func.max (Measurement.tobs),

                                            func.avg (Measurement.tobs)).filter (Measurement.date >= start_date)

    session.close ()

    temp_data = {'TMIN': temperature_statistics [0][0],

                 'TMAX': temperature_statistics [0][1],

                 'TAVG': temperature_statistics [0][2]} 
    
    print (temp_data)

    return

calc_temps_start ('2017-04-22')

#Define the /api/v1.0/<start>/<end> route
@wsgi.route ('/api/v1.0/<string:start>/<string:end>')

def calc_temps_start_end (start, end):

    start = input ('Input start date ')

    end = input ('Input end date ')

    start_date = dt.datetime.strptime (start, '%Y-%m-%d')

    end_date = dt.datetime.strptime (end, '%Y-%m-%d')

    session = Session (engine) 

#Calculate lowest, highest and average temperature for dates between start and end dates inclusive
    temperature_statistics = session.query (func.min (Measurement.tobs),

                                            func.max (Measurement.tobs),
                                             
                                            func.avg (Measurement.tobs)).filter (Measurement.date >= start_date, 
                                                                                 Measurement.date <= end_date)

    session.close ()

    temp_data = {'TMIN': temperature_statistics [0][0],
    
                 'TMAX': temperature_statistics [0][1],
         
                 'TAVG': temperature_statistics [0][2]}

    print (temp_data)

    return

calc_temps_start_end ('2017-04-22', '2017-04-23')

#If app is running as the main module. say so
if __name__ == '__main__':

    print ('This program is running as the main module.')