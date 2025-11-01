function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

document.getElementById("like-btn").addEventListener("click", function (e) {
  e.preventDefault();

  fetch(this.dataset.url, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      // Update like count
      const count = document.getElementById("like-count");
      count.textContent = data.total_likes;
    
      // Toggle button text
      const btn = document.getElementById("like-btn");
      btn.textContent = data.liked ? "❤️ Unlike" : "🤍 Like";
    
      // 🌟 Trigger heart splash when liked
      if (data.liked) {
        const splash = document.getElementById("heart-splash");
        for (let i = 0; i < 8; i++) {
          const heart = document.createElement("span");
          heart.classList.add("heart");
          heart.textContent = "❤️";
          // Random offset & size
          heart.style.left = `${Math.random() * 40 - 20}px`;
          heart.style.fontSize = `${14 + Math.random() * 10}px`;
          splash.appendChild(heart);
          // Remove after animation
          setTimeout(() => heart.remove(), 1000);
        }
      }
    });
    
});
    
