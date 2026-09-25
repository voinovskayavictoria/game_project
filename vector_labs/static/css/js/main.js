// VECTOR LABS — минимум JS
document.addEventListener("DOMContentLoaded", () => {
  // Плавное появление карточек
  document.querySelectorAll(".card, .team-card, .person, .gallery__item").forEach((el, i) => {
    el.style.opacity = 0;
    el.style.transform = "translateY(12px)";
    el.style.transition = "opacity .45s ease, transform .45s ease";
    setTimeout(() => {
      el.style.opacity = 1;
      el.style.transform = "translateY(0)";
    }, i * 40);
  });

  // «Живой» курсор в статус-карточке
  const dot = document.querySelector(".dot--ok");
  if (dot) {
    setInterval(() => {
      dot.style.opacity = dot.style.opacity === "0.4" ? "1" : "0.4";
    }, 900);
  }
});