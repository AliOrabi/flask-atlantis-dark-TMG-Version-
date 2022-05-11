const settings = {
	"async": true,
	"crossDomain": true,
	"url": "https://wft-geo-db.p.rapidapi.com/v1/geo/adminDivisions",
	"method": "GET",
	"headers": {
		"X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
		"X-RapidAPI-Key": "9e8b217857msh22bdda8117f7d6cp10f33djsn570cfb6a09dc"
	}
};

$.ajax(settings).done(function (response) {
	console.log(response);
});