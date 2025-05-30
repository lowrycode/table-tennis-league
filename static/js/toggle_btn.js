/*
  Adds toggle functionality to elements with the `.btn-toggle` class.

  When a `.btn-toggle` button is clicked, it reads the `data-target` attribute
  to find a selector for the element to toggle. That target element's
  `.d-none` class is then toggled to show or hide it.

  Only the first element matching the selector is affected.
*/
function attachToggleListeners() {
  document.querySelectorAll(".btn-toggle").forEach((button) => {
    // Avoid attaching duplicate listeners
    if (button.dataset.toggleListenerAttached) return;

    // Add event listener
    button.addEventListener("click", () => {
      const targetSelector = button.getAttribute("data-target");
      if (!targetSelector) return;

      const targetElem = document.querySelector(targetSelector);
      if (!targetElem) return;

      targetElem.classList.toggle("d-none");
    });

    // Add dataset to show event listener is assigned to button
    button.dataset.toggleListenerAttached = "true";
  });
}

// Attach on initial page load
document.addEventListener("DOMContentLoaded", attachToggleListeners);

// Reattach after HTMX swaps new content into DOM
document.body.addEventListener("htmx:afterSettle", attachToggleListeners);
