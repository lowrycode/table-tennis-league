/*
  Adds toggle functionality to elements with the `.btn-toggle` class.

  When a `.btn-toggle` button is clicked, it reads the `data-target` attribute
  to find a selector for the element to toggle. That target element's
  `.d-none` class is then toggled to show or hide it.

  Only the first element matching the selector is affected.
*/
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".btn-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const targetSelector = button.getAttribute("data-target");
      if (!targetSelector) return;

      const targetElem = document.querySelector(targetSelector);
      if (!targetElem) return;

      targetElem.classList.toggle("d-none");
    });
  });
});
