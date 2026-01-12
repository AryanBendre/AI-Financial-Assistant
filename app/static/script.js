const API_BASE_URL = ""; // Relative path for Render

document.getElementById("profileForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const name = document.getElementById("name").value.trim();
  const age = Number(document.getElementById("age").value);
  const income = Number(document.getElementById("income").value);

  if (!name || !age || !income) {
    alert("Please fill all fields correctly.");
    return;
  }

  try {
    // 1️⃣ Create user (FIXED: Added slash at the end)
    const userRes = await fetch("/user/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, age })
    });

    if (!userRes.ok) {
      const errorData = await userRes.json();
      console.error("User Error:", errorData);
      alert("Server Error: " + (errorData.detail || "Failed to create user"));
      return;
    }

    const userData = await userRes.json();
    const userId = userData.id || userData.user_id;

    if (!userId) {
      alert("Failed to create user. Please try again.");
      return;
    }

    // 2️⃣ Save session data
    localStorage.setItem("user_id", userId);
    localStorage.setItem("income", income);

    // 3️⃣ Save monthly income (FIXED: Added slash at the end)
    const month = new Date().toISOString().slice(0, 7);

    const incomeRes = await fetch("/income/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        month,
        income
      })
    });

    if (!incomeRes.ok) {
        console.error("Income Error");
        // We continue anyway since user is created
    }

    // 4️⃣ Navigate AFTER everything succeeds
    window.location.href = "expenses.html";

  } catch (error) {
    console.error("Onboarding error:", error);
    alert("Something went wrong. Check console for details.");
  }
});
