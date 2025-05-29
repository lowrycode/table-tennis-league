/*
  Controls the visibility of a warning message and the enabled state of
  a delete button based on the selected delete option and confirmation checkbox.

  - Selecting the "Delete Venue and Info" radio button:
    - Shows the div (with id `delete-venue-warning`) containing
      the warning message and confirmation checkbox.
    - Enables the delete button (with id `btn-delete-venue`) only if
      the confirmation checkbox (with id `confirm-venue-delete`) is checked.

  - Selecting the "Delete Unapproved Info" radio button:
    - Hides the div containing the warning message and confirmation checkbox.
    - Enables the delete button regardless of checkbox state.
*/
document.addEventListener("DOMContentLoaded", function () {
  const deleteAllRadio = document.getElementById("delete-venue-and-info");
  const deleteUnapprovedRadio = document.getElementById("delete_unapproved_info");
  const warning = document.getElementById("delete-venue-warning");
  const checkbox = document.getElementById("confirm-venue-delete");
  const button = document.getElementById("btn-delete-venue");

  // Add event listeners
  deleteAllRadio.addEventListener("change", toggleWarning);
  deleteUnapprovedRadio.addEventListener("change", toggleWarning);
  checkbox.addEventListener("change", toggleWarning);

  // Initialise state
  toggleWarning();

  // Helper function
  function toggleWarning() {
    if (deleteAllRadio.checked) {
      // Show warning message and confirmation checkbox
      warning.classList.remove("visually-hidden");
      // Enable or disable button
      button.disabled = !checkbox.checked;
    } else {
      warning.classList.add("visually-hidden");
      button.disabled = false;
    }
  }
});
