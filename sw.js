/* DJ Map : fonctionnement hors connexion.
   - events.json : réseau d'abord (dates fraîches), sinon la dernière copie.
   - page et images : copie locale tout de suite, mise à jour en arrière-plan. */
const V = "djmap-v3";
const CORE = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "satellite.jpg", "events.json"];
self.addEventListener("install", e => {
  e.waitUntil(caches.open(V).then(c => Promise.all(CORE.map(u => c.add(u).catch(() => {})))).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const r = e.request;
  if (r.method !== "GET") return;
  const u = new URL(r.url);
  if (u.origin !== location.origin) return;   // comptes et favoris : jamais mis en cache
  if (/events\.json$/.test(u.pathname)) {
    e.respondWith(fetch(r, { cache: "no-store" }).then(res => {
      const cp = res.clone(); caches.open(V).then(c => c.put(r, cp)); return res;
    }).catch(() => caches.match(r)));
    return;
  }
  e.respondWith(caches.match(r, { ignoreSearch: true }).then(hit => {
    const net = fetch(r).then(res => {
      if (res && (res.ok || res.type === "opaque")) { const cp = res.clone(); caches.open(V).then(c => c.put(r, cp)); }
      return res;
    }).catch(() => hit);
    return hit || net;
  }));
});
self.addEventListener("notificationclick", e => {
  e.notification.close();
  e.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(ws => {
    for (const w of ws) { if ("focus" in w) return w.focus(); }
    return self.clients.openWindow("./");
  }));
});
