const deleteButtons = document.querySelectorAll('.delete-button');

let csrf_token = "";
const csrfInput = document.getElementsByName("csrfmiddlewaretoken")[0];
if (csrfInput) {
    csrf_token = csrfInput.value;
}

deleteButtons.forEach(button => {
    button.addEventListener('click', async () => {
        const confirmDelete = confirm("Are you sure you want to delete this book?");
        if (!confirmDelete) return;

        const url = button.dataset.url; // ✅ straight from template

        try {
            const response = await fetch(url, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrf_token,
                },
            });

            if (response.ok) {
                console.log("✅ Book deleted successfully!");
                const card = button.closest(".card");
                if (card) {
                    card.style.transition = "opacity 0.5s";
                    card.style.opacity = "0";
                    setTimeout(() => card.remove(), 500);
                } else {
                    window.location.reload();
                }
            } else {
                const errorText = await response.text();
                console.error("❌ Delete failed:", response.status, errorText);
                alert("Delete failed: " + response.status);
            }
        } catch (error) {
            console.error("Error:", error);
            alert("❌ Error deleting book.");
        }
    });
});
