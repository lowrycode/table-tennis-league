/*
  Controls whether a button is enabled or disabled based on the state
  of a checkbox.

  The button must have the class name `.confirmation-required`.
  The checkbox must have the class name `.confirmation-checkbox`.

  Only the first elements matching each class are targeted.
*/
document.addEventListener("DOMContentLoaded", function () {
  const checkbox = document.querySelector(".confirmation-checkbox");
  const button = document.querySelector(".confirmation-required");

  if (checkbox && button) {
      checkbox.addEventListener("change", function () {
      button.disabled = !this.checked;
    });
  }
});