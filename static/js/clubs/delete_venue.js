document.addEventListener("DOMContentLoaded", function () {
  const deleteAllRadio = document.getElementById("delete-venue-and-info");
  const deleteUnapprovedRadio = document.getElementById("delete_unapproved_info");
  const warning = document.getElementById("delete-venue-warning");
  const checkbox = document.getElementById("confirm-venue-delete");
  const button = document.getElementById("btn-delete-venue");

  // Add Event listeners
  deleteAllRadio.addEventListener("change", toggleWarning);
  deleteUnapprovedRadio.addEventListener("change", toggleWarning);
  checkbox.addEventListener("change", toggleWarning);

  // Initial check
  toggleWarning();

  // Helper Function
  function toggleWarning() {
    if (deleteAllRadio.checked) {
      // Show warning checkbox
      warning.classList.remove("visually-hidden");
      // Conditionally show button
      button.disabled = !checkbox.checked;
    } else {
      warning.classList.add("visually-hidden");
      button.disabled = false;
    }
  }
});
