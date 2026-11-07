# Player-confirmed corrections and community research, applied on top of the compiled game data.
# Reads data/game-data.base.json (compiled from game data, GTG Hub and gacha.gg) and writes data/game-data.json.
import json,os
D=os.path.dirname(os.path.abspath(__file__))+'/data';g=json.load(open(f'{D}/game-data.base.json'))
# Artifact names as the game spells them (game files via gacha.gg; GTG Hub had typos)
RENAME={'Flaxian Staff':'Flaxan Staff','Flaxian Stun Device':'Flaxan Stun Device','Medical Healband':'Medical Headband','Medkit':'MedKit','Neural-Link Chip':'Neural-link Chip'}
for a in g['artifacts']: a['name']=RENAME.get(a['name'],a['name'])
for h in g['heroes']:
    for r in h.get('artifacts',[]): r['name']=RENAME.get(r['name'],r['name'])
for c in [g.get('comps',[]),g.get('ops',[])]: pass
g['artifactRenames']=RENAME
H={h['id']:h for h in g['heroes']}
# Kanzlok is almost solely advised for Blue Mark (player, 6 Nov 2026)
H['invincible']['artifacts']=[r for r in H['invincible']['artifacts'] if r['name']!='Kanzlok']
for r in H['shapesmith']['artifacts']:
    if r['name']=='Kanzlok': r['tier']='B'; r['note']='Only if Blue Mark doesn\'t need it. '+r['note']
for r in H['invincible-blue']['artifacts']:
    if r['name']=='Kanzlok': r['note']='The Kanzlok hero: players reserve it for him. '+r['note']
for a in g['artifacts']:
    if a['name']=='Kanzlok': a['reservedFor']='invincible-blue'
json.dump(g,open(f'{D}/game-data.json','w'),indent=1)
print('overrides applied')

# Who each contested artifact goes to: r/invinciblegtg consensus, Aug-Nov 2026 (first = first claim)
g=json.load(open(f'{D}/game-data.json'))
OWN={  # r/invinciblegtg: unique comments recommending/using hero + artifact (artcount.py, deduplicated, read by hand), Nov 2026
 'Kanzlok':['invincible-blue','shapesmith'],                 # 7, 4
 'Neural-link Chip':['conquest','thragg'],                    # 5, 3 (PvP: copies a mirror Conquest/Thragg)
 "Ragnar's Claw":['thragg'],                                  # 3 + LincGames
 'GDA Cloaking Device':['thragg','universa'],                  # 6, 4 (+ LincGames: Anissa, TJ, Kregg)
 'Oxygen Helmet':['conquest','brit'],                          # 5, 5 (+ LincGames: Brit in ops, Kregg)
 "Damien Darkblood's Notes":['anissa'],                       # 5 + GTG Hub
 'Flaxan Spray Gun':['anissa'],                               # 2 + LincGames ("heal spray" = Healing Gel, not this)
 'Burger Mart Burger':['general-kregg','shapesmith','the-immortal'],  # 3 + LincGames, 2, 1
 'Body Enhancement':['space-racer'],                          # 14
 'GDA Healing Gel':['atom-eve','brit','general-kregg'],       # 5 + GTG Hub, 4 + LincGames (PvP), 3
 'GDA Mines':['thragg'],                                      # 5 + GTG Hub + LincGames
 'MedKit':['robot','general-kregg'],                          # 8, 2
 'Battle Hologram':['invincible-blue','agent-spider','omni-man'],  # 3 + LincGames + GTG Hub, 3, 2 + GTG Hub
 "Mark Grayson's Earpiece":['tech-jacket'],                   # LincGames: "def best for most players on TJ"
 'Burger Mart Trash Bag':['allen-the-alien','komodo-dragon'], # 2 ("works great on Allen"), 2 (tested synergy)
 'Golden Apple':['aquarus'],
 'Mauler Cell (Not the Clone)':['powerplex'],
}
# LincGames (guide author) "commonly suggested" artifacts, r/invinciblegtg, 6 Nov 2026
GUIDE={'GDA Cloaking Device':['anissa','tech-jacket','general-kregg'],'Flaxan Spray Gun':['anissa'],"Mark Grayson's Earpiece":['tech-jacket'],
 'Guardians of the Globe Bracelet':['tech-jacket'],'GDA Mines':['thragg'],"Ragnar's Claw":['thragg'],'Flaxan Staff':['doc-seismic'],'Body Enhancement':['space-racer'],
 'Kanzlok':['invincible-blue'],'Battle Hologram':['invincible-blue','volcanikka'],'Oxygen Helmet':['brit','general-kregg'],'GDA Healing Gel':['brit'],
 'Martian Spear':['volcanikka'],'Flaxan Anti-Aging Bracelet':['volcanikka'],'Vitals Pad':['volcanikka'],'Burger Mart Burger':['general-kregg']}
