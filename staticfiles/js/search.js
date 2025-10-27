// Blog Search
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("blog-search-form");
  const overlay = document.getElementById("loading-overlay");
  const blogGrid = document.getElementById("blog-grid");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const query = document.getElementById("search-input").value;
    const url = form.action + "?q=" + encodeURIComponent(query);

    overlay.style.display = "flex"; // show spinner

    fetch(url, {
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => response.text())
      .then((data) => {
        const parser = new DOMParser();
        const html = parser.parseFromString(data, "text/html");
        const newBlogGrid = html.querySelector("#blog-grid");

        if (newBlogGrid) {
          blogGrid.innerHTML = newBlogGrid.innerHTML;
        } else {
          blogGrid.innerHTML = "<p>No matching blog items found.</p>";
        }

        overlay.style.display = "none";
      })
      .catch((error) => {
        console.error("Error:", error);
        overlay.style.display = "none";
      });
  });
});
