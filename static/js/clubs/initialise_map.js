function initMap() {
  const locations = JSON.parse(
    document.getElementById("locations-data").textContent
  );
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 8, // initial zoom is adjusted later
    center: { lat: 0, lng: 0 }, // temporary center is adjusted later
    mapTypeControl: false, // disable Map and Satellite buttons
    mapId: "a66276713f8e807fdbe186bb", // Uses map style created in Google Console
  });

  const bounds = new google.maps.LatLngBounds();

  locations.forEach((location) => {
    const position = { lat: location.lat, lng: location.lng };
    new google.maps.marker.AdvancedMarkerElement({
      position: position,
      map: map,
      title: `${location.name} (${location.clubs.join(", ")})`,
    });

    bounds.extend(position); // Add marker to bounds
  });

  map.fitBounds(bounds); // Auto-center & zoom to fit all markers
}
