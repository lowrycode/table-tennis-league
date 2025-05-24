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
