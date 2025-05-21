document.addEventListener("DOMContentLoaded", function () {
  const deleteAllRadio = document.getElementById("delete_all");
  const deleteUnapprovedRadio = document.getElementById("delete_unapproved");
  const warning = document.getElementById("delete-approved-club-info-warning");
  const checkbox = document.getElementById("confirm-club-info-delete");
  const button = document.getElementById("btn-delete-club-info");

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
