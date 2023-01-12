const version = '20230112155056';
const cacheName = `static::${version}`;

const buildContentBlob = () => {
  return ["/news/2022/10/24/acmc-2022-wrap-up/","/news/2021/08/30/call-for-contributions-to-chroma/","/news/2021/04/23/acmc21/","/news/2019/12/31/acmc-2019-proceedings-available/","/news/2019/12/17/acmc-2020-inclusion/","/news/2018/11/29/acmc-2019/","/news/2018/04/11/acmc-2018/","/news/2017/09/30/acmc-2017-adelaide/","/news/2015/10/13/acmc-2015/","/news/2014/04/18/extension-for-acmc-2014-submissions/","/about/","/acma-list/","/chroma/","/code-of-conduct/","/committee/","/competitions/","/conferences/","/duties/","/hosting-acmc/","/news/","/","/links/","/membership/","/search/","/assets/styles.css","/manifest.json","/assets/search.json","/redirects.json","/feed.xml","/sitemap.xml","/robots.txt","/assets/styles.css.map","/assets/logos/acma-logo-square-black.svg", "/assets/default-offline-image.png", "/assets/scripts/fetch.js"
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
