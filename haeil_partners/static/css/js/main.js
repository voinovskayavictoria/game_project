// HAEIL & PARTNERS — минимальный JS
document.addEventListener("DOMContentLoaded", () => {
  // Подсветка активного года в архиве
  document.querySelectorAll(".yearbar a").forEach(a => {
    if (a.href === location.href) a.classList.add("is-active");
  });
});