const API_BASE_URL = "";

// ===== SESSION =====
const user_id = localStorage.getItem("user_id");
const income = Number(localStorage.getItem("income")) || 0;
const month = new Date().toISOString().slice(0, 7);

if (!user_id) {
  alert("User session not found. Please start again.");
  window.location.href = "index.html";
}

// ===== DOM =====
const form = document.getElementById("expenseForm");
const tableBody = document.querySelector("#expenseTable tbody");

// ===== ADD EXPENSE =====
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const description = document.getElementById("description").value.trim();
  const amount = Number(document.getElementById("amount").value);

  if (!description || !amount) {
    alert("Please enter valid expense details.");
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/expense/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id, month, description, amount })
    });

    const data = await response.json();

    if (!data.id) {
      console.error("Backend response missing ID:", data);
      alert("Failed to add expense. Please try again.");
      return;
    }

    addRowToTable({
      id: data.id,
      description,
      amount,
      ai_category: data.ai_category,
      percentage: income
        ? ((amount / income) * 100).toFixed(2)
        : "-"
    });

    form.reset();
  } catch (err) {
    console.error(err);
    alert("Failed to add expense.");
  }
});

// ===== TABLE ROW =====
function addRowToTable(exp) {
  const row = document.createElement("tr");
  row.setAttribute("data-id", exp.id);

  row.innerHTML = `
    <td>${exp.description}</td>
    <td>₹${exp.amount}</td>
    <td>${exp.ai_category}</td>
    <td>${exp.percentage}%</td>
    <td>
      <button onclick="editExpense('${exp.id}')">✏️</button>
      <button onclick="deleteExpense('${exp.id}')">🗑️</button>
    </td>
  `;

  tableBody.appendChild(row);
}

// ===== EDIT EXPENSE =====
async function editExpense(id) {
  if (!id) {
    alert("Invalid expense ID.");
    return;
  }

  const row = document.querySelector(`tr[data-id="${id}"]`);
  if (!row) return;

  const currentDesc = row.children[0].innerText;
  const currentAmt = row.children[1].innerText.replace("₹", "");

  const newDesc = prompt("Edit description:", currentDesc);
  const newAmt = prompt("Edit amount:", currentAmt);

  if (!newDesc || !newAmt) return;

  try {
    const response = await fetch(`${API_BASE_URL}/expense/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        description: newDesc,
        amount: Number(newAmt)
      })
    });

    const data = await response.json();

    // Update UI with new values + AI category
    row.children[0].innerText = newDesc;
    row.children[1].innerText = `₹${newAmt}`;
    row.children[2].innerText = data.ai_category;
    row.children[3].innerText =
      income ? ((newAmt / income) * 100).toFixed(2) + "%" : "-";

  } catch (err) {
    console.error(err);
    alert("Failed to update expense.");
  }
}

// ===== DELETE EXPENSE =====
async function deleteExpense(id) {
  if (!id) {
    alert("Invalid expense ID.");
    return;
  }

  if (!confirm("Are you sure you want to remove this expense?")) return;

  try {
    await fetch(`${API_BASE_URL}/expense/${id}`, {
      method: "DELETE"
    });

    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (row) row.remove();

  } catch (err) {
    console.error(err);
    alert("Failed to delete expense.");
  }
}

// ===== ANALYZE =====
document.getElementById("analyzeBtn").addEventListener("click", () => {
  window.location.href = "summary.html";
});
