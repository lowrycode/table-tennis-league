document.addEventListener("DOMContentLoaded", function () {
  const checkbox = document.querySelector(".confirmation-checkbox");
  const button = document.querySelector(".confirmation-required");

  if (checkbox && button) {
      checkbox.addEventListener("change", function () {
      button.disabled = !this.checked;
    });
  }
});