const CACHE_NAME = 'weboffice-v5-cache';
const assetsToCache = [
  'index.html',
  'manifest.json',
  'https://awdev.my.id/assets/img/logo.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(assetsToCache);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
