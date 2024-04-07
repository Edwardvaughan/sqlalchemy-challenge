#Import the dependencies
import datetime as dt
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, MetaData, Table

#Database Setup

#create an engine to connect to the database
engine = create_engine ("sqlite:///C://Users/hawaii.sqlite")

#Reflect an existing database into a new model
metadata = MetaData ()

station = Table ("station", metadata, autoload_with = engine)
[c.name for c in station.columns]
["id", "station", "name", "latitude", "longitude", "elevation"]

measurement = Table ("measurement", metadata, autoload_with = engine)
[c.name for c in measurement.columns]
["id", "station", "date", "prcp", "tobs"]

#Reflect the tables
Base = automap_base ()
Base.prepare (autoload_with = engine)

#Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

#Flask Setup
app = Flask (__name__)

#Flask Routes

#Define the homepage route
@app.route ("/")

def home ():

    return (f"Climate App<br/>"
            f"Routes:<br/>"
            f"/api/v1.0/station<br/>"
            f"/api/v.1.0/preciptitation<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/&lt;start&gt;<br/>"
            f"/api/v1.0/&lt;start&gt;/&lt;end&gt;")

#Define the /api/v1.0/station route
@app.route ("/api/v1.0/station")

def station ():

    session = Session (engine)

    #Stations:
    Stations = session.query (Station.station).all ()

    #Convert Stations to a list
    station_list = [station for station in Stations]

    session.close ()

    return jsonify (station_list)

#Define the /api/v1.0/precipitation route
@app.route ("/api/v1.0/precipitation")
   
def precipitation ():

    session = Session (engine)

    #Calculate the date one year from the last date in the dataset
    most_recent_date = session.query (func.max (Measurement.date)).scalar ()
    one_year_previous = dt.datetime.strptime (most_recent_date, "%Y-%m-%d") - dt.timedelta (days = 365)

    #Perform a query to retrieve the date and precitation scores
    precipitation_data = session.query (Measurement.date, Measurement.prcp).filter (Measurement.date >= one_year_previous).all ()
    
    #Convert precipition_data to a dictionary
    precipitation_data = {date.prcp for date, prcp in precipitation_data}

    session.close ()

    return jsonify (precipitation_data)

#Define the /api/v1.0/tobs route
@app.route ("/api/v1.0/tobs")

def tobs ():

    session = Session (engine)

    #Most active station
    active_stations = session.query (Measurement.station,
    func.count (Measurement.station)).group_by (Measurement.station).order_by (func.count (Measurement.station)).desc ()
    most_active_station = active_stations [0][0]

    #Calculate the date one year from the last date in the dataset
    most_recent_date = session.query (func.max (Measurement.date)).scalar ()
    one_year_previous = dt.datetime.strptime (most_recent_date, "%Y-%m-%d") - dt.timedelta (days = 365)

    #Query the last 12 months of temperature observation data for this station
    temperature_data = session.query (Measurement.date, Measurement.tobs).filter (Measurement.station 
    == most_active_station, Measurement.date >= one_year_previous).all ()

    #Convert temperature_data to a list of dictionaries
    tobs_data = [{"Date": date, "Temperature": tobs} for date, tobs in temperature_data]

    session.close ()

    return jsonify (tobs_data)

#Define the /api/v1.0/<start> route
@app.route ("/api/v1.0/<string:start>")

def calc_temps_start (start):

    session = Session (engine)

    start_date = dt.datetime.strptime (start, "%Y-%m-%d")

    #Calculate highest, lowest and average temperature for dates greater than or equal to the start date
    temperature_statistics = session.query (func.min (Measurement.tobs),
                                            func.max (Measurement.tobs),
                                            func.avg (Measurement.tobs)).filter (Measurement.date >= start_date).all ()
    
    temp_data = {"TMIN": temperature_statistics [0][0],
                 "TMAX": temperature_statistics [0][1],
                 "TAVG": temperature_statistics [0][2]}
    
    session.close ()
    
    return jsonify (temp_data)

#Define the /api/v1.0/<start>/<end> route
@app.route ("/api/v1.0/<string:start>/<string:end>")

def calc_temps_start_end (start, end):

    session = Session (engine)

    start_date = dt.datetime.strptime (start, "%Y-%m-%d")
    end_date = dt.datetime.strptime (end, "%Y-%m-%d")

    #Calculate highest, lowest and average temperature for date between start and end dates inclusive
    temperature_statistics = session.query (func.min (Measurement.tobs),
                                            func.max (Measurement.tobs),
                                            func.avg (Measurement.tobs)).filter (Measurement.date >= start_date,
                                                                                 Measurement.date <= end_date).all ()
    
    temp_data = {"TMIN": temperature_statistics [0][0],
                 "TMAX": temperature_statistics [0][1],
                 "TAVG": temperature_statistics [0][2]}
    
    session.close ()

    return jsonify (temp_data)

#Run the app
if __name__ == "__main__":
    app.run (debug = True)