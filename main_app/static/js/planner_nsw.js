var MapsAccountKey = "KvO9Xix-Fn8WuxK8VKnqSm7tukA-aPgycdk-tEpxoNk";
var map = new atlas.Map("map", {
    "subscription-key": MapsAccountKey
});
var routeLineOption = {
    width: 5,
    cap: "round",
    join: "round"
};

function getLocation(position) {
    $("#start_lon").val(position.coords.longitude);
    $("#start_lat").val(position.coords.latitude);
    var start_lon = parseFloat($("#start_lon").val());
    var start_lat = parseFloat($("#start_lat").val());
    startPoint = new atlas.data.Point([start_lon, start_lat]);
    var swLon = start_lon;
    var swLat = start_lat;
    var neLon = start_lon;
    var neLat = start_lat;

    map.setCamera({
        center: [start_lon, start_lat],
        zoom:16
    });

    var startPin = new atlas.data.Feature(startPoint, {
        title: "Current Location",
        icon: "pin-round-blue"
    });

    // Add pins to the map for the start and end point of the route
    map.addPins([startPin], {
        name: "Current Location",
        textFont: "SegoeUi-Regular",
        textOffset: [0, -20]
    });

    return startPoint;
}

var popup = new atlas.Popup();
map.addEventListener("mouseover", "bad-bus-stops", (e) => {
    var popupContentElement = document.createElement("div");
    popupContentElement.style.padding = "5px";
    for(var message of JSON.parse(e.features[0].properties.messages)) {
        var popupContentText = document.createElement("p");
        popupContentText.innerText = message;
        popupContentElement.appendChild(popupContentText);
    }

    popup.setPopupOptions({
        position: e.features[0].geometry.coordinates,
        content: popupContentElement
    });

    popup.open(map);
});



function drawRoute(journey) {
    var routeCoordinates = [];
    var good_bus_stops = [];
    var bad_bus_stops = [];

    var swLon = Math.min($("#start_lon").val(), $('#dest_lon').val());
    var swLat = Math.min($("#start_lat").val(), $('#dest_lat').val());
    var neLon = Math.max($("#start_lon").val(), $('#dest_lon').val());
    var neLat = Math.max($("#start_lat").val(), $('#dest_lat').val());
    map.setCameraBounds({
        bounds: [swLon, swLat, neLon, neLat],
        padding: [150,250,150,250]
    });

    var destPoint = new atlas.data.Point([$('#dest_lon').val(), $('#dest_lat').val()]);

    var destPin = new atlas.data.Feature(destPoint, {
        title: $("#dest_name").val(),
        icon: "pin-round-blue"
    });

    map.removeLayers(["destination", "route_walk", "route_bus", "good-bus-stops", "bad-bus-stops"]);
    map.removeHtml();
    // map.removeEventListener();

    map.addPins([destPin], {
        name: "destination",
        textFont: "SegoeUi-Regular",
        textOffset: [0, -20]
    });


    for (var leg of journey.legs) {
        var legCoordinates = leg.coords.map(nsw_coord => nsw_coord.reverse()); // coord of nsw is lat:lon and azure is lon:lat
        var routeLinestring = new atlas.data.LineString(legCoordinates);
        if(leg.transportation.product.class == 100) {
            routeLineOption.color = "#191818";
            routeLineOption.name = "route_walk";
        } else {
            // leg.transportation.currentOnboard
            // leg.stopSequence.stop.expectedOnboard

            for (var i=0; i < leg.stopSequence.length; i++) {
                var messages = [];
                var stop = leg.stopSequence[i];
                if (i == 0 && leg.transportation.currentOnboard / leg.transportation.capacity  > 0.75) {
                    messages.push("Bus crowded, currently on board: " + leg.transportation.currentOnboard);
                }
                if (stop.expectedOnboard > 10) {
                    messages.push(stop.expectedOnboard + " people waiting for this bus here");
                }
                if (messages.length > 0) {
                    var stop_point = new atlas.data.Feature(
                    new atlas.data.Point(stop.coord.reverse()),
                        {
                            messages: messages,
                            position: stop.coord
                        }
                    );
                    bad_bus_stops.push(stop_point)
                } else {
                    var stop_point = new atlas.data.Feature(
                    new atlas.data.Point(stop.coord.reverse()));
                    good_bus_stops.push(stop_point);
                }

            }

            routeLineOption.color = "#2272B9";
            routeLineOption.name = "route_bus";
        }
        map.addLinestrings([new atlas.data.Feature(routeLinestring)], routeLineOption);
    }

    if (good_bus_stops.length > 0) {
        map.addPins(good_bus_stops, {
            name: "good-bus-stops",
            cluster: false,
            icon: "pin-round-darkblue",
            iconSize: 0.7
        });
    }
    if (bad_bus_stops.length > 0) {
        map.addPins(bad_bus_stops, {
            name: "bad-bus-stops",
            cluster: false,
            icon: "pin-round-red",
            iconSize: 0.7
        });
    }
}