# What each artifact does, turned into who it suits - used only when players and guides say little
SYN={
 'Battle Hologram':dict(roles=['Attacker','Support'],why='cuts allies\' cooldowns each time the wielder uses an ability'),
 "Mark Grayson's Earpiece":dict(roles=['Attacker'],why='periodic AoE and damage over time scaled on the wielder\'s attack'),
 'Obedience Collar':dict(roles=['Defender','Support'],why='confuses a random enemy every 21 s (works from anyone who stays alive)'),
 'Flaxan Anti-Aging Bracelet':dict(roles=['Attacker'],why='15% shorter main-ability cooldown, for heroes whose main ability does the work'),
 'Flaxan Drone Trap':dict(roles=['Defender'],why='silences and shreds whoever debuffs the wielder - a front-line tank'),
 'Flaxan Staff':dict(roles=['Defender'],why='reflects big hits and stuns - a hero who takes heavy single hits'),
 'Martian Spear':dict(roles=['Attacker'],tags=['Melee'],why='an extra melee hit every few seconds scaled on attack'),
 'Burger Mart Trash Bag':dict(roles=['Defender'],why='fires when the wielder is crit; damage scales on the wielder\'s defence'),
 'Cerulean Cosmos Flower':dict(roles=['Support'],why='cleanses and heals allies who drop below 25%'),
 'Flaxan Defense Barrier':dict(roles=['Defender'],teamTags=['Ranged'],why='gives ranged allies defence based on the wielder\'s defence'),
 'GDA Spy Drone':dict(teamTags=['Guardians of the Globe'],why='lowers ranged enemies\' crit for each Guardians ally'),
 'Guardians of the Globe Bracelet':dict(teamTags=['Guardians of the Globe'],why='stats for each Guardians ally on the team'),
 'Medical Headband':dict(roles=['Defender'],why='AoE heal for allies next to the wielder'),
 'Thraxan Armor':dict(roles=['Defender'],why='a periodic shield (and the Leader tag)'),
 'Vitals Pad':dict(roles=['Defender'],why='+40% healing received, for a damage sponge with a healer'),
 'Flaxan Stun Device':dict(roles=['Attacker','Defender','Support'],why='stuns enemies when they are healed - a counter to healing teams'),
 'GDA Synapse Breaker':dict(roles=['Defender'],why='punishes enemies who crit the wielder - a tank'),
 'Neural Disruptor':dict(roles=['Support'],why='team healing received and a counter to confusion'),
 'GDA Behavioral Suppressant':dict(roles=['Defender'],why='a small debuff every 10 s - only for a hero who lives long'),
 'Rescue Wristband':dict(roles=['Support'],why='pulls dying allies back and heals them'),
 'Orbital Monitor':dict(roles=['Attacker','Defender','Support'],why='silences one enemy at the start (PvP)'),
 'Sinlak Beetle Dart':dict(roles=['Attacker'],why='makes an enemy taunt onto your highest physical attacker'),
}
names={a['name'] for a in g['artifacts']}; ids={h['id'] for h in g['heroes']}
for k,v in OWN.items():
    assert k in names,k
    for x in v: assert x in ids,x
for a in g['artifacts']:
    if a['name'] in OWN: a['owners']=OWN[a['name']]
    if a['name'] in GUIDE: a['guide']=GUIDE[a['name']]
    if a['name'] in SYN: a['syn']=SYN[a['name']]
for k,v in GUIDE.items():
    assert k in names,k
    for x in v: assert x in ids,x
for k in SYN: assert k in names,k
g['artifactLevels']='No level cap. The artifact\'s ability improves up to level 30; after that only its stats keep rising, and levelling no longer costs Artifact XP. Artifact XP: Common to 10, Rare to 20, Special to 30. Levels 10, 20 and 30 are big steps (50/50/100 fragments).'
g['artifactNote']='Artifacts swap everywhere at once: there is no snapshotting, so moving one for PvP also moves it in a running op.'

