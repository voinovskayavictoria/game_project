// ORBIT DATA — минимум JS
document.addEventListener("DOMContentLoaded", () => {
  // Плавное появление карточек
  document.querySelectorAll(".card, .team-card, .person, .gallery__item, .doc-card").forEach((el, i) => {
    el.style.opacity = 0;
    el.style.transform = "translateY(10px)";
    el.style.transition = "opacity .4s ease, transform .4s ease";
    setTimeout(() => {
      el.style.opacity = 1;
      el.style.transform = "translateY(0)";
    }, i * 35);
  });

  // «Живые» бары в мини-дашборде
  document.querySelectorAll(".chart-bar").forEach((bar, i) => {
    const h = bar.style.getPropertyValue("--h");
    bar.style.height = "0";
    setTimeout(() => {
      bar.style.transition = "height .7s ease";
      bar.style.height = h;
    }, 200 + i * 60);
  });
});