from flask import Flask, render_template, request
import json
from geocodio import GeocodioClient, exceptions
import re, requests
import time
#source_url = 'https://waterservices.usgs.gov/nwis/iv/?format=json&bBox=-120.234468,38.864888,-119.195384,40.263760&period=PT2H&parameterCd=00060,00065&siteType=LK,ST&siteStatus=all'


app = Flask(__name__)
geocodio_client = GeocodioClient('7d7bff58c5fbdf9b5afc0c7dd59d0bddcb0d9db')

@app.route("/")
@app.route("/rivers")
def rivers():
	project_name = 'Rivers'
	return render_template("project.html", project_name = project_name)

@app.route('/geocode', methods = ['POST'])
def geocode():
    jsdata = request.form['data']
    try:
    	geocode_result = get_coordinates(geocodio_client,jsdata)
    	return_data = json.dumps(geocode_result)
    	return return_data
    except exceptions.GeocodioDataError:
    	return 'Invalid Query'

def get_coordinates(gc_client, query):
	query_text = re.sub(r'/[^a-zA-Z0-9., \-]/g','',query)
	print('Geocoding: {}'.format(query_text))
	location = gc_client.geocode(query_text)
	coords = location.coords
	coordinates = [coords[0],coords[1]]
	return coordinates

	#meet some sort of regex requirement to strip non alpha numeric characters except , .

if __name__ == '__main__':
	app.run(port=5000,debug = True)