# Newer artifacts GTG Hub left 'Untiered' - rated from r/invinciblegtg, Jun-Nov 2026
T={
 'GDA Mines':('A',"Players' current pick for Thragg (his basic attacks are AoE) over Ragnar's Claw; also good on Tech Jacket and Volcanikka."),
 'GDA Synapse Breaker':('B','Goes on a tank that soaks crits: Conquest, Brit, Immortal or Kregg. Its big damage numbers are partly a display bug.'),
 'Neural Disruptor':('B','Team Energy Defense and healing, and cleanses Confusion - counters Thragg and Shapesmith. Best on a support like Kregg.'),
 'Orbital Monitor':('B','Strong in PvP at level 30 (silences enemies at the start, and silence now blocks skills, totems and artifacts). Weak in ops: only triggers once, not per wave.'),
 'Coalition of Planets Badge':('B','Crit damage that grows with other Coalition of Planets heroes alive - for teams with Space Racer, Tech Jacket, Anissa or Blue Mark.'),
 'Mauler Cell (The Original)':('B','Only for a Mauler ops team (Mauler Twins, Powerplex, Battle Beast); needs 2+ Maulers.'),
 'Mauler Cell (Not the Clone)':('B','Only for a Mauler ops team; the life-leech cell usually goes on Powerplex.'),
 "Ragnar's Claw":('B','A Thragg artifact (LincGames lists it after Mines); some players call it underwhelming next to Mines or the Cloak.'),
 'GDA Behavioral Suppressant':('C','Small Attack/Defense debuff every 10s - only worth it on a hero who lives a long time.'),
 'Rescue Wristband':('C','"Solid but nothing special" - for teams with no support.'),
 "Thraxan's Jetpack":('C','Only 3.5% extra damage, and only for flying heroes against grounded ones.'),
 'Sinlak Beetle Dart':('?','Too new - players haven\'t settled on it. Cuts an enemy\'s Physical Defense by 40% and makes them taunt your strongest physical attacker.'),
}
for a in g['artifacts']:
    if a['name'] in T: a['tier'],a['tierNote']=T[a['name']]; a['tierSrc']='r/invinciblegtg'
H={h['id']:h for h in g['heroes']}
H['thragg']['artifacts'].insert(0,{'name':'GDA Mines','tier':'A','note':'Current player pick: boosts his AoE basic attacks.','src':'r/invinciblegtg'})
json.dump(g,open(f'{D}/game-data.json','w'),indent=1)
print('artifact owners + tiers applied')

# Full re-check of every hero against r/invinciblegtg (Aug-Nov 2026, 3,400+ posts read via search + threads), 6 Nov 2026
g=json.load(open(f'{D}/game-data.json'));H={h['id']:h for h in g['heroes']}
T={ # id: (pvp,ops,raid,note)
 'nolan':('C','F','F','Players: "stop building him" - outclassed by newer Viltrumites. Food.'),
 'machine-head':('C','C','F','Luxury build: "no way worth building over Doc, Volk, Powerplex, Maulers".'),
 'thaedus':('B','C','C','Players split: some feed him, others still run him for his DoT and bulk. Kregg does the support job better.'),
 'the-immortal':('B','F','C','Players split (one "don\'t waste anything on him", one "replaced Allen in PvP with good success") - GTG Hub\'s PvP B stands. Brit is the stronger tank.'),
 'universa':('A','A','B','Still widely used and praised (Train and Gain, Downtown Destruction, event ops), but a 2nd Space Racer is the stronger ops pick.'),
 'battle-beast':('B','F','C','Few recent opinions: fans still run him in PvP; some players have stopped building him. Weak in ops.'),
 'allen-the-alien':('B','B','C','"Solid", "second-best FWB defender" but outclassed by Brit; fine Well Done slot.'),
 'agent-spider':('B','A','B','Great in ops (crit Well Done team); his crit stacking is underwhelming in PvP. Luxury build behind Tech Jacket.'),
 'flaxan-leader':('B','A','B','Ops farmer: his 3rd skill raises GDA Op rewards; good with Space Racer.'),
 'omni-man':('B','A','B','Players split on PvP (some feed him, some still carry with him); core of the Well Done crit team.'),
 'red-rush':('B','B','B','Fine early; Tech Jacket and Blue Mark are the Earth\'s Defenders to build first.'),
 'war-woman':('C','C','C','Little player talk; GTG Hub lists her as food. One player reports strong PvP damage.'),
 'wolf-man':('B','C','B','Too new to call: looking like a solid PvP tank, weak in ops. Oxygen Helmet, Healing Gel or Cloak.'),
 'damien-darkblood-under-realm':('C','B','C','Most players feed him; still used in the Well Done Subsoil team.'),
 'shapesmith':('A','A','B','Great early and in Alliance War; falls off in late PvP unless his Kanzlok is level 20+.'),
}
for k,(p,o,r,n) in T.items():
    H[k]['tier']={'pvp':p,'ops':o,'raid':r}; H[k]['note']=n
