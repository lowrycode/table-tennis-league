/*
  Controls the visibility of a warning message and the enabled state of
  a delete button based on the selected delete option and confirmation checkbox.

  - Selecting the "Delete All" radio button:
    - Shows the div (with id `delete-approved-club-info-warning`) containing
      the warning message and confirmation checkbox.
    - Enables the delete button (with id `btn-delete-club-info`) only if
      the confirmation checkbox (with id `confirm-club-info-delete`) is checked.

  - Selecting the "Delete Unapproved" radio button:
    - Hides the div containing the warning message and confirmation checkbox.
    - Enables the delete button regardless of checkbox state.
*/
document.addEventListener("DOMContentLoaded", function () {
  const deleteAllRadio = document.getElementById("delete_all");
  const deleteUnapprovedRadio = document.getElementById("delete_unapproved");
  const warning = document.getElementById("delete-approved-club-info-warning");
  const checkbox = document.getElementById("confirm-club-info-delete");
  const button = document.getElementById("btn-delete-club-info");

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
