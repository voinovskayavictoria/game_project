// Мария Лебедева — минимальный JS
document.addEventListener("DOMContentLoaded", () => {
  // Плавный фейд статей
  document.querySelectorAll(".content > *").forEach((el, i) => {
    el.style.opacity = 0;
    el.style.transition = "opacity .5s ease";
    setTimeout(() => { el.style.opacity = 1; }, i * 40);
  });

  // Подсветка «красным маркером» при наведении — уже в CSS,
  // здесь просто убираем ссылку с клавиатурного фокуса
  document.querySelectorAll(".marker-link, a").forEach(a => {
    a.addEventListener("keydown", () => {});
  });
});