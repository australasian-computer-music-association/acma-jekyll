---
layout: null
sitemap: false
---
// The old Alembic theme registered a caching service worker at /sw.js.
// This replacement clears its caches and unregisters itself so returning
// visitors don't get stale pages. Safe to delete once old workers have expired.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    for (const key of await caches.keys()) await caches.delete(key);
    await self.registration.unregister();
    for (const client of await self.clients.matchAll({ type: 'window' })) client.navigate(client.url);
  })());
});
