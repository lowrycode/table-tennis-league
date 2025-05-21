document.addEventListener("DOMContentLoaded", function () {
  const checkbox = document.getElementById("confirm-account-delete");
  const button = document.getElementById("btn-delete-account");

  if (checkbox && button) {
    checkbox.addEventListener("change", function () {
      button.disabled = !this.checked;
    });
  }
});