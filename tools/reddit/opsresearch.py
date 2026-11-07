import json,sys,time,re,urllib.parse,os
sys.path.insert(0,'tools/reddit')
from fetch import get,parse
OUT='reddit-data/ops';os.makedirs(OUT,exist_ok=True)
OPS={'DD':['downtown destruction','DD team'],'EWA':["everyone who's anyone",'EWA solo'],'GotG':['guardians of the globe op','gotg op team'],'RR':['reanimen rampage','RR op'],
'SO':["schools out op","school's out"],'TiH':['this is heavy','TiH team'],'TaG':['train and gain','TaG fish'],'TutH':['turn up the heat','TutH'],'WD':['well done op','well done team'],'ALL':['ops teams guide','gda ops comps']}
def search(q):
    for a in range(3):
        x=get(f"https://www.reddit.com/r/invinciblegtg/search.rss?q={urllib.parse.quote(q)}&restrict_sr=1&sort=relevance&t=year&limit=40");r=parse(x)
        if r or 'entry' in x: return r
        time.sleep(40)
    return []
for k,qs in OPS.items():
    f=f'{OUT}/{k}.json'
    if os.path.exists(f): continue
    posts={}
    for q in qs:
        for p in search(q):
            if p['date']>='2026-06-01': posts[p['link']]=p
        time.sleep(6)
    cands=sorted(posts.values(),key=lambda p:p['date'],reverse=True)
    pat=re.compile(r'team|comp|best|lineup|waves|help|setup|who|\?',re.I)
    cands=[p for p in cands if pat.search(p['title'])][:6]
    th=[]
    for p in cands:
        c=parse(get(p['link'].rstrip('/')+'/.rss?limit=100'));time.sleep(8)
        th.append(dict(post=p,comments=[e['text'][:500] for e in c[:60]]))
    json.dump(dict(op=k,posts=list(posts.values()),threads=th),open(f,'w'))
    print(k,len(posts),len(th),flush=True)
