// frontend/script.js
const apiUrl = "http://localhost:8000";

async function fetchProducts() {
    const res = await fetch(`${apiUrl}/products/`);
    const data = await res.json();
    displayProducts(data);
}

async function searchProducts() {
    const q = document.getElementById('searchBox').value;
    const res = await fetch(`${apiUrl}/search/?q=${q}`);
    const data = await res.json();
    displayProducts(data);
}

function displayProducts(products) {
    const list = document.getElementById('productList');
    list.innerHTML = '';
    products.forEach(p => {
        const div = document.createElement('div');
        div.className = 'product';
        div.innerHTML = `
            <strong>${p.title}</strong> - ₹${p.price}<br>
            ${p.description}<br>
            <em>Category:</em> ${p.category}<br>
            <button onclick="deleteProduct(${p.id})">Delete</button>
            <button onclick="showSuggestions(${p.id})">Similar</button>
        `;
        list.appendChild(div);
    });
}

async function addProduct(e) {
    e.preventDefault();
    const product = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        price: parseFloat(document.getElementById('price').value),
        category: document.getElementById('category').value
    };
    await fetch(`${apiUrl}/products/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(product)
    });
    fetchProducts();
    e.target.reset();
}

async function deleteProduct(id) {
    await fetch(`${apiUrl}/products/${id}`, { method: "DELETE" });
    fetchProducts();
}

async function showSuggestions(id) {
    const res = await fetch(`${apiUrl}/suggestions/${id}`);
    const data = await res.json();
    alert("🧠 Suggested Products:\n" + data.map(p => p.title).join("\n"));
}

fetchProducts();
