import os,re,json,collections
texts=set()
for root,_,fs in os.walk('reddit-data'):
    for f in fs:
        p=os.path.join(root,f)
        try:t=open(p,errors='ignore').read()
        except:continue
        if f.endswith('.json'):
            try:
                d=json.loads(t)
                def walk(x):
                    if isinstance(x,dict):
                        for k,v in x.items():
                            if k in('text','t') and isinstance(v,str):texts.add(v)
                            else:walk(v)
                    elif isinstance(x,list):
                        for v in x:
                            if isinstance(v,str):texts.add(v)
                            else:walk(v)
                walk(d)
            except Exception:pass
        else:
            for line in t.split('\n'):
                if line.startswith('- ['):texts.add(line.split('] ',1)[-1])
H={'anissa':r'anis+a|annis+a','invincible-blue':r'blark|blue mark|blue suit|invincible blue|black (?:and|&) blue','invincible':r'yark|yellow mark|yellow invincible|\byinv','conquest':r'conquest','thragg':r'thragg','general-kregg':r'kregg','omni-man':r'omni[ -]?man|nolan','robot':r'\brobot\b','atom-eve':r'\beve\b','tech-jacket':r'tech ?jacket|\btj\b','space-racer':r'space ?racer|\bsr\b','universa':r'universa|\buni\b','shapesmith':r'shape ?smith|\bss\b','the-immortal':r'immortal','brit':r'\bbrit\b|\bbritt\b','doc-seismic':r'doc seismic|\bdoc\b','volcanikka':r'volc\w*','rex-splode':r'\brex\b','allen-the-alien':r'\ballen\b','cecil-stedman':r'cecil','agent-spider':r'spider','powerplex':r'power ?plex','battle-beast':r'battle beast','titan':r'\btitan\b','volcanikka':r'volc\w*|vulc\w*','komodo-dragon':r'komodo','seance-dog':r'seance','monster-girl':r'monster ?girl','agent-spider':r'agent spider|\bspider\b','thula':r'thula','donald-ferguson':r'donald','invincible':r'yark|yellow mark|yellow invincible|\bog mark\b','dinosaurus':r'dino\w*','mauler-twin-range':r'ranged mauler|mauler','green-ghost':r'green ghost','rus-livingston':r'\brus\b','kid-omni-man':r'kid omni','damien-darkblood-under-realm':r'armou?red (damien|darkblood)|under ?realm'}
A={"Damien Darkblood's Notes":r"darkblood'?s? notes?|\bdd notes|notebook|(?<!patch )\bnotes\b","Flaxan Spray Gun":r"spray ?gun|flaxan gun|\bspray\b","GDA Cloaking Device":r"cloak\w*","Mark Grayson's Earpiece":r"ear ?piece","Neural-link Chip":r"neural|n ?link","MedKit":r"med ?kit|medipac","GDA Healing Gel":r"healing gel|\bgel\b","Burger Mart Burger":r"burger(?! mart trash)","Burger Mart Trash Bag":r"trash bag","Oxygen Helmet":r"oxygen|helmet","Martian Spear":r"spear","Battle Hologram":r"hologram|\bholo\b","Guardians of the Globe Bracelet":r"globe bracelet|gotg bracelet|guardians bracelet|globe thing","Flaxan Anti-Aging Bracelet":r"anti[- ]?aging|flaxan belt|flaxan bracelet","GDA Mines":r"\bmines\b|gda mine","Obedience Collar":r"collar","Kanzlok":r"kanz\w*","Body Enhancement":r"body enhance\w*|body enchant\w*","Flaxan Staff":r"staff","Flaxan Defense Barrier":r"barrier","Flaxan Stun Device":r"stun device","GDA Spy Drone":r"spy ?drone","Flaxan Drone Trap":r"drone trap","Cerulean Cosmos Flower":r"flower","Medical Headband":r"headband","Vitals Pad":r"vital","GDA Synapse Breaker":r"synapse","Ragnar's Claw":r"claw","Golden Apple":r"apple","Thraxan Armor":r"thraxan armou?r","Neural Disruptor":r"disruptor|dampener","Orbital Monitor":r"orbital","Rescue Wristband":r"wristband","Sinlak Beetle Dart":r"beetle|sinlak","Coalition of Planets Badge":r"(cop|coalition) badge","GDA Behavioral Suppressant":r"suppressant","Mauler Cell":r"mauler cell","GDA Spy Drone":r"spy ?drone","Flaxan Drone Trap":r"drone trap"}
c=collections.Counter();ex=collections.defaultdict(list);seenc=set()
for t in texts:
    for cl in re.split(r'[.;\n|!?]|,(?=\s*[A-Za-z ]{0,25}(?:-|:|on|with))|\band\b',t):
        l=cl.lower()
        hs=[h for h,r in H.items() if re.search(r,l)]
        ar=[a for a,r in A.items() if re.search(r,l)]
        key=re.sub(r'\W+',' ',l).strip()[:80]
        if len(hs)==1 and len(ar)==1 and (ar[0],hs[0],key) not in seenc:
            seenc.add((ar[0],hs[0],key))
            c[(ar[0],hs[0])]+=1;ex[(ar[0],hs[0])].append(cl.strip()[:120])
by=collections.defaultdict(list)
for (a,h),n in c.items():by[a].append((n,h))
for a in sorted(by):
    print(a,':',', '.join(f'{h} {n}' for n,h in sorted(by[a],reverse=True)[:6]))
json.dump({f'{a}|{h}':ex[(a,h)][:5] for (a,h) in c},open('reddit-data/artpairs.json','w'),indent=1)
print(len(texts),'texts')
