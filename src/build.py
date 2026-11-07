"""Build the GitHub Pages site (repo root) from src/.
   python3 src/build.py          -> runs overrides.py, then writes index.html, sw.js, manifest, splash screens."""
import json,os,hashlib,subprocess,sys,shutil
SRC=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.dirname(SRC)
URL='https://mkeegan-stack.github.io/gtg-advisor/'
BG='#1a2558';BAR='#18214f'
subprocess.run([sys.executable,os.path.join(SRC,'overrides.py')],check=True,stdout=subprocess.DEVNULL)
data=json.dumps(json.load(open(os.path.join(SRC,'data/game-data.json'))),separators=(',',':'),ensure_ascii=False).replace('</','<\\/')
s=open(os.path.join(SRC,'app.src.html')).read().replace('/*__DATA__*/',data)

# local fonts instead of Google Fonts (works offline, no third-party requests)
GF='''<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Saira+Condensed:wght@600;700;800&family=Rubik:wght@400;500;700&display=swap" rel="stylesheet">'''
assert GF in s
fonts='<style>'+''.join(f"@font-face{{font-family:'Saira Condensed';font-weight:{w};font-display:swap;src:url(fonts/saira-condensed-{w}.woff2) format('woff2')}}" for w in (600,700,800))+"@font-face{font-family:'Rubik';font-weight:300 900;font-display:swap;src:url(fonts/rubik.woff2) format('woff2')}</style>"
fonts+='<link rel="preload" href="fonts/saira-condensed-800.woff2" as="font" type="font/woff2" crossorigin>'

# iPhone launch screens: plain background colour (the startup animation starts from the same colour)
SPL=[(440,956,3),(430,932,3),(428,926,3),(420,912,3),(414,896,3),(414,896,2),(414,736,3),(402,874,3),(393,852,3),(390,844,3),(375,812,3),(375,667,2),(360,780,3),(320,568,2)]
os.makedirs(os.path.join(ROOT,'splash'),exist_ok=True)
try:
    from PIL import Image
    for w,h,r in SPL:
        p=os.path.join(ROOT,'splash',f'{w}x{h}@{r}.png')
        if not os.path.exists(p):Image.new('RGB',(w*r,h*r),BG).save(p,optimize=True)
except ImportError: print('Pillow missing: splash screens not regenerated')
splash=''.join(f'<link rel="apple-touch-startup-image" href="splash/{w}x{h}@{r}.png" media="(device-width: {w}px) and (device-height: {h}px) and (-webkit-device-pixel-ratio: {r}) and (orientation: portrait)">' for w,h,r in SPL)

head=f'''<meta name="description" content="Teams, GDA ops, artifacts and next moves for Invincible: Guarding the Globe, worked out from your own roster.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/favicon.svg" type="image/svg+xml"><link rel="icon" href="icons/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"><meta name="apple-mobile-web-app-title" content="GTG Advisor">
<meta property="og:type" content="website"><meta property="og:title" content="GTG Advisor"><meta property="og:description" content="Teams, GDA ops, artifacts and next moves for Invincible: Guarding the Globe.">
<meta property="og:url" content="{URL}"><meta property="og:image" content="{URL}og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{URL}og.png">
{splash}
<script>window.APP_STANDALONE=true;</script>
{fonts}'''
s=s.replace(GF,head)
s=s.replace('<body>\n','<body>\n'+open(os.path.join(SRC,'boot.html')).read()+'\n',1)
s=s.replace('</body>','<script src="vendor/qrcode.js"></script>\n<script src="standalone.js"></script>\n</body>')
assert s.count('name="theme-color"')==1
open(os.path.join(ROOT,'index.html'),'w').write(s)
shutil.copy(os.path.join(SRC,'standalone.js'),os.path.join(ROOT,'standalone.js'))

json.dump({"name":"GTG Advisor","short_name":"GTG Advisor","description":"Teams, GDA ops, artifacts and next moves for Invincible: Guarding the Globe.",
  "start_url":"./","scope":"./","display":"standalone","orientation":"portrait","background_color":BG,"theme_color":BAR,
  "icons":[{"src":"icons/icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},{"src":"icons/icon-512.png","sizes":"512x512","type":"image/png","purpose":"any"},
           {"src":"icons/maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]},open(os.path.join(ROOT,'manifest.webmanifest'),'w'),indent=1)

core=['./','index.html','manifest.webmanifest','standalone.js','vendor/qrcode.js','icons/icon-192.png','icons/icon-512.png','icons/apple-touch-icon.png','icons/favicon.svg','icons/favicon-32.png']+[f'fonts/{f}' for f in sorted(os.listdir(os.path.join(ROOT,'fonts'))) if f.endswith('.woff2')]
h=hashlib.sha256()
for f in core[1:]:h.update(open(os.path.join(ROOT,f),'rb').read())
ver=h.hexdigest()[:12]
sw=f'''/* GTG Advisor service worker - cache version {ver} (changes with every build) */
const CACHE='gtg-{ver}';const CORE={json.dumps(core)};
self.addEventListener('install',e=>{{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()));}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));}});
self.addEventListener('fetch',e=>{{const r=e.request;if(r.method!=='GET'||new URL(r.url).origin!==location.origin)return;
  if(r.mode==='navigate'){{e.respondWith(fetch(r.url,{{cache:'no-cache'}}).then(res=>{{const cp=res.clone();caches.open(CACHE).then(c=>c.put('index.html',cp));return res;}}).catch(()=>caches.match('index.html')));return;}}
  e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{{if(res.ok){{const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp));}}return res;}})));}});
'''
open(os.path.join(ROOT,'sw.js'),'w').write(sw)
open(os.path.join(ROOT,'.nojekyll'),'w').write('')
print('built',len(s),'bytes; cache',ver)
