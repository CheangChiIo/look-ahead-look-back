"use strict";

const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
const overview = [...document.querySelectorAll(".overview-video")];
const reelToggle = document.getElementById("reel-toggle");
let reelPaused = reducedMotion.matches;
const visibleOverview = new Set();
document.getElementById("overview-robot").playbackRate = 2;

function updateReelButton() {
  reelToggle.textContent = reelPaused ? "Play ▶" : "Pause Ⅱ";
  reelToggle.setAttribute("aria-label", reelPaused ? "Play overview videos" : "Pause overview videos");
}
function syncReelPlayback() {
  overview.forEach(video => {
    if (!reelPaused && !document.hidden && visibleOverview.has(video)) video.play().catch(() => {});
    else video.pause();
  });
  updateReelButton();
}
function loadVideos(container) {
  container.querySelectorAll("video[data-src]").forEach(video => {
    if (!video.getAttribute("src")) {
      video.src = video.dataset.src;
      video.preload = "metadata";
      video.load();
    }
  });
}
reelToggle.addEventListener("click", () => {
  reelPaused = !reelPaused;
  syncReelPlayback();
});
updateReelButton();

document.querySelectorAll("[data-tabs]").forEach(list => {
  const tabs = [...list.querySelectorAll('[role="tab"]')];
  function activate(selected, focus = false) {
    tabs.forEach(tab => {
      const active = tab === selected;
      const panel = document.getElementById(tab.getAttribute("aria-controls"));
      tab.setAttribute("aria-selected", String(active));
      tab.tabIndex = active ? 0 : -1;
      panel.hidden = !active;
      if (!active) panel.querySelectorAll("video").forEach(video => video.pause());
      if (active) loadVideos(panel);
    });
    if (focus) selected.focus();
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => activate(tab));
    tab.addEventListener("keydown", event => {
      let next;
      if (event.key === "ArrowRight") next = (index + 1) % tabs.length;
      if (event.key === "ArrowLeft") next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === "Home") next = 0;
      if (event.key === "End") next = tabs.length - 1;
      if (next !== undefined) {
        event.preventDefault();
        activate(tabs[next], true);
      }
    });
  });
});
document.querySelectorAll("details").forEach(details => details.addEventListener("toggle", () => {
  if (details.open) loadVideos(details);
  else details.querySelectorAll("video").forEach(video => video.pause());
}));

const mediaObserver = new IntersectionObserver(entries => {
  entries.forEach(({target, isIntersecting}) => {
    if (isIntersecting) {
      if (target.dataset.src && !target.getAttribute("src")) {
        target.src = target.dataset.src;
        target.preload = "metadata";
        target.load();
      }
    }
    if (target.classList.contains("overview-video")) {
      if (isIntersecting) visibleOverview.add(target);
      else visibleOverview.delete(target);
    } else if (!isIntersecting) target.pause();
  });
  syncReelPlayback();
}, {threshold: .15});
document.querySelectorAll("video").forEach(video => mediaObserver.observe(video));
document.addEventListener("visibilitychange", () => {
  if (document.hidden) document.querySelectorAll("video").forEach(video => video.pause());
  else syncReelPlayback();
});
reducedMotion.addEventListener("change", event => {
  if (event.matches) {
    reelPaused = true;
    overview.forEach(video => video.pause());
    updateReelButton();
  }
});

const imageDialog = document.getElementById("image-dialog");
const enlargedImage = document.getElementById("dialog-image");
document.querySelectorAll("[data-zoom]").forEach(button => button.addEventListener("click", () => {
  enlargedImage.src = button.dataset.zoom;
  enlargedImage.alt = button.querySelector("img")?.alt || "Research figure";
  document.getElementById("dialog-caption").textContent = button.dataset.caption || enlargedImage.alt;
  imageDialog.showModal();
}));
document.getElementById("close-image").addEventListener("click", () => imageDialog.close());
imageDialog.addEventListener("click", event => {
  if (event.target === imageDialog) {
    const box = imageDialog.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) imageDialog.close();
  }
});

function makeTable(caption, columns, names, rows) {
  const table = document.createElement("table");
  const title = document.createElement("caption");
  title.textContent = caption;
  table.append(title);
  const thead = table.createTHead();
  const header = thead.insertRow();
  ["Method", ...columns].forEach(label => {
    const th = document.createElement("th");
    th.scope = "col";
    th.textContent = label;
    header.append(th);
  });
  const tbody = table.createTBody();
  names.forEach((name, index) => {
    const tr = tbody.insertRow();
    if (name === "Ours") tr.className = "ours-row";
    const th = document.createElement("th");
    th.scope = "row";
    th.textContent = name;
    tr.append(th);
    rows[index].forEach(value => {
      const td = tr.insertCell();
      td.textContent = Number(value).toFixed(1);
    });
  });
  return table;
}
fetch("results.json").then(response => {
  if (!response.ok) throw new Error("Result data request failed");
  return response.json();
}).then(data => {
  Object.entries(data.benchmarks).forEach(([key, benchmark]) => {
    document.querySelector(`[data-result-table="${key}"]`).append(makeTable(benchmark.name + " · task success (%)", benchmark.columns, data.methods, benchmark.rows));
    document.querySelector(`[data-protocol="${key}"]`).textContent = benchmark.protocol;
  });
  document.getElementById("ablation-table").append(makeTable("LIBERO-Long · complete-task success (%)", ["Task 4", "Task 7", "Task 8", "Average"], data.ablations.variants, data.ablations.per_task.map((row,i) => [...row,data.ablations.success[i]])));
  document.getElementById("stage-table").append(makeTable("Independent stage continuation success (%)", data.stages.names, ["Without preplay", "Ours"], [data.stages.without_preplay,data.stages.ours]));
}).catch(() => {
  document.querySelectorAll("[data-result-table], #ablation-table, #stage-table").forEach(container => {
    const link = document.createElement("a");
    link.href = "results.json";
    link.textContent = "Open the reported result data";
    container.append(link);
  });
});

document.getElementById("copy-citation").addEventListener("click", async () => {
  const text = document.getElementById("citation-text").textContent;
  const status = document.getElementById("copy-status");
  try {
    await navigator.clipboard.writeText(text);
    status.textContent = "BibTeX copied.";
  } catch {
    const range = document.createRange();
    range.selectNodeContents(document.getElementById("citation-text"));
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    status.textContent = "Citation selected. Use your browser's copy command.";
  }
});
