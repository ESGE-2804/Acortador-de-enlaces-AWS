const API_BASE = "http://3.93.175.66";

document.getElementById('shorten-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const originalUrl = document.getElementById('url-input').value;
  const resultDiv = document.getElementById('result');
  const errorDiv = document.getElementById('error');

  // Limpiar estados previos
  resultDiv.classList.add('hidden');
  errorDiv.classList.add('hidden');
  resultDiv.innerHTML = '';
  errorDiv.innerText = '';

  try {
    const res = await fetch(`${API_BASE}/shorten`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ original_url: originalUrl })
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || `Error del servidor: ${res.status}`);
    }

    const data = await res.json();
    resultDiv.innerHTML = `✅ Enlace corto: <a href="${data.short_url}" target="_blank" rel="noopener noreferrer">${data.short_url}</a>`;
    resultDiv.classList.remove('hidden');
    resultDiv.style.display = 'block';
  } catch (err) {
    errorDiv.innerText = `❌ ${err.message}`;
    errorDiv.classList.remove('hidden');
    errorDiv.style.display = 'block';
  }
});