for h in g['heroes']: h['tierSrc']='GTG Hub (Aug) checked against r/invinciblegtg Aug-Nov 2026'
for k in T: H[k]['tierSrc']='r/invinciblegtg, Aug-Nov 2026'
# Skill upgrade order: Hub skill tiers cross-checked with players. to15 = players push this skill to 15.
SK={'general-kregg':{2:'S'},'space-racer':{3:'S'},'cecil-stedman':{2:'A',3:'A'},'rex-splode':{1:'S',2:'A'}}  # Rex: 2nd skill first for the Well Done crit team (players, Jun 2026), then Cherry Bomb
for k,m in SK.items():
    for i,pr in m.items(): H[k]['skills'][i]['prio']=pr
# only where 2+ players say to push past 10 (or an op needs it): Anissa 2nd, Blue Mark 2nd, TJ 2nd, SR 4th, Thragg 1st & 4th and Kregg 3rd (This Is Heavy)
TO15={'anissa':[1],'thragg':[0,3],'general-kregg':[2],'tech-jacket':[1],'invincible-blue':[1],'space-racer':[3]}
# Levels players widely say a skill should reach (only where several players agree)
# Agent Spider 2nd: "get 2nd skill to at least 10" for ops / Well Done crit (3 players + LincGames' WD team note)
TARGETS={'agent-spider':{1:(10,'Players: get his 2nd skill to at least 10 for ops - it\'s why he\'s in the Well Done crit team.')}}
for k,d in TARGETS.items():
    h=next(x for x in g['heroes'] if x['id']==k)
    for i,(lv,why) in d.items(): h['skills'][i]['target']=lv; h['skills'][i]['targetWhy']=why
for k,ix in TO15.items():
    for i in ix: H[k]['skills'][i]['to15']=True
g['skillPrioNote']='Skill priority: GTG Hub skill tiers (July), cross-checked with r/invinciblegtg. Skills marked "to 15" are the ones players push past 10; others are fine at 10.'
# Ops and raid additions from players
O={o['id']:o for o in g['ops']}
O['reanimen-rampage']['now']+=' At high ranks Cecil can carry it alone with four level-1 Multi-Pauls as sacrifices.'
O['turn-up-the-heat']['now']+=' Players use 4 fish + a ranged hero, or Powerplex with Mauler Cells + Maulers.'
g['raid']['notes'].append('Brit with the Flaxan Staff does real work in Boss Raid (Flaxan Staff now reflects true damage).')
json.dump(g,open(f'{D}/game-data.json','w'),indent=1)
print('hero/skill re-check applied')

g=json.load(open(f'{D}/game-data.json'))
for a in g['artifacts']:
    if not a.get('source'): a['source']='Limited: events, event trophy roads and artifact passes (rotating)'
json.dump(g,open(f'{D}/game-data.json','w'),indent=1)

g=json.load(open(f'{D}/game-data.json'));H={h['id']:h for h in g['heroes']}
H['aquarus']['keepBase']='Players keep Aquarus (fish) at base skills for ops teams - leave his skills at 1.'
H['multi-paul']['keepBase']='Kept at low level as sacrifices in This Is Heavy - don\'t invest.'
O={o['id']:o for o in g['ops']}
O['everyone-whos-anyone']['alts']={'brit':['invincible']}
O['everyone-whos-anyone']['now']='Solo hero. Brit is best once built (skills 4, then 1, then 2); a high-level Yark (Invincible) also gets high waves - use whichever is stronger on your account.'
json.dump(g,open(f'{D}/game-data.json','w'),indent=1)

