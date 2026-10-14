// 본문 그림을 누르면 화면 크기로 크게 보여 준다. 다시 누르거나 Esc로 닫는다.
// navigation.instant로 페이지가 바뀌어도 동작하도록 document에 한 번만 건다.
(function () {
  var MIN = 120; // 이보다 작게 그려진 그림(아이콘 등)은 대상에서 뺀다
  var box = null;

  function target(el) {
    if (!el || el.tagName !== "IMG") return null;
    if (!el.closest(".md-content") || el.closest("a") || el.closest(".twemoji")) return null;
    if (el.getBoundingClientRect().width < MIN) return null;
    return el;
  }

  function close() {
    if (!box) return;
    box.remove();
    box = null;
    document.documentElement.classList.remove("cc-lightbox-open");
  }

  function open(img) {
    close();
    box = document.createElement("div");
    box.className = "cc-lightbox";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-label", img.alt || "그림 크게 보기");
    var big = document.createElement("img");
    big.src = img.currentSrc || img.src;
    big.alt = img.alt || "";
    box.appendChild(big);
    var cap = img.closest("figure") && img.closest("figure").querySelector("figcaption");
    if (cap || img.alt) {
      var t = document.createElement("div");
      t.className = "cc-lightbox-caption";
      t.textContent = cap ? cap.textContent : img.alt;
      box.appendChild(t);
    }
    box.addEventListener("click", close);
    document.body.appendChild(box);
    document.documentElement.classList.add("cc-lightbox-open");
  }

  document.addEventListener("click", function (e) {
    var img = target(e.target);
    if (!img) return;
    e.preventDefault();
    open(img);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") close();
  });
  document.addEventListener("mouseover", function (e) {
    var img = target(e.target);
    if (img) img.style.cursor = "zoom-in";
  });
})();
