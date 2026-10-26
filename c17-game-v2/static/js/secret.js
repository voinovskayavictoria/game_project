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

// ---------- Поиск чатов (секретная часть) ----------
(function () {
  if (window.__secretSearchBound) return;
  window.__secretSearchBound = true;

  document.addEventListener("input", function (e) {
    var input = e.target;
    if (!input || input.id !== "chat-search") return;

    var list = document.getElementById("chat-list");
    if (!list) return;

    var items = Array.from(list.querySelectorAll(".s-chat"));
    var q = input.value.trim().toLowerCase();
    var visible = 0;

    items.forEach(function (el) {
      var nameEl = el.querySelector(".s-chat__name");
      var name = nameEl ? nameEl.textContent.toLowerCase() : "";
      var hit = !q || name.indexOf(q) !== -1;
      el.style.display = hit ? "" : "none";
      if (hit) visible++;
    });

    var empty = list.querySelector(".s-chat-empty");
    if (visible === 0 && !empty) {
      var d = document.createElement("div");
      d.className = "s-chat-empty";
      d.textContent = "ничего не найдено";
      list.appendChild(d);
    } else if (visible > 0 && empty) {
      empty.remove();
    }
  });

  document.addEventListener("keydown", function (e) {
    var input = e.target;
    if (!input || input.id !== "chat-search") return;
    if (e.key === "Escape") {
      input.value = "";
      input.dispatchEvent(new Event("input", { bubbles: true }));
    }
  });
})();