// Minimal Service Worker for PWA Installation
self.addEventListener('install', (e) => {
  console.log('[Service Worker] Installed');
});

self.addEventListener('fetch', (e) => {
  // Serves requests normally from the network
  e.respondWith(fetch(e.request));
});