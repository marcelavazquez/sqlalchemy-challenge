import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
# Home Site
@app.route("/")
def home():
    return (
        f"Welcome to the Climate App of Hawaii!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query all results to a dict using date as key and prcp as value
    results = session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()

    session.close()

    # Create dictionary
    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_list.append(prcp_dict)
    
    # jsonify list
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Station.station, Station.name).all()

    session.close()

    # Create dictionary
    stations_list= []
    for station, name in results:
        stations_dict = {}
        stations_dict[station] = name
        stations_list.append(stations_dict)

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # last year of data
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

     # Query the dates and temperature observations of the most active station for the last year of data.
    results = session.query(Measurement.date, Measurement.tobs).\
                    filter(Measurement.station == 'USC00519281').\
                    filter(Measurement.date >= year_ago).all()
    
    session.close()

    # Create dictionary
    tobs_list= []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

   # Query TMIN, TAVG and TMAX for all dates >= start date
    results = session.query(Measurement.date,\
                func.min(Measurement.tobs),\
                func.max(Measurement.tobs),\
                func.avg(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
    
    session.close()

    # Create dictionary
    start_list= []
    for date, min, max, avg in results:
        start_dict = {}
        start_dict["Date"] = date
        start_dict["TMIN"] = min
        start_dict["TMAX"] = max
        start_dict["TAVG"] = avg
        start_list.append(start_dict)

    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

     # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query TMIN, TAVG and TMAX for for dates between the start and end date inclusive
    results = session.query(Measurement.date,\
                func.min(Measurement.tobs),\
                func.max(Measurement.tobs),\
                func.avg(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()    
               

    session.close()

     # Create dictionary
    start_end_list= []
    for date, min, max, avg in results:
        start_end_dict = {}
        start_end_dict["Date"] = date
        start_end_dict["TMIN"] = min
        start_end_dict["TMAX"] = max
        start_end_dict["TAVG"] = avg
        start_end_list.append(start_end_dict)

    return jsonify(start_end_list)


if __name__ == "__main__":
    app.run(debug=True)