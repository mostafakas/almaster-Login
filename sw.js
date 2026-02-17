const CACHE_NAME = 'almaster-cache-v1';

// ملفات نريد تحميلها بسرعة (فقط الملفات الثابتة)
// ملحوظة: لا نضع روابط فايربيز هنا عشان البيانات تفضل مباشرة ومباشرة
const urlsToCache = [
  './',
  './index.html',
  '/payroll.html', // أضف هذا السطر هنا
  './manifest.json',
  './icon-192.png',
  './icon-512.png'
];

// 1. تثبيت التطبيق وتخزين الملفات الأساسية
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// 2. تفعيل التطبيق
self.addEventListener('activate', event => {
  console.log('Service Worker Activated');
});

// 3. استراتيجية الشبكة أولاً (Network First)
// بنقول للتطبيق: حاول تجيب البيانات من النت الأول (عشان فايربيز والداتا الجديدة)
// لو مفيش نت، هات من الكاش المحفوظ
self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request).catch(() => {
      return caches.match(event.request);
    })
  );

});
