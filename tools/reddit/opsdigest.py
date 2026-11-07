import json,sys,re
NAMES=r'thragg|kregg|blark|blue mark|yark|invincible|anissa|space racer|\bsr\b|universa|uni\b|fish|aquarus|multi.?paul|cecil|conquest|brit|omni.?man|tech jacket|\btj\b|rex|agent spider|spider|allen|eve|robot|volc|doc|darkblood|damien|maul|powerplex|shapesmith|titan|iguana|king lizard|angstrom|seance|thula|kid omni|lucan|rus|nolan|war woman|battle beast|ragnar|immortal|komodo|dino|red rush|thaedus|flaxan|wolf|monster girl|donald|dupli|green ghost'
pat=re.compile(NAMES,re.I)
for k in sys.argv[1:]:
    d=json.load(open(f'reddit-data/ops/{k}.json'))
    print(f'######## {k}')
    for t in d['threads']:
        print(' ##',t['post']['date'],t['post']['title'][:90],'|',t['post']['text'][:200].replace('\n',' '))
        n=0
        for c in t['comments'][1:]:
            if pat.search(c) and len(c)>40: print('   -',c[:260].replace('\n',' '));n+=1
            if n>=6:break
