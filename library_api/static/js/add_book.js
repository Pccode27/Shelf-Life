const csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;

const formWrapper = document.querySelector(".form-wrapper");
const form = document.getElementById("form");

const title = document.querySelector("#title-input-wrapper .search-bar input");
const author = document.querySelector("#author-input-wrapper .search-bar input");
const genre = document.querySelector("#genre-input-wrapper .search-bar input");
const year = document.querySelector("#year-input-wrapper .search-bar input");
const pages = document.querySelector("#pages-input-wrapper .search-bar input");
const chapters = document.querySelector("#chapters-input-wrapper .search-bar input");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Basic validation
    if (year.value && (isNaN(year.value) || year.value < 1800 || year.value > 2026)) {
        alert("⚠️ Please enter a valid year (1800-2026).");
        return;
    }

    // Show loading feedback
    const loadingMsg = document.createElement("p");
    loadingMsg.textContent = "⏳ Adding book...";
    loadingMsg.style.color = "orange";
    formWrapper.appendChild(loadingMsg);

    try {
        const response = await fetch("/library/add/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token,
            },
            body: JSON.stringify({
                title: title.value.trim(),
                author: author.value.trim(),
                genre: genre.value.trim(),
                publishing_year: year.value.trim(),
                pages: pages.value.trim(),
                chapters: chapters.value.trim(),
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Success:", data);

        // Show success feedback
        formWrapper.innerHTML = `<h3 style="color:green;">✅ Book added successfully!</h3>`;
        
        // Redirect smoothly after 2s
        setTimeout(() => {
            window.location.href = "/";
        }, 2000);

    } catch (error) {
        console.error("Error:", error);
        formWrapper.innerHTML += `<p style="color:red;">❌ Failed to add book. Please try again.</p>`;
    }
});

window.onload = () => {
    if (form) form.reset();
};
