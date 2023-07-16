var staticCacheName = 'djangopwa-v1';

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(staticCacheName).then(function(cache) {
      return cache.addAll([
        '/offline'
      ]);
    })
  );
});

self.addEventListener('fetch', function(event) {
  var requestUrl = new URL(event.request.url);
    if (requestUrl.origin === location.origin) {
      if ((requestUrl.pathname === '/')) {
        event.respondWith(caches.match('/base_layout'));
        return;
      }
    }
    event.respondWith(
      caches.match(event.request).then(function(response) {
        return response || fetch(event.request);
      })
    );
});

// Register event listener for the 'push' event.
self.addEventListener('push', function (event) {
  // Retrieve the textual payload from event.data (a PushMessageData object).
  // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
  // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.
  const eventInfo = event.data.text();
  const data = JSON.parse(eventInfo);
  const head = data.head || 'New Notification 🕺🕺';
  const body = data.body || 'This is default content. Your notification didn\'t have one 🙄🙄';

  // Keep the service worker alive until the notification is created.
  event.waitUntil(
      self.registration.showNotification(head, {
          body: body,
          icon: 'https://i.imgur.com/MZM3K5w.png'
      })
  );
});