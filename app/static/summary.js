const API_BASE_URL = "";

const user_id = localStorage.getItem("user_id");
const month = new Date().toISOString().slice(0, 7);

if (!user_id) {
  alert("Session expired. Please start again.");
  window.location.href = "index.html";
}

async function loadSummary() {
  const loading = document.getElementById("loading");
  const content = document.getElementById("content");

  try {
    const res = await fetch(`${API_BASE_URL}/analysis/${user_id}/${month}`);
    if (!res.ok) throw new Error("API error");

    const data = await res.json();

    // OVERVIEW
    document.getElementById("summary").innerHTML = `
      <h3>Overview</h3>
      <p><strong>Monthly Income:</strong> ₹${data.total_income}</p>
      <p><strong>Total Expenses:</strong> ₹${data.total_spent}</p>
    `;

    // BREAKDOWN
    document.getElementById("breakdown").innerHTML = `
      <h3>50:30:20 Breakdown</h3>

      <p>Needs (${data.needs_percentage}%)</p>
      <div class="progress"><span class="needs-bar" style="width:${data.needs_percentage}%"></span></div>

      <p>Wants (${data.wants_percentage}%)</p>
      <div class="progress"><span class="wants-bar" style="width:${data.wants_percentage}%"></span></div>

      <p>Invest (${data.invest_percentage}%)</p>
      <div class="progress"><span class="invest-bar" style="width:${data.invest_percentage}%"></span></div>
    `;

    // AI TIPS
    const adviceDiv = document.getElementById("advice");
    adviceDiv.innerHTML = "<h3>💡 AI Insights</h3>";
    data.tips.forEach(tip => {
      adviceDiv.innerHTML += `<div class="ai-tip">${tip}</div>`;
    });

    loading.style.display = "none";
    content.style.display = "block";

  } catch (err) {
    console.error(err);
    loading.innerHTML = "❌ Failed to load analysis. Please refresh.";
  }
}

document.getElementById("restartBtn").addEventListener("click", () => {
  window.location.href = "index.html";
});

loadSummary();
