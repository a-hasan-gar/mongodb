//the maps api is setup above
window.onload = function() {

    var latlng = new google.maps.LatLng(51.5074, -0.1278); //Set the default location of map

    var map = new google.maps.Map(document.getElementById('map'), {

        center: latlng,

        zoom: 11, //The zoom value for map

        mapTypeId: google.maps.MapTypeId.ROADMAP

    });

    var marker = new google.maps.Marker({

        position: latlng,

        map: map,

        title: 'Place the marker for your location!', //The title on hover to display

        draggable: true //this makes it drag and drop

    });

    google.maps.event.addListener(marker, 'dragend', function(a) {

        console.log(a);

        document.getElementById('id_lon_lat').value = a.latLng.lat().toFixed(4) + ', ' + a.latLng.lng().toFixed(4); //Place the value in input box

      

    });

};