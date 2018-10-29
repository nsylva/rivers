sites = []
var mymap = L.map('my-map');
var basemap = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
});
					
mymap.on('load moveend', function(e) {
   	var bounds = mymap.getBounds();
   	var southWest = bounds.getSouthWest();
   	var northEast = bounds.getNorthEast();
   	var boundsStr = southWest.lng.toFixed(6) + ',' + southWest.lat.toFixed(6) + ','+ northEast.lng.toFixed(6) + ','+ northEast.lat.toFixed(6);
   	var baseURL = 'https://waterservices.usgs.gov/nwis/iv/?format=json&period=PT2H&parameterCd=00060,00065&siteType=LK,ST&siteStatus=all&bBox=';
   	var newRequestURL = baseURL + boundsStr
   	$.post( "/update_stations", {
    	javascript_data: newRequestURL
	}).done(function(response) {
		var obj = JSON.parse(response)
		for (var key in obj){
			var site = obj[key]
			var site_code = site['site_code']
			if(sites.includes(site_code) === false) {
				var coordinates = site['coordinates']							
				var site_type_code = site['site_type_code']
				var site_name = site['site_name']
				var marker = L.marker(coordinates)
				var popupContent = 
					'<ul class="list-unstyled">\
					<li><b>'+ site_name +'</b></li>\
					<li>Site ID: '+ site_code +'</li>\
					<li>Site Type: ' + site_type_code + '</li>\
					<li>Coordinates: '+ coordinates[0] +', ' + coordinates[1]+ '</li>';
					marker.bindPopup(popupContent).openPopup();
					marker.addTo(mymap);
					sites.push(site_code)
			}	
		}
	});
});
mymap.setView([39.323041, -120.185002], 13);
basemap.addTo(mymap);