function showRoutes(journeys) {
    drawRoute(journeys[0]);
    for(var i=0;i<journeys.length;i++) {
        var journey = journeys[i];
        var journeyListItemElement = document.createElement("li");
    }
}

function searchResultsHandler(locations) {
    var searchInfoPanelBody = document.getElementById("search-info");
    searchInfoPanelBody.innerHTML = "";

    for(var i=0;i<locations.length;i++) {
        var location = locations[i];
        var resultListItemElement = document.createElement("li");
        resultListItemElement.dataset.lat = location.coord[0];
        resultListItemElement.dataset.lon = location.coord[1];
        resultListItemElement.dataset.id = location.id;
        resultListItemElement.dataset.name = location.name;
        resultListItemElement.classList.add('list-group-item');
        resultListItemElement.innerHTML = resultListItemElement.dataset.name;

        resultListItemElement.addEventListener("click", function (event) {
            var dest = event.target;
            var data = {
                "origin_lon": $("#start_lon").val(),
                "origin_lat": $("#start_lat").val(),
                "dest": dest.dataset.id
            };
            $('#dest_lon').val(dest.dataset.lon);
            $('#dest_lat').val(dest.dataset.lat);
            $('#dest_name').val(dest.dataset.name);

            $.ajax({url: "/map/route_planner", data: data, success: function(result){
               result = JSON.parse(result);
               showRoutes(result);
            }});
            searchInfoPanelBody.innerHTML = "";

        });

        searchInfoPanelBody.appendChild(resultListItemElement);
    }
}

function debounce(fn, duration) {
  var timer;
  return function(){
    clearTimeout(timer);
    timer = setTimeout(fn, duration);
  }
}

var searchInput = document.getElementById("search-input");
searchInput.addEventListener("keyup", debounce(function (e) {
    var searchInputValue = searchInput.value;
    var result;
    $.ajax({url: "/map/stop_finder", data: {'dest': searchInputValue }, success: function(result){
       result = JSON.parse(result);
       searchResultsHandler(result)
    }});
}, 300));

function error(error) {
    alert("get current location failed, using default location");
    console.log(error.message);
    var start_lon = $("#start_lon").val();
    var start_lat = $("#start_lat").val();
    startPoint = new atlas.data.Point([start_lon, start_lat]);

    map.setCamera({
        center: [start_lon, start_lat],
        zoom:16
    });

    var startPin = new atlas.data.Feature(startPoint, {
        title: "Current Location",
        icon: "pin-round-blue"
    });

    // Add pins to the map for the start and end point of the route
    map.addPins([startPin], {
        name: "Current Location",
        textFont: "SegoeUi-Regular",
        textOffset: [0, -20]
    });

}

navigator.geolocation.getCurrentPosition(getLocation, error);
