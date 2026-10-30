const API_BASE = "http://<IP_PUBLICA_EC2>"; // Sin el puerto 8000 si usas Nginx

document.getElementById('shorten-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const originalUrl = document.getElementById('url-input').value;
    const resultDiv = document.getElementById('result');
    
    try {
        const res = await fetch(`${API_BASE}/shorten`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ original_url: originalUrl })
        });
        
        if (!res.ok) throw new Error("Error al acortar el enlace");
        
        const data = await res.json();
        resultDiv.innerHTML = `✅ Enlace corto: <a href="${data.short_url}" target="_blank">${data.short_url}</a>`;
        resultDiv.style.display = 'block';
    } catch (err) {
        alert(err.message);
    }
});
