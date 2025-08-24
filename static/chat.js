const socket = io();

let lastSeen = 0;
let firstNewId = null;
let unseenCount = 0;

function el(tag, cls, html) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html !== undefined) e.innerHTML = html;
  return e;
}

function fmtMsg(m) {
  if (m.type === "system") {
    return `<span class="sys">[${m.time}] ${m.text}</span>`;
  }
  return `<span class="time">[${m.time}]</span> <b>${m.user}</b>: ${escapeHtml(m.text)}`;
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, ch => ({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
  }[ch]));
}

function scrollToBottom() {
  const chat = document.getElementById("chat");
  chat.scrollTop = chat.scrollHeight;
}

socket.on("connect", () => {
  socket.emit("chat:join", { room: window.DAV.room });
});

socket.on("room:count", (data) => {
  const elc = document.getElementById("roomcount");
  if (elc) elc.innerText = data.count;
});

socket.on("chat:history", (payload) => {
  const { items, last_seen_id } = payload;
  lastSeen = last_seen_id || 0;

  const chat = document.getElementById("chat");
  chat.innerHTML = "";

  let firstNewFound = false;
  for (const m of items) {
    const p = el("div", "msg " + (m.type==="system"?"sys":""));
    p.innerHTML = fmtMsg(m);
    p.id = "m" + m.id;
    chat.appendChild(p);

    if (m.id > lastSeen && !firstNewFound) {
      firstNewId = m.id;
      firstNewFound = true;
    }
  }

  unseenCount = items.filter(m => m.id > lastSeen).length;
  if (unseenCount > 0) {
    document.getElementById("newCount").innerText = `(${unseenCount})`;
    document.getElementById("jumpNew").style.display = "block";
  } else {
    document.getElementById("jumpNew").style.display = "none";
  }
  scrollToBottom();
});

socket.on("chat:new_message", (m) => {
  const chat = document.getElementById("chat");
  const p = el("div", "msg " + (m.type==="system"?"sys":""));
  p.innerHTML = fmtMsg(m);
  p.id = "m" + m.id;
  chat.appendChild(p);

  if (m.id > lastSeen && firstNewId === null) {
    firstNewId = m.id;
  }
  if (m.id > lastSeen) {
    unseenCount++;
    document.getElementById("newCount").innerText = `(${unseenCount})`;
    document.getElementById("jumpNew").style.display = "block";
  }
  scrollToBottom();
});

function jumpToNew() {
  if (!firstNewId) return;
  const elNew = document.getElementById("m" + firstNewId);
  if (elNew) elNew.scrollIntoView({ behavior: "smooth", block: "center" });
  // прочитано до низа:
  const all = document.querySelectorAll(".msg");
  if (all.length) {
    const last = all[all.length-1].id.replace("m","");
    lastSeen = parseInt(last, 10);
    socket.emit("chat:mark_seen", { last_id: lastSeen });
  }
  unseenCount = 0;
  firstNewId = null;
  document.getElementById("jumpNew").style.display = "none";
}

function sendMsg() {
  const inp = document.getElementById("text");
  const t = (inp.value || "").trim();
  if (!t) return;
  socket.emit("chat:send", { text: t });
  inp.value = "";
}
