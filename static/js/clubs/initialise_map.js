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
  const infoWindow = new google.maps.InfoWindow();

  locations.forEach((location) => {
    const position = { lat: location.lat, lng: location.lng };
    marker = new google.maps.marker.AdvancedMarkerElement({
      position: position,
      map: map,
      title: `${location.name} (${location.clubs.join(", ")})`,
    });

    marker.addListener("gmp-click", () => {
      const content = `
        <h6 class="fs-6 mb-2">${location.name}</h6>
        <ul class="lh-lg mb-0 ps-3">
          ${location.clubs.map((club) => `<li>${club}</li>`).join("")}
        </ul>`;
      infoWindow.setContent(content);
      infoWindow.setPosition(position);
      infoWindow.open(map);
    });

    bounds.extend(position); // Add marker to bounds
  });

  map.fitBounds(bounds); // Auto-center & zoom to fit all markers
}
