// ========================================================
// CONNECT — публичный JS
// ========================================================

// ---------- Основная инициализация ----------
document.addEventListener("DOMContentLoaded", () => {

  // автоскролл чата к последнему сообщению
  const box = document.getElementById("messages");
  if (box) box.scrollTop = box.scrollHeight;

  // плавное появление списка чатов
  document.querySelectorAll(".chat-item").forEach((el, i) => {
    el.style.opacity = 0;
    el.style.transition = "opacity .3s ease";
    setTimeout(() => { el.style.opacity = 1; }, i * 40);
  });

  // индикатор «печатает...» при отправке формы
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


// ---------- Поиск чатов (делегирование, всегда работает) ----------
(function () {

  // Уже привязан? Не дублируем.
  if (window.__chatSearchBound) return;
  window.__chatSearchBound = true;

  document.addEventListener("input", function (e) {
    var input = e.target;
    if (!input || input.id !== "chat-search") return;

    var list = document.getElementById("chat-list");
    if (!list) return;

    // пересобираем элементы каждый раз — на случай, если DOM обновился
    var items = Array.from(list.querySelectorAll(".chat-item"));
    var q = input.value.trim().toLowerCase();
    var visible = 0;

    items.forEach(function (el) {
      var nameEl = el.querySelector(".chat-item__name");
      var name = nameEl ? nameEl.textContent.toLowerCase() : "";
      var hit = !q || name.indexOf(q) !== -1;
      el.style.display = hit ? "" : "none";
      if (hit) visible++;
    });

    var empty = list.querySelector(".chat-empty");
    if (visible === 0 && !empty) {
      var d = document.createElement("div");
      d.className = "chat-empty";
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