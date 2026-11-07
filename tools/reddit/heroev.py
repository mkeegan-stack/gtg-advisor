import json,re,os,sys,collections
sys.path.insert(0,'tools/reddit')
exec(open('tools/reddit/artcount.py').read().split("H={")[0])  # loads texts
ALIAS={'nolan':r'\bnolan\b','machine-head':r'machine ?head','thaedus':r'thaedus','the-immortal':r'immortal','universa':r'universa|\buni\b','battle-beast':r'battle ?beast','allen-the-alien':r'\ballen\b','agent-spider':r'agent spider|\bspider\b','flaxan-leader':r'flaxan leader','omni-man':r'omni[ -]?man','red-rush':r'red rush','war-woman':r'war ?woman','wolf-man':r'wolf ?man','damien-darkblood-under-realm':r'darkblood|armou?red damien|under ?realm','shapesmith':r'shape ?smith'}
NEG=r"\bfood\b|fodder|don'?t (?:build|waste|invest|bother)|not worth|useless|trash|bad\b|weak|mid\b|outclassed|fell off|falls off|skip|meh|overrated"
POS=r"\bbest\b|great|strong|broken|insane|\bop\b|meta|must|carry|carries|love|worth (?:it|building)|good"
for h,r in ALIAS.items():
    pos=neg=0;ex=[]
    for t in texts:
        for s in re.split(r'(?<=[.!?\n])\s+',t):
            l=s.lower()
            if not re.search(r,l):continue
            n=bool(re.search(NEG,l));p=bool(re.search(POS,l))
            if n and not p:neg+=1;ex.append('- '+s[:160])
            elif p and not n:pos+=1;ex.append('+ '+s[:160])
    print(f'== {h}: +{pos} -{neg}')
    if h in sys.argv[1:]:print('\n'.join(ex[:40]))
