document.querySelectorAll(".clickable_line").forEach(row => {
    row.addEventListener("click", () => {
      window.location = row.dataset.href;
    });
  });
  