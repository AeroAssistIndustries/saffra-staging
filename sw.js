const C='saffra-v6';
const PRE=['./','index.html','manifest.webmanifest','fonts/bodoni-moda-latin-wght-normal.woff2','fonts/bodoni-moda-latin-wght-italic.woff2','fonts/dm-sans-latin-wght-normal.woff2','img/icon-180.png','img/icon-192.png','img/icon-512.png','img/bottle-her.webp','img/bottle-him.webp','img/duo.webp'];
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(C).then(c=>c.addAll(PRE)).catch(()=>{}));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET'||new URL(e.request.url).origin!==location.origin) return;
  e.respondWith(fetch(e.request).then(r=>{if(r.ok){const c=r.clone();caches.open(C).then(x=>x.put(e.request,c));}return r;}).catch(()=>caches.match(e.request,{ignoreSearch:true}).then(r=>r||caches.match('./'))));
});
