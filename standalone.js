/* Home Screen app layer: service worker, install guide, Android install + back button, sharing. Only in the GitHub Pages build. */
(function(){
"use strict";
var isStandalone=window.navigator.standalone===true||(window.matchMedia&&matchMedia('(display-mode: standalone)').matches);
var LS_KEY='gtg-advisor-state',BROWSER_KEY='gtg-use-browser';
try{if(navigator.storage&&navigator.storage.persist)navigator.storage.persist();}catch(e){}
if('serviceWorker' in navigator&&(location.protocol==='https:'||location.hostname==='localhost')){window.addEventListener('load',function(){navigator.serviceWorker.register('sw.js').catch(function(){});});}

/* share + QR (More -> About) */
window.gtgShare=function(){var url=location.origin+location.pathname;if(navigator.share){navigator.share({title:'GTG Advisor',text:'Teams, ops, artifacts and next moves for Invincible: Guarding the Globe',url:url}).catch(function(){});}
  else if(navigator.clipboard){navigator.clipboard.writeText(url).then(function(){typeof toast==='function'&&toast('Link copied');});}};
window.gtgAfterRender=function(){var el=document.getElementById('gtgQr');if(el&&window.qrcode&&!el.firstChild){var q=qrcode(0,'M');q.addData(location.origin+location.pathname);q.make();el.innerHTML=q.createSvgTag({cellSize:3,margin:0});}};

/* Android: install button + back button closes panels instead of quitting */
var deferred=null;
window.addEventListener('beforeinstallprompt',function(e){e.preventDefault();deferred=e;var b=document.getElementById('gtgInstallBtn');if(b)b.style.display='';});
window.gtgInstall=function(){if(!deferred)return;deferred.prompt();deferred.userChoice.finally(function(){deferred=null;});};
var isIOS=/iPad|iPhone|iPod/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
if(isStandalone&&!isIOS){history.pushState({gtg:1},'');window.addEventListener('popstate',function(){
  var sh=document.getElementById('sheet');if(sh&&sh.classList.contains('open')&&typeof closeSheet==='function'){closeSheet();}
  else if(typeof tab!=='undefined'&&tab!=='home'&&typeof setTab==='function'){setTab('home');}
  history.pushState({gtg:1},'');});}

/* install guide: first visit in a browser with nothing saved here */
var hasData=false;try{hasData=!!localStorage.getItem(LS_KEY);}catch(e){}
var useBrowser=false;try{useBrowser=localStorage.getItem(BROWSER_KEY)==='1';}catch(e){}
if(isStandalone||hasData||useBrowser)return;
var ua=navigator.userAgent;var inApp=/FBAN|FBAV|Instagram|Line\/|Twitter|Snapchat|TikTok|GSA\//.test(ua);
var android=/Android/.test(ua),samsung=/SamsungBrowser/.test(ua),firefox=/Firefox|FxiOS/.test(ua),safariIOS=isIOS&&/Safari/.test(ua)&&!/CriOS|FxiOS|EdgiOS|OPiOS/.test(ua);
var desktop=!isIOS&&!android;
var steps;
if(inApp)steps=['This page is open inside another app. Open it in '+(isIOS?'Safari':'Chrome')+' first (use the ⋯ or share menu and choose "Open in browser").','Then follow the steps there to add it to your Home Screen.'];
else if(safariIOS)steps=['Tap <b>⋯</b> at the bottom of Safari, then <b>Share</b>.','Choose <b>Add to Home Screen</b>.','Keep <b>Open as Web App</b> switched on and tap <b>Add</b>.','Open it from your Home Screen.'];
else if(isIOS)steps=['Tap the <b>Share</b> button in the address bar.','Choose <b>Add to Home Screen</b>, then <b>Add</b>.','Open it from your Home Screen.'];
else if(samsung)steps=['Tap <b>☰</b>, then <b>Add page to</b> → <b>Home screen</b>.','Open it from your Home Screen.'];
else if(firefox)steps=['Tap <b>⋮</b>, then <b>Install</b>.','Open it from your Home Screen.'];
else if(android)steps=['Tap <b>Install</b> below, or <b>⋮</b> → <b>Add to Home screen</b>.','Open it from your Home Screen.'];
else steps=['Scan the code with your phone\'s camera to open this page there.','Follow the steps it shows to add it to your Home Screen.'];
var css='#gtgInst{position:fixed;inset:0;z-index:9000;background:linear-gradient(180deg,#1a2558,#21388f);color:#fff;overflow:auto;padding:calc(28px + env(safe-area-inset-top)) 22px 30px;font-family:Rubik,system-ui,sans-serif}'+
'#gtgInst h1{font-family:"Saira Condensed",sans-serif;font-weight:800;font-size:40px;line-height:1;margin:14px 0 4px}#gtgInst .k{color:#a9c1ff;font-size:13px;letter-spacing:2px;text-transform:uppercase}'+
'#gtgInst ol{padding:0;margin:22px 0;list-style:none;counter-reset:s}#gtgInst li{counter-increment:s;background:#2443a6;border:1px solid #4d79e6;padding:12px 12px 12px 52px;margin-bottom:8px;position:relative;font-size:16px;line-height:1.35}'+
'#gtgInst li:before{content:counter(s);position:absolute;left:12px;top:10px;width:28px;height:28px;background:#ffd21f;color:#18214f;font-weight:800;display:flex;align-items:center;justify-content:center;font-family:"Saira Condensed",sans-serif;font-size:18px}'+
'#gtgInst .b{display:block;width:100%;padding:14px;font-size:17px;font-weight:700;border:0;margin-top:8px;font-family:inherit}#gtgInst .g{background:#2fe08a;color:#0f2a1c}#gtgInst .l{background:transparent;color:#dbe6ff;text-decoration:underline;font-weight:500}'+
'#gtgInst .qr{background:#fff;padding:10px;display:inline-block;line-height:0;margin-top:6px}';
var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
var d=document.createElement('div');d.id='gtgInst';
d.innerHTML='<img src="icons/icon-192.png" width="72" height="72" alt=""><div class="k" style="margin-top:14px">Invincible: Guarding the Globe</div><h1>GTG ADVISOR</h1><div style="color:#dbe6ff">Add it to your Home Screen: it opens full screen, works offline and keeps your data on your phone.</div>'+
  '<ol>'+steps.map(function(x){return '<li>'+x+'</li>';}).join('')+'</ol>'+
  (desktop?'<div class="qr" id="gtgInstQr"></div>':'')+
  '<button class="b g" id="gtgInstallBtn" style="display:none" onclick="gtgInstall()">Install</button>'+
  '<button class="b l" id="gtgUseBrowser">Use it in this browser instead</button>';
document.body.appendChild(d);
if(deferred){document.getElementById('gtgInstallBtn').style.display='';}
if(desktop&&window.qrcode){var q=qrcode(0,'M');q.addData(location.href.split('#')[0]);q.make();document.getElementById('gtgInstQr').innerHTML=q.createSvgTag({cellSize:5,margin:0});}
document.getElementById('gtgUseBrowser').onclick=function(){try{localStorage.setItem(BROWSER_KEY,'1');}catch(e){}d.remove();st.remove();};
})();
