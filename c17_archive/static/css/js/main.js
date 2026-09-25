// C-17 ARCHIVE — «печатная машинка» для команд + мигание
document.addEventListener("DOMContentLoaded", () => {
  // Появление строк промптов с задержкой
  const lines = document.querySelectorAll(".prompt-line");
  lines.forEach((el, i) => {
    el.style.opacity = 0;
    setTimeout(() => {
      el.style.transition = "opacity .3s ease";
      el.style.opacity = 1;
    }, i * 220);
  });

  // Плавное появление основных блоков
  document.querySelectorAll(".term-body > *").forEach((el, i) => {
    if (el.classList.contains("prompt-line")) return;
    el.style.opacity = 0;
    setTimeout(() => {
      el.style.transition = "opacity .5s ease";
      el.style.opacity = 1;
    }, 200 + i * 60);
  });
});