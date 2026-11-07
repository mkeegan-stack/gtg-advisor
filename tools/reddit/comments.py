import json,sys,time,re
sys.path.insert(0,'tools/reddit')
from fetch import get,parse
data=json.load(open('reddit-data/raw/search.json'))
idx={}
for q,items in data.items():
    for i in items: idx[i['title']]=i
want=[l.strip() for l in open('reddit-data/want.txt') if l.strip()]
out=[]
for w in want:
    m=[i for t,i in idx.items() if t.startswith(w)]
    if not m: print("MISSING",w); continue
    p=m[0]; url=p['link'].rstrip('/')+'/.rss?limit=100'
    c=parse(get(url)); time.sleep(12)
    out.append(dict(post=p,comments=c))
    print(f"\n===== {p['date']} | {p['title']} ({len(c)} entries)")
    for e in c[:40]:
        t=e['text'][:500]
        if t: print(f"- [{e['author']}] {t}")
json.dump(out,open('reddit-data/raw/threads_arts2.json','w'),indent=1)
