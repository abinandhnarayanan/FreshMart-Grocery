const searchInput = document.getElementById("searchInput");
const sortSelect = document.getElementById("sortSelect");
const container = document.getElementById("productContainer");

// Run only if these elements exist on the page
if (searchInput && sortSelect && container) {

    function filterProducts() {
        const value = searchInput.value.toLowerCase();

        document.querySelectorAll(".product-item").forEach(card => {
            const name = card.dataset.name.toLowerCase();
            card.style.display = name.includes(value) ? "" : "none";
        });
    }

    function sortProducts() {
        const cards = Array.from(document.querySelectorAll(".product-item"));

        if (sortSelect.value === "low") {
            cards.sort((a, b) => Number(a.dataset.price) - Number(b.dataset.price));
        } else if (sortSelect.value === "high") {
            cards.sort((a, b) => Number(b.dataset.price) - Number(a.dataset.price));
        } else if (sortSelect.value === "name") {
            cards.sort((a, b) => a.dataset.name.localeCompare(b.dataset.name));
        }

        cards.forEach(card => container.appendChild(card));
    }

    searchInput.addEventListener("keyup", filterProducts);
    sortSelect.addEventListener("change", sortProducts);
}