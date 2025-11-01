(function () {
  const rootId = "toast-root";

  function ensureRoot() {
    let root = document.getElementById(rootId);
    if (!root) {
      root = document.createElement("div");
      root.id = rootId;
      root.setAttribute("aria-live", "polite");
      root.setAttribute("aria-atomic", "true");
      document.body.appendChild(root);
    }
    return root;
  }

  function icon(level) {
    const m = {
      success: `<svg viewBox="0 0 24 24"><path d="M9 16l-3.5-3.5 1.4-1.4L9 13.2l7.1-7.1 1.4 1.4z"/></svg>`,
      info: `<svg viewBox="0 0 24 24"><path d="M11 7h2v2h-2zm0 4h2v6h-2z"/><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor"/></svg>`,
      warning: `<svg viewBox="0 0 24 24"><path d="M1 21h22L12 2 1 21zm12-3h-2v2h2zm0-8h-2v6h2z"/></svg>`,
      error: `<svg viewBox="0 0 24 24"><path d="M18.3 5.7L5.7 18.3m0-12.6L18.3 18.3" stroke-width="2" stroke="currentColor"/></svg>`,
    };
    return m[level] || m.info;
  }

  function createToast(text, level, ttl = 4000) {
    const root = ensureRoot();
    const el = document.createElement("div");
    el.className = `toast ${level || "info"}`;
    el.setAttribute("role", "status");
    el.innerHTML = `
        <div class="toast__icon" aria-hidden="true">${icon(level)}</div>
        <div class="toast__text"></div>
        <button class="toast__close" aria-label="Close">&times;</button>
        <div class="toast__progress" style="--ttl:${ttl}ms"></div>
      `;
    el.querySelector(".toast__text").textContent = text;

    const close = () => {
      el.classList.remove("show");
      el.addEventListener("transitionend", () => el.remove(), { once: true });
    };

    const button = el.querySelector(".toast__close");
    button.addEventListener("click", close);

    // Auto-hide timer
    let timer = setTimeout(close, ttl);

    // Pause on hover
    el.addEventListener("mouseenter", () => {
      el.classList.add("paused");
      clearTimeout(timer);
    });
    el.addEventListener("mouseleave", () => {
      el.classList.remove("paused");
      // Estimate remaining by progress width
      const bar = el.querySelector(".toast__progress");
      const w = parseFloat(getComputedStyle(bar).width);
      const total = el.getBoundingClientRect().width;
      const ratio = total > 0 ? w / total : 0;
      const remaining = Math.max(200, Math.floor(ttl * ratio));
      timer = setTimeout(close, remaining);
    });

    root.appendChild(el);
    requestAnimationFrame(() => el.classList.add("show"));
  }

  function renderQueue(queue) {
    if (!Array.isArray(queue)) return;
    queue.forEach((item) =>
      createToast(
        item.text || String(item),
        item.level || "info",
        item.ttl || 4000
      )
    );
  }

  // Public API
  window.showToast = (text, level = "info", ttl = 4000) =>
    createToast(text, level, ttl);
  window.renderDjangoToasts = (queue) => renderQueue(queue);
})();
