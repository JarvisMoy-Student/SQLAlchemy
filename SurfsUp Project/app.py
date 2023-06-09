# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import func, create_engine
from scipy import stats

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Home Route 
@app.route("/")
def home():
    return(f"/api/v1.0/precipitation <br>"
           f"/api/v1.0/stations <br>"
           f"/api/v1.0/tobs <br>"
           f"/api/v1.0/start/Enter State Date Format (yyyy-mm-dd) <br>"
           f"/api/v1.0/start/end/Enter State Date Format (yyyy-mm-dd)/Enter End Date Format (yyyy-mm-dd)")

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print(f"Request recieved for precipitation page...")

    # Query Precipitation results
    results = session.query(measurement.date, measurement.prcp).\
            filter (measurement.date <= '2017-08-23').\
            filter (measurement.date >= '2016-08-23').\
            filter (measurement.prcp != 'None').\
            order_by(measurement.date.desc()).all()

    # make empty list and store the dictionaries
    precipList = []
    for result in results:
        precipDict = {}
        precipDict["date"] = result["date"]
        precipDict["prcp"] = result["prcp"]
        precipList.append(precipDict)

    # Return a JSON list from the dataset
    return jsonify(precipList)


# Station Route
@app.route("/api/v1.0/stations")
def stations():
    print(f"Request received for list of stations...")

    # Query Station results

    results = session.query(measurement.station,func.count(measurement.id)).\
            group_by(measurement.station).\
            order_by(func.count(measurement.id).desc()).all() 
    

    stationList = []
    for result in results:
        stationDict = {}
        stationDict["station"] = result["station"]
        stationList.append(stationDict)

    # Return a JSON list of stations from the dataset
    return jsonify(stationList)

#Tobs Route
@app.route("/api/v1.0/tobs")
def tobs():
    print(f"Request received for most active station in the past year...")

    # Query the dates and temperature observations of the most-active station for the previous year of data.
    results = session.query(measurement.date, measurement.tobs).\
            filter (measurement.date <= '2017-08-23').\
            filter (measurement.date >= '2016-08-23').\
            filter (measurement.tobs != 'None').\
            filter (measurement.station == 'USC00519281').all()
    
    #session.close()
    
    tobsList = []

    for date,tobs in results:
        tobsdict={}
        tobsdict['date'] = date
        tobsdict['tobs'] = tobs
        
        tobsList.append(tobsdict)
   
   
   # Return a JSON list of temperature observations for the previous year.
    return jsonify(tobsList)
    
@app.route("/api/v1.0/start/<start>")
def start(start):
     print(f"Request received for start date...")
     
     results = session.query(measurement.tobs).\
            filter (measurement.date >= start).\
            filter (measurement.tobs != 'None' and measurement.tobs !='bb').all()
     
     session.close()

     # append the temp observations to list
     
     results = np.ravel(results)
    
     tobsList = []
     r = []

     for tobs in results:
        tobs_dict = {}

        tobsList.append(tobs)

     tobs_dict['min'] = stats.tmin(tobsList)
     tobs_dict['avg'] = stats.tmean(tobsList)
     tobs_dict['max'] = stats.tmax(tobsList)

     r.append(tobs_dict)

     return jsonify(r)


@app.route("/api/v1.0/start/end/<start>/<end>")
def end(start, end):
     print(f"Request received for enddate...")
     
     results = session.query(measurement.tobs).\
            filter (measurement.date >= start).\
            filter (measurement.date >= end).\
            filter (measurement.tobs != 'None' and measurement.tobs !='bb').all()
     
     session.close()
     
     # append the temp observations to list
     
     results = np.ravel(results)
    
     tobsList = []
     r = []

     for tobs in results:
        tobs_dict = {}

        tobsList.append(tobs)

     tobs_dict['min'] = stats.tmin(tobsList)
     tobs_dict['avg'] = stats.tmean(tobsList)
     tobs_dict['max'] = stats.tmax(tobsList)

     r.append(tobs_dict)

     return jsonify(r)


if __name__ == "__main__":
    app.run(debug=True) 