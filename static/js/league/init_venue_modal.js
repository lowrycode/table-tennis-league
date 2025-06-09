/*
  Initialises the body of the venue-modal that displays when the venue button
  is pressed for a specific fixture on the fixtures page.

  The modal body contains two divs
  - #modal-fixture-info: initialised with the home and away teams
  - #modal-venue-info: initialised with bootstrap spinner which is replaced by
  results from HTMX request
*/
document.addEventListener("click", function (e) {
  if (e.target.matches(".venue-btn")) {
    const modalFixtureInfo = document.getElementById("modal-fixture-info");
    const modalVenueInfo = document.getElementById("modal-venue-info");

    const home = e.target.dataset.home;
    const away = e.target.dataset.away;

    // Initialise fixture info - home vs away
    if (modalFixtureInfo) {
      modalFixtureInfo.textContent = `${home} vs ${away}`;
    }

    // Initialise venue info - bootstrap spinner
    if (modalVenueInfo) {
      modalVenueInfo.innerHTML = `
        <div class="d-flex justify-content-center align-items-center" style="min-height: 100px;">
          <div class="spinner-border text-primary" aria-hidden="true">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
      `;
    }
  }
});
