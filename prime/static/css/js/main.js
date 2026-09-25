// PRIME SYSTEMS — минимальный JS
document.addEventListener("DOMContentLoaded", () => {
  // Плавное появление секций (необязательно, чисто для «живости»)
  document.querySelectorAll(".section").forEach(el => {
    el.style.opacity = 0;
    el.style.transition = "opacity .4s ease";
    requestAnimationFrame(() => { el.style.opacity = 1; });
  });
});