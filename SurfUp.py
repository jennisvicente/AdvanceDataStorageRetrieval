#Flask 
import numpy as np
import pandas as pd

import datetime as dt
from datetime import timedelta, datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
#Queries
#-------Precipitation-----------
precipitation_results = session.query(Measurement.date, Measurement.prcp).\
order_by(Measurement.date).filter(Measurement.date.between(dt.date(2016, 8, 23),dt.date(2017, 8, 23))).all()
df = pd.DataFrame(precipitation_results, columns=['Measurement Date', 'Precipitation'])
df=df.dropna()
df1=df.groupby('Measurement Date').sum()
df1=df1.to_dict('index')
df1
#--------------Stations---------
df2 =pd.read_sql_query(session.query(Station.name).statement, engine)
df2=df2.to_dict()
df2
#-------------Tobs--------------
df3= pd.read_sql_query(session.query(Measurement.date, Measurement.tobs).\
filter(Measurement.date.between(dt.date(2016, 8, 23), dt.date(2017, 8, 23), Measurement.station== 'USC00519281')).statement, engine)
df3=df3.to_dict('records')
#-----------Temps---------------
#Start Date
start_date = datetime.strptime('2016-08-05', '%Y-%m-%d').date()
start= pd.read_sql_query(session.query(func.max(Measurement.tobs), \
                            func.min(Measurement.tobs),\
                            func.avg(Measurement.tobs)).\
                            filter(Measurement.date >= start_date).statement, engine)
start.index=['08-05-2016']
start.columns=['Min Temp','Max Temp','Avg Temp']
df4=start.to_dict('index')
#Start to End
start_date = datetime.strptime('2016-08-05', '%Y-%m-%d').date()
end_date = datetime.strptime('2017-08-05', '%Y-%m-%d').date()
start_end= pd.read_sql_query(session.query(func.max(Measurement.tobs), \
                            func.min(Measurement.tobs),\
                            func.avg(Measurement.tobs)).\
                            filter(Measurement.date.between(dt.date(start_date), dt.date(end_date)).statement, engine)

start_end.index=['Dates']
start_end.columns=['Min Temp','Max Temp','Avg Temp']
df5=start_end.to_dict('index')



#--------------------------------------------Flask-------------------------------------------------

app = Flask(__name__)




@app.route("/")
def welcome():
    return (
        f" Surf UP available API!<br/>"
        f"Available Routes:<br/>"
        f"--- Dates and Precipitation observations: Last year ---<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"--- Stations : City ---<br/>"
        f"/api/v1.0/stations<br/>"
        f"--- Temperature observations: Last year ---<br/>"
        f"/api/v1.0/tobs<br/>"
        f"--- Dates and Precipitation observations: Last year ---<br/>"
        f"/api/v1.0/calc_temps/start<br/>"
        
        f"/api/v1.0/calc_temps/start_end/<end>"
        
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of dates and precipitation observations"""
    precipitation_ = list(np.ravel(df1))
    return jsonify(precipitation_)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    return jsonify(df2)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of dates and temperature observations from a year from the last data point"""
    return jsonify(df3)

@app.route("/api/v1.0/calc_temps/start")
def calc_temps(start='start_date'):
    """Return a list of dates and temperature observations from a year from the last data point"""
    return jsonify(df4)
                             
@app.route("/api/v1.0/calc_temps/start_end")
def calc_temps2(start='start_date', end='end_date'):
    """Return a list of dates and temperature observations from a year from the last data point"""
    return jsonify(df5)


    

if __name__ == "__main__":
    app.run(debug=True)





