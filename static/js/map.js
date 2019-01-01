global_sites = {}
var mymap = L.map('my-map');
var basemap = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
});
function buildRequestURL(){
	var bounds = mymap.getBounds();
   	var southWest = bounds.getSouthWest();
   	var northEast = bounds.getNorthEast();
   	var boundsStr = southWest.lng.toFixed(6) + ',' + southWest.lat.toFixed(6) + ','+ northEast.lng.toFixed(6) + ','+ northEast.lat.toFixed(6);
   	var baseURL = 'https://waterservices.usgs.gov/nwis/iv/?format=json&period=PT2H&parameterCd=00060,00065&siteType=ST&siteStatus=all&bBox=';
   	var newRequestURL = baseURL + boundsStr;
   	return newRequestURL;
};

function parseUSGSData(data){
	var sites = {}
	var site_list = data['value']['timeSeries']
	for (var s = 0; s<site_list.length; s++){
		var site = site_list[s];
		var siteName = site['sourceInfo']['siteName']
		var siteCode = site['sourceInfo']['siteCode'][0]['value']
		var siteTypeCode = site['sourceInfo']['siteProperty'][0]['value']
		var latitude = site['sourceInfo']['geoLocation']['geogLocation']['latitude']
		var longitude = site['sourceInfo']['geoLocation']['geogLocation']['longitude']
		if (!(sites.hasOwnProperty(siteCode))){
			var newSite = {}
			newSite['siteName'] = siteName
			newSite['siteCode'] = siteCode
			newSite['siteTypeCode'] = siteTypeCode
			newSite['coordinates'] = [latitude,longitude]
			newSite['measurements'] = {}
			sites[siteCode] = newSite
		}
		else {
			//just get the measurements
		}
	}
	return sites
};

//var parseMeasurements = function(site) {
//	var measurements = site['values'][0]['value']
//
//}

function validateSearchInput(input){
	return input.replace(/[^a-zA-Z0-9,. \-]/g, '');
};


function locationSearch(query){
	$.post('/geocode',{
		data : validateSearchInput(query)
	}).done(function(response){
		if (response == 'Invalid Query'){
			console.log('Invalid Query');
			$('#map-cont').prepend('<span class="alert alert-danger">Invalid Search</span>')
			
		}
		else {
			response = JSON.parse(response);
			mymap.setView(response,11);
		}
	})
	;

};
					
mymap.on('load moveend', function() {
   	var URL = buildRequestURL();
   	$.get(URL, function(data){
   		USGSData = parseUSGSData(data)
   		for (var key in USGSData){
			var site = USGSData[key]
			var site_code = site['siteCode']
			if (!(site_code in global_sites)) {
				//console.log('if statement working')
				var coordinates = site['coordinates']							
				var site_type_code = site['siteTypeCode']
				var site_name = site['siteName']
				var marker = L.marker(coordinates);
				var popupContent = 
					'<ul class="list-unstyled">\
					<li><b>'+ site_name +'</b></li>\
					<li>Site ID: '+ site_code +'</li>\
					<li>Site Type: ' + site_type_code + '</li>\
					<li>Coordinates: '+ coordinates[0] +', ' + coordinates[1]+ '</li>';
				marker.bindPopup(popupContent).openPopup();
				marker.addTo(mymap);
				global_sites[site_code] = site				
   			}
   			else {
   				//just add new measurements
   			}
   		}
	});
});
mymap.setView([39.323041, -120.185002], 13);
basemap.addTo(mymap);
