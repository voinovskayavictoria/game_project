document.addEventListener("DOMContentLoaded", () => {
  const box = document.getElementById("messages");
  if (box) box.scrollTop = box.scrollHeight;

  document.querySelectorAll(".chat-item").forEach((el, i) => {
    el.style.opacity = 0;
    el.style.transition = "opacity .3s ease";
    setTimeout(() => { el.style.opacity = 1; }, i * 40);
  });

  const form = document.getElementById("chat-form");
  if (form && box) {
    form.addEventListener("submit", () => {
      const hint = document.createElement("div");
      hint.className = "msg msg--typing";
      hint.textContent = "печатает...";
      box.appendChild(hint);
      box.scrollTop = box.scrollHeight;
    });
  }
});