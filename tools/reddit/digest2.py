import json,sys,re,os
G=json.load(open('src/data/game-data.json'));H={h['id']:h for h in G['heroes']}
for hid in sys.argv[1:]:
    f=f'reddit-data/heroes/{hid}.json'
    if not os.path.exists(f): print('MISSING',hid);continue
    d=json.load(open(f));h=H[hid]
    keys=[d['name'].split()[0].lower()]+[a.lower() for a in h.get('alias',[]) if len(a)>2]
    if hid=='invincible':keys=['yark','yellow mark','og mark','regular invincible','invincible ']
    if hid=='invincible-blue':keys=['blark','blue mark','blue invincible']
    pat=re.compile('|'.join(re.escape(k) for k in keys),re.I)
    out=[]
    for t in d['threads']:
        for c in t['comments']:
            if pat.search(c['t']) or pat.search(t['post']['title']):
                if len(c['t'])>30: out.append(c['t'][:220])
    for p in d['posts']:
        if pat.search(p['text']) and re.search(r'good|best|worth|bad|meta|tier|skill|build|op\b|carry|strong|weak',p['text'],re.I):
            m=pat.search(p['text']);out.append('[post] '+p['text'][max(0,m.start()-60):m.start()+160])
    print(f'## {hid} [{len(d["posts"])}]');[print(' -',x.replace('\n',' ')) for x in out[:7]]
