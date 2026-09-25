// CONNECT — публичный JS
document.addEventListener("DOMContentLoaded", () => {
  // Автоскролл к последнему сообщению
  const box = document.querySelector(".conversation__messages");
  if (box) box.scrollTop = box.scrollHeight;

  // Плавное появление
  document.querySelectorAll(".chat-item").forEach((el, i) => {
    el.style.opacity = 0;
    el.style.transition = "opacity .3s ease";
    setTimeout(() => { el.style.opacity = 1; }, i * 40);
  });
});