# sqlalchemy-challenge
Module 10 homework

%matplotlib inline
import matplotlib.pyplot as plt

import pandas as pd
import datetime as dt

#Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, MetaData, Table, text

#create engine to hawaii.sqlite
engine = create_engine ("sqlite:///C://Users/hawaii.sqlite")

#reflect an existing database into a new model
metadata = MetaData ()

station = Table ("station", metadata, autoload_with = engine)
[c.name for c in station.columns]
['id', 'station', 'name', 'latitude', 'longitude', 'elevation']

measurement = Table ("measurement", metadata, autoload_with = engine)
[c.name for c in measurement.columns]
['id', 'station, 'date, 'prcp', 'tobs']

#reflect the tables
Base = automap.base ()
Base.prepare (autoload-with = engine)

#View all of the classes that automap found
for mapped_class in Base.classes:
  print (mapped_class)

#Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

#Create our session (link) from Python to the DB
session = Session (engine)

#Find the most recent date in the data set.
most_recent_date = session.query (func.max (Measurement.date)).scalar ()

#Design a query to retrieve the last 12 months of precipitation data.
#And plot the results.  Starting from the most recent data point in the database.
#Calculate the date one year from the last date in the dataset.
one_year_previous = dt.datetime.strptime (most_recent_date, "%Y-%m-%d") - dt.timedelta (days = 365)
one_year_previous_string = one_year_previous.strftime ("%Y-%m-%d"

#Perform a query to retrieve the date and precipitation scores
precipitation_data = session.query (Measurement.date, Measurement.prcp).filter (Measurement.date >= one_year_previous).all ()

#Save the query results as a Pandas DataFrame.  Explicitly set the column names
precipitation_df = pd.DataFrame (precipitation_data, columns = ["Date", "Precipitation"])

#Sort the dataframe by date
precipitation_df = precipitation_df.sort_values ("Date")

#Use Pandas plotting with Matplotlib to plot the data
precipitation_df.plot (x = "Date", y = "Precipitation", title = "Precipitation Over the Last Twelve Months", rot = 90)
plt.xlabel ("Date")
plt.ylabel ("Inches")
plt.show ()

#Use Pandas to calculate the summary statistics for the precipitation data

#Calculate summary statistics for the precipitation data
summary_statistics = precipitation_df ["Precipitation"].describe ()

#Display the summary statistics as dataframe
summary_statistics_df = pd.DataFrame (summary_statistics)
print (summary_ststistics_df)

#Design a query to calculate the total number of stations in the dataset
total_stations = session.query (func.count (Station.station)).all ()
print (total_stations)

#Design a query to find the most active stations (i.e., which stations have the most rows?) List the stations and their counts in descending order.
active_stations = session.query (Measurement.station, func.count (Measurement.station)).group_by (Measurement.station).order_by (func.count (Measurement.station).desc ()).all ()

#Display the result
print (active_stations)

#Using the most active station id from the previous query, calculate the lowest, highest and average temperature
most_active_station = active_stations [0][0]

#Calculate the lowest, highest and average temperature for the most active station
temperature_statistics = session.func (min (Measurement.tobs).label ("Lowest Temperature"),
                                 func (max (Measurement.tobs).label ("Highest Temperature"),
                                 func (avg (Measurement.tobs).label ("Average Temperature").
                                 filter (Measurement.station == most_active_station).all ()
print (temperature_statistics)

#Using the most active station id
#Query the last 12 months of temperature observation data for this station and plot the results as a histogram

#Find the most recent date in the dataset

#Find the most active station

#Calculate the date one year from the most recent date in the dataset

#Query the last 12 months of temperature observation data for the most active station
temperature_data = session.query (Measurement.date, Measurement.tobs).filter (Measurement.station == most_active_station, Measurement.date >= one_year_previous_string).all ()

#Save the query results in a Pandas DataFrame
temperature_df = pd.DataFrame (temperature_data, columns = ["Date", "Temperature"])

#Convert the "Date" column to datetime
temperature_df ["Date"] = pd.to_datetime (temperature_df ["Date"])

#Displat the y-axis label before plotting
y_label_text = "Text (0.5, 4.183333333333314, "Temperature")"
print (y_label_text)

#Plot the results as a histogram
plt.hist (temperature_df ["Temperature"], bin = 12, label = "tobs")
plt.xlabel ("Temperature"] 
plt.ylabel ("Frequency")
plt.title ("f"Temperature Observation Data for Station {most_active_station} Last Twelve Months"")
plt.legend ()
plt.show ()

#Close session
session.close ()
