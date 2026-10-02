document.querySelectorAll(".planner-form").forEach(form => {
  form.addEventListener("submit", async e => {
    e.preventDefault();
    const results = form.parentElement.querySelector(".results");
    results.innerHTML = "<p>Generating recommendations...</p>";
    try {
      const r = await fetch(form.dataset.endpoint, {method:"POST", body:new FormData(form)});
      const data = await r.json();
      if (!r.ok) throw new Error(data.detail || "Request failed");
      results.innerHTML = `<h3>${data.summary || "Recommendations"}</h3>` +
        (data.items || []).map(x => `
          <div class="result">
            <b>${x.name}</b>
            <div>${x.category} · ₹${Number(x.price).toLocaleString("en-IN")} · ${x.platform}</div>
            <p>${x.reason || ""}</p>
          </div>`).join("");
    } catch(err) {
      results.innerHTML = `<p>${err.message}</p>`;
    }
  });
});
