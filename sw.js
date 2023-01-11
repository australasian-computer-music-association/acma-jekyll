const version = '20230111035114';
const cacheName = `static::${version}`;

const buildContentBlob = () => {
  return ["/news/2022/10/24/acmc-2022-wrap-up.html","/news/2021/08/30/call-for-contributions-to-chroma.html","/news/2021/04/23/acmc21.html","/news/2019/12/31/acmc-2019-proceedings-available.html","/news/2019/12/17/acmc-2020-inclusion.html","/news/2018/11/29/acmc-2019.html","/news/2018/04/11/acmc-2018.html","/news/2017/09/30/acmc-2017-adelaide.html","/news/2015/10/13/acmc-2015.html","/news/2014/04/18/extension-for-acmc-2014-submissions.html","/about/","/acma-list/","/chroma-archive.html","/code-of-conduct.html","/committee.html","/competitions.html","/conference/","/duties.html","/hosting-acmc.html","/news/","/","/links.html","/membership.html","/search.html","/manifest.json","/assets/search.json","/assets/styles.css","/redirects.json","/feed.xml","/sitemap.xml","/robots.txt","/assets/logos/acma-logo-square-black.svg", "/assets/default-offline-image.png", "/assets/scripts/fetch.js"
  ]
}

const updateStaticCache = () => {
  return caches.open(cacheName).then(cache => {
    return cache.addAll(buildContentBlob());
  });
};

const clearOldCache = () => {
  return caches.keys().then(keys => {
    // Remove caches whose name is no longer valid.
    return Promise.all(
      keys
        .filter(key => {
          return key !== cacheName;
        })
        .map(key => {
          console.log(`Service Worker: removing cache ${key}`);
          return caches.delete(key);
        })
    );
  });
};

self.addEventListener("install", event => {
  event.waitUntil(
    updateStaticCache().then(() => {
      console.log(`Service Worker: cache updated to version: ${cacheName}`);
    })
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(clearOldCache());
});

self.addEventListener("fetch", event => {
  let request = event.request;
  let url = new URL(request.url);

  // Only deal with requests from the same domain.
  if (url.origin !== location.origin) {
    return;
  }

  // Always fetch non-GET requests from the network.
  if (request.method !== "GET") {
    event.respondWith(fetch(request));
    return;
  }

  // Default url returned if page isn't cached
  let offlineAsset = "/offline/";

  if (request.url.match(/\.(jpe?g|png|gif|svg)$/)) {
    // If url requested is an image and isn't cached, return default offline image
    offlineAsset = "/assets/default-offline-image.png";
  }

  // For all urls request image from network, then fallback to cache, then fallback to offline page
  event.respondWith(
    fetch(request).catch(async () => {
      return (await caches.match(request)) || caches.match(offlineAsset);
    })
  );
  return;
});
