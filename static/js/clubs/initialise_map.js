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
    const marker = new google.maps.marker.AdvancedMarkerElement({
      position: position,
      map: map,
      title: `${location.name} (click for details)`,
    });

    marker.addListener("gmp-click", () => {
      const content = `
        <h6 class="fs-6 mb-2 px-2">${location.name}</h6>
        <p class="mb-2 fst-italic fw-semibold px-2">${location.address}</p>
        <p class="mb-0 px-2">Clubs that use this venue:</p>
        <ul class="lh-lg mb-0 ps-4 pe-2">
          ${location.clubs
            .map(
              (club) =>
                `<li><a href="#club-article-${club.id}" aria-label="Jump to club information">${club.name}</a></li>`
            )
            .join("")}
        </ul>`;
      infoWindow.setContent(content);
      infoWindow.setPosition(position);
      infoWindow.open(map);
    });

    bounds.extend(position); // Add marker to bounds
  });

  map.fitBounds(bounds); // Auto-center & zoom to fit all markers
}
