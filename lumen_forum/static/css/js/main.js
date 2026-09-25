document.addEventListener("DOMContentLoaded", () => {
  // --- Мини-лайтбокс ---
  const overlay = document.createElement("div");
  overlay.className = "lightbox";
  overlay.style.cssText = `
    position: fixed; inset: 0; background: rgba(0,0,0,.88);
    display: none; align-items: center; justify-content: center;
    z-index: 1000; cursor: zoom-out;
  `;
  const overlayImg = document.createElement("img");
  overlayImg.style.cssText = "max-width:92vw;max-height:92vh;object-fit:contain;";
  overlay.appendChild(overlayImg);
  document.body.appendChild(overlay);

  overlay.addEventListener("click", () => { overlay.style.display = "none"; });

  document.querySelectorAll(".gallery img").forEach(img => {
    img.addEventListener("click", e => {
      e.preventDefault();
      overlayImg.src = img.src;
      overlay.style.display = "flex";
    });
  });

  // --- Плавное появление секций ---
  document.querySelectorAll(".section").forEach(el => {
    el.style.opacity = 0;
    el.style.transition = "opacity .4s ease";
    requestAnimationFrame(() => { el.style.opacity = 1; });
  });
});