# Several player teams per op (Reddit + GTG Hub); the app checks your team against the closest one
g=json.load(open(f'{D}/game-data.json'));O={o['id']:o for o in g['ops']}
def comps(o): 
    out=[]; 
    if o.get('comp'): out.append(o['comp'])
    out+= [c['heroes'] for c in o['hubComps'] if c['heroes']]
    return out
EXTRA={'downtown-destruction':[['anissa','invincible-blue']],
 'this-is-heavy':[['powerplex','mauler-twin-melee','mauler-twin-range']],
 'reanimen-rampage':[['cecil-stedman','multi-paul','multi-paul','multi-paul','multi-paul'],['mauler-twin-melee','mauler-twin-range','powerplex','mauler-twin-melee','mauler-twin-range']],
 'everyone-whos-anyone':[['invincible']],
 'well-done':[['omni-man','rex-splode','agent-spider','allen-the-alien','red-rush']]}
for k,o in O.items():
    cs=comps(o)+EXTRA.get(k,[])
    if k=='everyone-whos-anyone': cs=[['brit'],['invincible']]
    seen=[];[seen.append(c) for c in cs if c not in seen]
    o['comps']=seen
json.dump(g,open(f'{D}/game-data.json','w'),indent=1)

# Whole-team templates per op from r/invinciblegtg (Jun-Nov 2026) + GTG Hub. core = what the team is built around,
# flex = heroes players slot in around the core, sac = low-level sacrifice/fish slots (level doesn't matter).
g=json.load(open(f'{D}/game-data.json'));O={o['id']:o for o in g['ops']}
T={
'downtown-destruction':dict(rule='Anissa does most of the work here (pink XP).',templates=[
  dict(name='Space Racer + Anissa',core=['anissa','space-racer'],flex=['invincible-blue','volcanikka','rus-livingston','universa','doc-seismic']),
  dict(name='Universa + Anissa + Blue Mark',core=['anissa','universa','invincible-blue'],flex=['rus-livingston','doc-seismic','volcanikka'],sac=['kid-omni-man']),
  dict(name='Anissa + Universa',core=['anissa','universa'],flex=['doc-seismic','volcanikka','invincible-blue'],sac=['kid-omni-man'])]),
'everyone-whos-anyone':dict(rule='Solo op: one hero only - adding others lowers waves (Cecil alongside Yark is the only pairing players mention).',solo=True,templates=[
  dict(name='Solo Brit',core=['brit']),dict(name='Solo Yark',core=['invincible'],flex=['cecil-stedman'])]),
'guardians-of-the-globe':dict(rule='Armour (gear) op, low priority: players fill it with heroes no better op needs. Criminals get a 20% faction boost here. A Lizard League team (Komodo, King Lizard, Iguana + the 2 common Lizard soldiers) reaches ~1,400 waves without taking anyone from other ops.',templates=[
  dict(name='Lizard League',core=['komodo-dragon','king-lizard','iguana'],flex=['lizard-soldier-m','lizard-soldier-f','angstrom-levy','titan']),
  dict(name='Criminals (20% boost)',core=['komodo-dragon','angstrom-levy','titan'],flex=['king-lizard','iguana','magmaniac','powerplex','mauler-twin-range','machine-head'],thin=True),
  dict(name='Maulerplex (filler)',core=['powerplex','mauler-twin-range'],flex=['mauler-twin-range','mauler-twin-range','mauler-twin-range'],thin=True)]),
'reanimen-rampage':dict(rule='Cecil carries it with sacrifices, or a Mauler team.',templates=[
  dict(name='Cecil + sacrifices',core=['cecil-stedman'],sac=['multi-paul','multi-paul','multi-paul','multi-paul']),
  dict(name='Maulerplex',core=['powerplex','mauler-twin-range','mauler-twin-melee'],flex=['angstrom-levy','battle-beast'])]),
# TiH (LincGames + players, Oct-Nov 2026): "3 rare & lvl1 Multi-Pauls, Thragg & Kregg is an easy min-max comp"; at higher op ranks add
# Conquest (the op throws immunity-barrier enemies at you), Cecil, Blue Mark, Anissa or Agent Spider. Sacrifices should die easily: level 1 is fine
# ("lvl 340 vs lvl 1 the difference is minimal"); Multi-Paul's 3rd skill makes a copy when he dies = 2 deaths each; Ragnars tested much worse.
'this-is-heavy':dict(rule='Kregg\'s 3rd skill charges Thragg every time an ally dies, so the team feeds him sacrifices: Multi-Pauls at level 1 are fine (his 3rd skill gives two deaths each; Ragnars do much worse). Thragg at the back so the sacrifices get hit first. At higher op ranks swap sacrifices for Conquest, Cecil, Blue Mark, Anissa or Agent Spider.',templates=[
  dict(name='Thragg + Kregg + Multi-Paul sacrifices',core=['thragg','general-kregg'],sac=['multi-paul','multi-paul','multi-paul'],flex=['conquest','cecil-stedman','invincible-blue','anissa','agent-spider','tech-jacket','doc-seismic']),
  dict(name='Thragg + Kregg + Volcanikka summons',core=['thragg','general-kregg','volcanikka'],flex=['multi-paul','tech-jacket','doc-seismic','conquest'],thin=True)]),
'train-and-gain':dict(rule='Space Racer (front left) with Body Enhancement + fish. Tech Jacket adds far less here (~30-40 waves) than in Well Done (~110).',templates=[
  dict(name='Space Racer + 4 fish',core=['space-racer'],sac=['aquarus','aquarus','aquarus','aquarus']),
  dict(name='Space Racer + Tech Jacket + fish',core=['space-racer','tech-jacket'],sac=['aquarus','aquarus','aquarus']),
  dict(name='Space Racer + Flaxan Leaders + fish',core=['space-racer'],flex=['flaxan-leader','flaxan-leader'],sac=['aquarus','aquarus']),
  dict(name='Maulerplex',core=['powerplex','mauler-twin-range','mauler-twin-melee'],flex=['mauler-twin-range','mauler-twin-melee'])]),
'turn-up-the-heat':dict(rule='Gold only - lowest priority. Short op: fish teams or Maulerplex.',templates=[
  dict(name='Space Racer + Tech Jacket + fish',core=['space-racer'],flex=['tech-jacket','anissa'],sac=['aquarus','aquarus']),
  dict(name='Maulerplex',core=['powerplex','mauler-twin-range'],flex=['mauler-twin-range','mauler-twin-melee','angstrom-levy']),
  dict(name='5 fish',core=[],sac=['aquarus','aquarus','aquarus','aquarus','aquarus'])]),
'well-done':dict(rule='Crit team makes Omni-Man "unstoppable" (needs Rex and Agent Spider 2nd skills); Cecil (3rd skill to 10) and Tech Jacket push waves.',templates=[
  dict(name='Crit team',core=['omni-man','rex-splode','agent-spider'],flex=['tech-jacket','cecil-stedman','allen-the-alien']),
  dict(name='Subsoil',core=['volcanikka','damien-darkblood-under-realm','doc-seismic'],flex=['omni-man','agent-spider','tech-jacket'])]),
'schools-out':dict(rule='Only worth running during All Hands on Deck events (rewards come from the recruitment pool).',templates=[
  dict(name='Space Racer + Anissa + Tech Jacket + fish',core=['space-racer','anissa','tech-jacket'],flex=['invincible-blue','tech-jacket'],sac=['aquarus','aquarus'])]),
}
O['guardians-of-the-globe'].update(name='The Guardians Around The Globe',short='TGAG',priority='low',now='Armour op. Leftover heroes; Criminals get +20%. Lizard League (Komodo, King Lizard, Iguana + 2 Lizard soldiers) is the comp players name.')
for k,v in T.items():
    O[k]['templates']=v['templates'];O[k]['rule']=v['rule'];O[k]['solo']=v.get('solo',False)
    O[k]['comps']=[(t['core']+t.get('flex',[])+t.get('sac',[]))[:5] for t in v['templates']]
g['eventOpTip']='Event ops last 3-5 minutes: players pull Space Racer and Anissa out of their usual op for a few runs. A second, unskilled level-340 Space Racer and 3-4 level-159 fish cover most event ops.'
json.dump(g,open(f'{D}/game-data.json','w'),indent=1)
