import json,time,urllib.parse,re,sys,os
sys.path.insert(0,'tools/reddit')
from fetch import get,parse
Q={"Battle Hologram":["battle hologram","hologram"],"Mark Grayson's Earpiece":["earpiece"],"Obedience Collar":["obedience collar","collar"],"Flaxan Anti-Aging Bracelet":["anti aging bracelet","anti-aging"],"Flaxan Drone Trap":["drone trap"],"Flaxan Staff":["flaxan staff"],"Martian Spear":["martian spear"],"Burger Mart Trash Bag":["trash bag"],"Cerulean Cosmos Flower":["cosmos flower"],"Flaxan Defense Barrier":["defense barrier"],"GDA Spy Drone":["spy drone","spydrone"],"Guardians of the Globe Bracelet":["guardians bracelet","globe bracelet"],"Medical Headband":["headband"],"Thraxan Armor":["thraxan armor"],"Vitals Pad":["vitals pad"],"Flaxan Stun Device":["stun device"],"GDA Synapse Breaker":["synapse breaker"],"Neural Disruptor":["neural disruptor"],"Orbital Monitor":["orbital monitor"],"Rescue Wristband":["rescue wristband"],"Sinlak Beetle Dart":["beetle dart","sinlak"],"Coalition of Planets Badge":["coalition badge","cop badge"],"GDA Behavioral Suppressant":["behavioral suppressant"],"Mauler Cell (The Original)":["mauler cell"],"Flaxan Spray Gun":["spray gun"],"GDA Healing Gel":["healing gel"],"Burger Mart Burger":["burger mart burger"]}
for name,qs in Q.items():
    fn=f'reddit-data/arts/{re.sub(r"[^a-z]","_",name.lower())}.json'
    if os.path.exists(fn): continue
    posts={}
    for q in qs[:1]:
        for attempt in range(3):
            r=parse(get(f"https://www.reddit.com/r/invinciblegtg/search.rss?q={urllib.parse.quote(q)}&restrict_sr=1&sort=relevance&t=all&limit=50"));time.sleep(9)
            if r: break
            time.sleep(30)
        for p in r: posts[p['link']]=p
    key=qs[0].split()[-1].lower()
    threads=[]
    cand=[p for p in posts.values() if any(k in (p['title']+' '+p['text']).lower() for k in [q.lower() for q in qs])][:3]
    for p in cand:
        for attempt in range(3):
            c=parse(get(p['link'].rstrip('/')+'/.rss?limit=100'));time.sleep(9)
            if c: break
            time.sleep(30)
        threads.append(dict(post=p,comments=[x['text'] for x in c]))
    json.dump(dict(artifact=name,posts=list(posts.values()),threads=threads),open(fn,'w'))
    print(name,len(posts),'posts',len(threads),'threads',sum(len(t['comments']) for t in threads),'comments',flush=True)
