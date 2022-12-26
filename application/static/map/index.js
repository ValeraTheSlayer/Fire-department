// This example adds a search box to a map, using the Google Place Autocomplete
// feature. People can enter geographical searches. The search box will return a
// pick list containing a mix of places and predicted search terms.
// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">
function initAutocomplete() {
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 51.1333, lng: 71.4333 },
    zoom: 13,
    mapTypeId: "roadmap",
  });
  const contentString =
    '<div id="content">' +
    '<h1>Сығанақ, 24</h1>' +
    '<h3>Есиль район, Нур-Султан * Z05K7B0</h3>' +
    '<div class="row">' +
    '<div class="col">' +
    "<img src='/static/images/78_big.jpg' alt='jysan' style='width: 250px; height: 250px;'>" +
    "</div>" +
    '<div class="col">' +
    "<h5>Финасовый центр</h5> <ul><li>9 этажей</li><li>6 парковок</li><li>2 главных входа</li><li>3 аварийных выходов</li>" +
    "</div>" +
    "</div>" +
    "</div>";
  const infowindow = new google.maps.InfoWindow({
    content: contentString,
  });

  // Define the LatLng coordinates for the polygon's path.
  const FireDepartmentCoords_1 = [
    { lat: 51.132792,  lng: 71.359819 },
    { lat: 51.188164,  lng: 71.300326 },
    { lat: 51.253416,  lng: 71.374483 },
    { lat: 51.197151,  lng: 71.4758599},
    { lat: 51.127198,  lng: 71.616118},
    {lat: 51.106142, lng: 71.545052},
  ];
  const FireDepartmentCoords_2 = [
    { lat: 51.132792,  lng: 71.359819 },
    { lat: 51.028971,  lng: 71.316155 },
    { lat: 51.0280622,  lng: 71.4633179 },
    {lat: 51.106142, lng: 71.545052},
  ];
// Construct the polygon.
  const bermudaTriangle = new google.maps.Polygon({
    paths: FireDepartmentCoords_1,
    strokeColor: "#FF0000",
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: "#FF0000",
    fillOpacity: 0.0,
  });
  bermudaTriangle.setMap(map);
  const bermudaTriangle_2 = new google.maps.Polygon({
    paths: FireDepartmentCoords_2,
    strokeColor: "#FF0000",
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: "#0066FF",
    fillOpacity: 0.0,
  });
  bermudaTriangle_2.setMap(map);
  // Create the search box and link it to the UI element.
  const input = document.getElementById("pac-input");
  const searchBox = new google.maps.places.SearchBox(input);
  // map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
  // Bias the SearchBox results towards current map's viewport.
  map.addListener("bounds_changed", () => {
    searchBox.setBounds(map.getBounds());
  });
  let markers = [];
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener("places_changed", () => {
    const places = searchBox.getPlaces();
    if (places.length == 0) {
      return;
    }
    // Clear out the old markers.
    markers.forEach((marker) => {
      marker.setMap(null);
    });
    markers = [];
    // For each place, get the icon, name and location.
    const bounds = new google.maps.LatLngBounds();
    places.forEach((place) => {
      if (!place.geometry || !place.geometry.location) {
        console.log("Returned place contains no geometry");
        return;
      }
      const coordinate = new google.maps.LatLng(place.geometry.location.lat(), place.geometry.location.lng());
      const isWithinPolygon_1 = google.maps.geometry.poly.containsLocation(coordinate, bermudaTriangle);
      const isWithinPolygon_2 = google.maps.geometry.poly.containsLocation(coordinate, bermudaTriangle_2);
      // console.log(isWithinPolygon_1);
      // console.log(isWithinPolygon_2);
      // console.log(place.geometry.location.lat())
      // console.log(place.geometry.location.lng())
      // if(isWithinPolygon_1){
      //   $('#fire_department').attr('title', 'Пожарная часть 7');
      //   $('#fire_department').tooltip('toggle');
      // } else if(isWithinPolygon_2){
      //   $('#fire_department').attr('title', 'Пожарная часть 6');
      //   $('#fire_department').tooltip('toggle');
      // } else {
      //   alert('No in Area')
      // }

      const icon = {
        url: place.icon,
        size: new google.maps.Size(100, 100),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(50, 50),
      };
      // Create a marker for each place.
      markers.push(
        new google.maps.Marker({
          map,
          // icon,
          title: place.name,
          position: place.geometry.location,
        })
      );
    markers.forEach((marker) => {
      // marker.setMap(null);
       marker.addListener("click", () => {
        infowindow.open(map, marker);
      });
    });

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
  });
}