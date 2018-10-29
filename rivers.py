from flask import Flask, render_template, request
import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
#source_url = 'https://waterservices.usgs.gov/nwis/iv/?format=json&bBox=-120.234468,38.864888,-119.195384,40.263760&period=PT2H&parameterCd=00060,00065&siteType=LK,ST&siteStatus=all'


app = Flask(__name__)


@app.route("/")
@app.route("/rivers")
def rivers():
	project_name = 'Rivers'
	return render_template("project.html", project_name = project_name)

@app.route('/update_stations', methods = ['POST'])
def update_stations():
    jsdata = request.form['javascript_data']
    print('POST received!')
    return json.dumps(parse_USGS_data(jsdata))

def get_USGS_data(url):
	t0 = time.time()
	try:
		print('Requesting data from USGS.')
		#use requests to download the source url
		response = requests_retry_session().get(url)
		#unpack JSON into a dictionary
		data = json.loads(response.text)
		return data
	except Exception as x:
		print('It failed :(', x.__class__.__name__)
		print('Attempted URL: '+ url)
	else:
		print('It eventually worked', response.status_code)
	finally:
		t1 = time.time()
		print('Took', t1 - t0, 'seconds')

#Retry code for reliability from: https://www.peterbe.com/plog/best-practice-with-retries-with-requests
def requests_retry_session(retries=3,backoff_factor=0.3,status_forcelist=(500, 502, 504),session=None,):
	session = session or requests.Session()
	retry = Retry(total=retries,read=retries,connect=retries,backoff_factor=backoff_factor,status_forcelist=status_forcelist)
	adapter = HTTPAdapter(max_retries=retry)
	session.mount('http://', adapter)
	session.mount('https://', adapter)
	return session

def parse_USGS_data(url): #update to not use sites explicitly
	"""
	Purpose: Makes a request to the USGS based on a URL and parses dictionary created from the response JSON
	Returns: Dictionary of dictionaries
	"""
	data = get_USGS_data(url)
	sites = {}
	#loop through each timeSeries entry
	for entry in data['value']['timeSeries']:
		#Extract the variables we are interested in
		site_name = entry['sourceInfo']['siteName']
		site_code = int(entry['sourceInfo']['siteCode'][0]['value']) #for some reason forcing an int here works. I do not know why.
		site_type_code = entry['sourceInfo']['siteProperty'][0]['value']
		latitude = entry['sourceInfo']['geoLocation']['geogLocation']['latitude']
		longitude = entry['sourceInfo']['geoLocation']['geogLocation']['longitude']
		#check if we already have the site. if not, create one. Duplicate sites may appear if 
		#more than one parameter is measured at a site. 
		if site_code not in sites.keys():
			sites[site_code] = {'site_name' : site_name,
								'site_code' : site_code,
								'site_type_code' : site_type_code,
								'coordinates' : [latitude, longitude]
								}
	return sites

@app.context_processor
def parse_USGS_data_context(): #update to not use sites explicitly
	"""
	Purpose: Makes a request to the USGS based on a URL and parses dictionary created from the response JSON
	Returns: Dictionary of dictionaries
	"""
	def parse(url):
		data = get_USGS_data(url)
		print(url)
		sites = {}
		#loop through each timeSeries entry
		for entry in data['value']['timeSeries']:
			#Extract the variables we are interested in
			site_name = entry['sourceInfo']['siteName']
			site_code = int(entry['sourceInfo']['siteCode'][0]['value']) #for some reason forcing an int here works. I do not know why.
			site_type_code = entry['sourceInfo']['siteProperty'][0]['value']
			latitude = entry['sourceInfo']['geoLocation']['geogLocation']['latitude']
			longitude = entry['sourceInfo']['geoLocation']['geogLocation']['longitude']
			#check if we already have the site. if not, create one. Duplicate sites may appear if 
			#more than one parameter is measured at a site. 
			if site_code not in sites.keys():
				sites[site_code] = {'site_name' : site_name,
									'site_code' : site_code,
									'site_type_code' : site_type_code,
									'coordinates' : [latitude, longitude]
									}
		return sites
	return dict(parse=parse)


if __name__ == '__main__':
	app.run(port=5000,debug = True)

