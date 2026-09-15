let selectedConvId = null;

document.getElementById("file-input").addEventListener("change", async (e) => {
  if (e.target.files[0]) await uploadFile(e.target.files[0]);
});

const dz = document.getElementById("drop-zone");
dz.addEventListener("dragover", (e) => { e.preventDefault(); dz.style.borderColor = "#7c3aed"; });
dz.addEventListener("dragleave", () => { dz.style.borderColor = "#4c1d95"; });
dz.addEventListener("drop", async (e) => { e.preventDefault(); if (e.dataTransfer.files[0]) await uploadFile(e.dataTransfer.files[0]); });

async function uploadFile(file) {
  const fd = new FormData();
  fd.append("file", file);
  const r = document.getElementById("upload-result");
  r.className = "";
  r.innerHTML = "⏳ در حال آپلود...";
  try {
    const res = await fetch("/api/upload/", { method: "POST", body: fd });
    const data = await res.json();
    r.innerHTML = res.ok
      ? `✅ آپلود شد: <strong>${data.title}</strong> (${data.message_count} پیام از ${data.source})`
      : `❌ خطا: ${data.detail}`;
    if (res.ok) loadConversations();
  } catch { r.innerHTML = "❌ خطای شبکه"; }
}

async function loadConversations() {
  const list = await (await fetch("/api/upload/list")).json();
  const c = document.getElementById("conversations-list");
  if (!list.length) { c.innerHTML = '<p class="muted">هنوز مکالمه‌ای آپلود نشده</p>'; return; }
  c.innerHTML = list.map(x => `
    <div class="conversation-item" onclick="selectConv('${x.id}', this)">
      <span>${x.title || "بدون عنوان"}</span>
      <div><span class="badge">${x.source}</span><span class="badge">${x.message_count} پیام</span></div>
    </div>`).join("");
}

function selectConv(id, el) {
  document.querySelectorAll(".conversation-item").forEach(i => i.classList.remove("selected"));
  el.classList.add("selected");
  selectedConvId = id;
  document.getElementById("summarize-btn").disabled = false;
}

document.getElementById("summarize-btn").addEventListener("click", async () => {
  if (!selectedConvId) return;
  const r = document.getElementById("summary-result");
  r.className = "";
  r.innerHTML = "⏳ در حال خلاصه‌سازی...";
  try {
    const res = await fetch("/api/summarize/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        conversation_id: selectedConvId,
        model: document.getElementById("model-select").value,
        style: document.getElementById("style-select").value
      })
    });
    const data = await res.json();
    if (res.ok) {
      r.innerHTML = `
        <h3>📝 خلاصه</h3><p style="margin:.5rem 0">${data.summary}</p>
        <h3 style="margin-top:1rem">🎯 نکات کلیدی</h3>
        <ul style="margin:.5rem 0;padding-right:1.5rem">${data.key_points.map(p => `<li>${p}</li>`).join("")}</ul>
        <h3 style="margin-top:1rem">🚀 Prompt آماده</h3>
        <div class="ready-prompt" id="rp">${data.ready_prompt}</div>
        <button class="copy-btn" onclick="copyPrompt()">📋 کپی Prompt</button>`;
    } else { r.innerHTML = `❌ خطا: ${data.detail}`; }
  } catch { r.innerHTML = "❌ خطای شبکه"; }
});

function copyPrompt() {
  navigator.clipboard.writeText(document.getElementById("rp").innerText).then(() => {
    const b = document.querySelector(".copy-btn");
    b.textContent = "✅ کپی شد!";
    setTimeout(() => b.textContent = "📋 کپی Prompt", 2000);
  });
}

loadConversations();