// Чёрный какао — минимум JS
document.addEventListener("DOMContentLoaded", () => {
  // Плавное появление карточек при загрузке
  document.querySelectorAll(".gallery__item, .event-list li, .staff__item").forEach((el, i) => {
    el.style.opacity = 0;
    el.style.transition = "opacity .5s ease, transform .5s ease";
    el.style.transform = "translateY(10px)";
    setTimeout(() => {
      el.style.opacity = 1;
      el.style.transform = "translateY(0)";
    }, i * 60);
  });
});