const form = document.getElementById("comic-form");
const charactersBox = document.getElementById("characters");
const addCharBtn = document.getElementById("add-character");
const generateBtn = document.getElementById("generate-btn");
const downloadBtn = document.getElementById("download-btn");
const progressBox = document.getElementById("progress");
const progressFill = document.getElementById("progress-fill");
const progressText = document.getElementById("progress-text");
const errorBox = document.getElementById("error-box");
const okBox = document.getElementById("ok-box");
const grid = document.getElementById("comic-grid");
const comicHeader = document.getElementById("comic-header");
const comicTitle = document.getElementById("comic-title");
const comicLogline = document.getElementById("comic-logline");
const panelCount = document.getElementById("panel-count");
const panelCountVal = document.getElementById("panel-count-val");

let currentComic = null;

function addCharacterRow(name = "", description = "") {
  const row = document.createElement("div");
  row.className = "char-row";
  row.innerHTML = `
    <input type="text" class="char-name" placeholder="Name" maxlength="60" value="${escapeAttr(name)}" />
    <input type="text" class="char-desc" placeholder="Appearance / personality" maxlength="400" value="${escapeAttr(description)}" />
    <button type="button" class="char-remove" title="Remove">×</button>`;
  row.querySelector(".char-remove").addEventListener("click", () => row.remove());
  charactersBox.appendChild(row);
}

function escapeAttr(v) {
  return String(v).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
}
function escapeHtml(v) {
  return String(v).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function setProgress(pct, text) {
  progressFill.style.width = `${pct}%`;
  if (text) progressText.textContent = text;
}

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.classList.remove("hidden");
}
function clearMessages() {
  errorBox.classList.add("hidden");
  okBox.classList.add("hidden");
}
function setBusy(busy) {
  generateBtn.disabled = busy;
  generateBtn.textContent = busy ? "Generating…" : "⚡ Generate Comic";
}

async function apiPost(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const data = await res.json();
      if (data.detail) detail = typeof data.detail === "string" ? data.detail : JSON.stringify(data.detail);
    } catch (_) {}
    throw new Error(detail);
  }
  return res.json();
}

function collectRequest() {
  const characters = [...charactersBox.querySelectorAll(".char-row")]
    .map((row) => ({
      name: row.querySelector(".char-name").value.trim(),
      description: row.querySelector(".char-desc").value.trim(),
    }))
    .filter((c) => c.name.length > 0);

  return {
    idea: document.getElementById("idea").value.trim(),
    characters,
    setting: document.getElementById("setting").value.trim(),
    tone: document.getElementById("tone").value,
    art_style: document.getElementById("art-style").value,
    panel_count: parseInt(panelCount.value, 10),
  };
}

function renderPanels(comic) {
  comicHeader.classList.remove("hidden");
  comicTitle.textContent = comic.title;
  comicLogline.textContent = comic.logline || "";
  grid.innerHTML = "";

  comic.panels.forEach((panel) => {
    const el = document.createElement("div");
    el.className = "panel";
    el.id = `panel-${panel.id}`;
    const dialogues = (panel.dialogues || [])
      .map((d) => `<div class="bubble"><strong>${escapeHtml(d.speaker)}:</strong> ${escapeHtml(d.line)}</div>`)
      .join("");
    el.innerHTML = `
      <div class="art">
        <span class="num">PANEL ${panel.id}</span>
        <div class="spin"></div>
        <span class="pend">drawing…</span>
      </div>
      <div class="caption">${escapeHtml(panel.narration || panel.scene || "")}</div>
      <div class="body">
        ${dialogues}
        <div class="scene">${escapeHtml(panel.scene || "")}</div>
      </div>`;
    grid.appendChild(el);
  });
}

function setPanelImage(panel, url) {
  const el = document.getElementById(`panel-${panel.id}`);
  if (!el) return;
  const art = el.querySelector(".art");
  art.innerHTML = `<span class="num">PANEL ${panel.id}</span><img src="${url}?t=${Date.now()}" alt="Panel ${panel.id}" />`;
}

async function generateImages(comic, req) {
  const total = comic.panels.length;
  let failed = 0;
  for (let i = 0; i < total; i++) {
    const panel = comic.panels[i];
    setProgress(30 + Math.round(((i) / total) * 65), `Drawing panel ${i + 1} of ${total}…`);
    try {
      const resp = await apiPost("/api/generate-image", {
        panel_id: panel.id,
        image_prompt: panel.image_prompt || panel.scene,
        art_style: req.art_style,
        characters: req.characters,
        tone: req.tone,
      });
      panel.image_url = resp.image_url;
      setPanelImage(panel, resp.image_url);
      if (!resp.ok) failed++;
    } catch (err) {
      failed++;
      const el = document.getElementById(`panel-${panel.id}`);
      if (el) {
        const art = el.querySelector(".art");
        art.innerHTML = `<span class="num">PANEL ${panel.id}</span><span style="color:#b00;font-size:.8rem;padding:1rem;text-align:center">Image failed: ${escapeHtml(err.message)}</span>`;
      }
    }
  }
  return failed;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearMessages();
  const req = collectRequest();
  if (req.idea.length < 5) {
    showError("Please enter a story idea (at least 5 characters).");
    return;
  }

  setBusy(true);
  downloadBtn.classList.add("hidden");
  progressBox.classList.remove("hidden");
  currentComic = null;

  try {
    setProgress(10, "Writing outline with Gemini 2.5 Flash…");
    const comic = await apiPost("/api/generate-story", req);
    currentComic = comic;
    renderPanels(comic);
    setProgress(30, "Story ready. Generating illustrations…");

    const failed = await generateImages(comic, req);
    setProgress(100, failed ? `Done with ${failed} image issue(s).` : "Comic complete!");
    downloadBtn.classList.remove("hidden");

    if (failed) {
      showError("Story generated, but some images could not be drawn (model busy or quota). You can still download the PDF or try again.");
    } else {
      okBox.textContent = `“${comic.title}” ready — ${comic.panels.length} panels generated.`;
      okBox.classList.remove("hidden");
    }
  } catch (err) {
    showError(err.message);
    setProgress(0, "Failed.");
  } finally {
    setBusy(false);
    setTimeout(() => progressBox.classList.add("hidden"), 2500);
  }
});

downloadBtn.addEventListener("click", async () => {
  if (!currentComic) return;
  clearMessages();
  downloadBtn.disabled = true;
  try {
    const res = await fetch("/api/export-pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(currentComic),
    });
    if (!res.ok) throw new Error(`PDF export failed (${res.status})`);
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${(currentComic.title || "comic").replace(/[^A-Za-z0-9]+/g, "-").toLowerCase()}.pdf`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  } catch (err) {
    showError(err.message);
  } finally {
    downloadBtn.disabled = false;
  }
});

addCharBtn.addEventListener("click", () => addCharacterRow());
panelCount.addEventListener("input", () => {
  panelCountVal.textContent = panelCount.value;
});

async function loadHealth() {
  try {
    const res = await fetch("/api/health");
    const data = await res.json();
    document.getElementById("dot-google").className = `dot ${data.google_key ? "on" : "off"}`;
    document.getElementById("dot-hf").className = `dot ${data.hf_key ? "on" : "na"}`;
  } catch (_) {
    document.getElementById("dot-google").className = "dot off";
    document.getElementById("dot-hf").className = "dot na";
  }
}

addCharacterRow("Nova", "A shy robot with glowing amber eyes who can grow flowers");
addCharacterRow("Mayor Vale", "Proud, skeptical leader of Neo-Garden");
loadHealth();