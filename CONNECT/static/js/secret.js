// CONNECT // ROOT — скрытый JS
document.addEventListener("DOMContentLoaded", () => {
  const box = document.querySelector(".s-conversation__messages");
  if (box) box.scrollTop = box.scrollHeight;

  // Появление строк лога по одной
  document.querySelectorAll(".log-row").forEach((el, i) => {
    el.style.opacity = 0;
    el.style.transition = "opacity .3s ease";
    setTimeout(() => { el.style.opacity = 1; }, i * 50);
  });

  // Курсор-мигалка
  const blink = document.querySelector(".s-blink");
  if (blink) setInterval(() => {
    blink.style.opacity = blink.style.opacity === "0.2" ? "1" : "0.2";
  }, 600);
});