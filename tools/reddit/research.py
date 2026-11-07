import json,sys,time,re,urllib.parse,os
sys.path.insert(0,'tools/reddit')
from fetch import get,parse
G=json.load(open('src/data/game-data.json'))
OUT='reddit-data/heroes'
SHORT={'thragg':'Thragg','invincible-blue':'Blue Mark','general-kregg':'Kregg','mauler-twin-range':'Mauler Twin','mauler-twin-melee':'Mauler Twin','capevincible':'Capevincible','darkwing-2':'Darkwing 2','damien-darkblood-under-realm':'Darkblood Under Realm','nolan':'Nolan Viltrum','robot-lp':'Robot Life Pod','atom-eve-arm':'Armored Eve','invincible':'Invincible'}
EVAL=re.compile(r'worth|good|best|build|skill|tier|meta|upgrade|invest|level|priority|\?|op |strong|weak|trash|underrated|overrated|use',re.I)
def search(q):
    for attempt in range(3):
        x=get(f"https://www.reddit.com/r/invinciblegtg/search.rss?q={urllib.parse.quote(q)}&restrict_sr=1&sort=new&t=year&limit=50")
        r=parse(x)
        if r or 'entry' in x: return r
        time.sleep(30)
    return []
ids=sys.argv[1:] or [h['id'] for h in G['heroes']]
for hid in ids:
    f=f'{OUT}/{hid}.json'
    if os.path.exists(f): continue
    h=[x for x in G['heroes'] if x['id']==hid][0]
    name=SHORT.get(hid,re.sub(r' \(.*\)','',h['name']))
    posts=search(f'"{name}"'); time.sleep(4)
    sk=search(f'{name} skills'); time.sleep(4)
    seen={};
    for p in posts+sk:
        if p['date']>='2026-08-01': seen[p['link']]=p
    cands=sorted([p for p in seen.values() if name.split()[0].lower() in (p['title']+p['text']).lower() and EVAL.search(p['title'])],key=lambda p:p['date'],reverse=True)[:3]
    threads=[]
    for p in cands:
        c=parse(get(p['link'].rstrip('/')+'/.rss?limit=100')); time.sleep(5)
        threads.append(dict(post=p,comments=[dict(a=e['author'],t=e['text'][:600]) for e in c[1:60]]))
    json.dump(dict(id=hid,name=name,posts=list(seen.values()),threads=threads),open(f,'w'))
    print(hid,len(seen),len(threads),flush=True)
