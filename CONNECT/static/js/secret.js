document.addEventListener("DOMContentLoaded", () => {
  const box = document.getElementById("messages");
  if (box) box.scrollTop = box.scrollHeight;

  document.querySelectorAll(".s-chat").forEach((el, i) => {
    el.style.opacity = 0;
    el.style.transition = "opacity .3s ease";
    setTimeout(() => { el.style.opacity = 1; }, i * 30);
  });

  const blink = document.querySelector(".s-blink");
  if (blink) setInterval(() => {
    blink.style.opacity = blink.style.opacity === "0.2" ? "1" : "0.2";
  }, 600);
});