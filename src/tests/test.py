"""Headless checks for the Pages build. Run from repo root: python3 src/tests/test.py  (needs playwright + chromium)"""
import asyncio,json,os,subprocess,sys,time,socket
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PORT=8765;BASE=f'http://localhost:{PORT}/'
SAMPLE=os.environ.get('SAMPLE')  # optional saved state (JSON) to test with real data
fails=[]
def check(ok,msg):
    print(('PASS ' if ok else 'FAIL ')+msg);
    if not ok: fails.append(msg)
async def page(b,w=390,standalone=False,state=None,browser_flag=True,reduce=False):
    ctx=await b.new_context(viewport={'width':w,'height':844},reduced_motion='reduce' if reduce else 'no-preference')
    js=''
    if standalone: js+="Object.defineProperty(navigator,'standalone',{get:()=>true});"
    if browser_flag: js+="try{localStorage.setItem('gtg-use-browser','1')}catch(e){};"
    if state: js+=f"try{{if(!localStorage.getItem('gtg-advisor-state'))localStorage.setItem('gtg-advisor-state',{json.dumps(json.dumps(state))})}}catch(e){{}};"
    if js: await ctx.add_init_script(js)
    pg=await ctx.new_page();pg.errs=[];pg.ext=[]
    pg.on('pageerror',lambda e:pg.errs.append(str(e)))
    pg.on('console',lambda m:m.type=='error' and pg.errs.append(m.text))
    pg.on('request',lambda r:(not r.url.startswith(BASE) and not r.url.startswith('data:') and not r.url.startswith('blob:')) and pg.ext.append(r.url))
    return ctx,pg
async def main():
    srv=subprocess.Popen([sys.executable,'-m','http.server',str(PORT)],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
    state=json.load(open(SAMPLE)) if SAMPLE else None
    try:
      async with async_playwright() as p:
        b=await p.chromium.launch()
        # 1. first visit in a browser: install guide
        ctx,pg=await page(b,browser_flag=False);await pg.goto(BASE);await pg.wait_for_timeout(600)
        check(await pg.locator('#gtgInst').count()==1,'install guide shows on first browser visit')
        await pg.click('#gtgUseBrowser');check(await pg.locator('#gtgInst').count()==0,'"use in browser" dismisses the guide')
        check(not pg.ext,'no requests to other sites: '+', '.join(pg.ext[:3]));check(not pg.errs,'no errors (browser): '+'; '.join(pg.errs[:3]));await ctx.close()
        # 2. every tab at 3 widths: no sideways scroll, no error banner
        for w in (320,390,430):
            ctx,pg=await page(b,w=w,state=state);await pg.goto(BASE);await pg.wait_for_timeout(500)
            for t in ['home','roster','teams','database','more']:
                subs={'teams':['pvp','raid','ops','battle','meta'],'more':['player','artifacts','totems','backup','about']}.get(t,[None])
                for sv in subs:
                    await pg.evaluate(f"()=>{{tab='{t}';{'sub.tm' if t=='teams' else 'sub.mv'}={json.dumps(sv)};render()}}")
                    sw=await pg.evaluate('document.documentElement.scrollWidth');eb=await pg.evaluate("getComputedStyle(document.getElementById('err')).display")
                    if sw>w or eb!='none':check(False,f'{t}/{sv} at {w}px: width {sw}, error banner {eb}')
            check(not pg.errs,f'no errors at {w}px: '+'; '.join(pg.errs[:3]));await ctx.close()
        # 3. Home Screen mode: startup animation runs and removes itself
        ctx,pg=await page(b,standalone=True,state=state);await pg.goto(BASE)
        check(await pg.locator('#gtgSp').count()==1,'startup cover present at launch (standalone)')
        await pg.wait_for_timeout(3200);check(await pg.locator('#gtgSp').count()==0 and await pg.locator('#gtgSpS').count()==0,'cover and its style removed after the animation')
        check(not pg.errs,'no errors (standalone): '+'; '.join(pg.errs[:3]));await ctx.close()
        ctx,pg=await page(b,standalone=True,reduce=True);await pg.goto(BASE);await pg.wait_for_timeout(1500)
        check(await pg.locator('#gtgSp').count()==0,'reduced motion: short fade, then gone');await ctx.close()
        ctx,pg=await page(b);await pg.goto(BASE);await pg.wait_for_timeout(300)
        check(await pg.locator('#gtgSp').count()==0,'no startup animation in a browser tab');await ctx.close()
        # 4. data survives a reload; offline works after first visit
        ctx,pg=await page(b);await pg.goto(BASE);await pg.wait_for_timeout(800)
        await pg.evaluate("()=>{S.player.name='TESTER';save();}");await pg.reload();await pg.wait_for_timeout(500)
        check(await pg.evaluate("S.player.name")=='TESTER','data survives a reload')
        await pg.evaluate("navigator.serviceWorker.ready");await pg.wait_for_timeout(800);await pg.reload();await pg.wait_for_timeout(500)
        await ctx.set_offline(True);await pg.reload();await pg.wait_for_timeout(800)
        check(await pg.evaluate("typeof S!=='undefined'&&S.player.name==='TESTER'"),'loads offline with data');await ctx.close()
        # 5. advice rules that must never break (checked against your real data)
        ctx,pg=await page(b);await pg.goto(BASE);await pg.wait_for_timeout(800)
        r=await pg.evaluate("""()=>{const PR={S:0,A:1,B:2,C:3};const bad=[];
          owned().forEach(id=>{const ns=nextSkill(id);if(!ns)return;const u=S.heroes[id];H[id].skills.forEach((s,i)=>{const cur=Math.max(1,+(u.skills||[])[i]||1);
            if(skillUnlocked(u,i)&&cur<10&&ns.cur<10&&(PR[s.prio]??2)<(PR[ns.prio]??2))bad.push('skill: '+id+' '+ns.name+' over '+s.name);});
            const c1=JSON.stringify(nextSkill(id));if(JSON.stringify(nextSkill(id))!==c1)bad.push('skill unstable: '+id);});
          _plan=null;const f=finalArtifacts(bestTeams('pvp',{n:1})[0],{team:raidSquad().squad.slice(0,5)});
          Object.entries(f.moves).forEach(([id,m])=>{const cur=S.heroes[id].artifact;const lost=cur&&Object.values(f.moves).some(o=>norm(o.n)===norm(cur));
            if(!artBacking(m.n,id)&&cur&&!lost)bad.push('artifact: '+m.n+' -> '+id+' has no player/guide backing');
            if(!inMyTeams(id)&&!(bestTeams('pvp',{n:1})[0]||{team:[]}).team.includes(id))bad.push('artifact to unused hero: '+id);});
          const keep=JSON.stringify(Object.fromEntries(owned().map(i=>[i,S.heroes[i].artifact])));owned().forEach(i=>{S.heroes[i].artifact=f.fin[i]||'';});_plan=null;
          const f2=finalArtifacts(bestTeams('pvp',{n:1})[0],{team:raidSquad().squad.slice(0,5)});if(Object.keys(f2.moves).length)bad.push('artifacts not settled after doing the moves: '+Object.entries(f2.moves).map(([i,m])=>i+'<-'+m.n).join(', '));
          Object.entries(JSON.parse(keep)).forEach(([i,a])=>S.heroes[i].artifact=a);_plan=null;return bad;}""")
        check(not r,'advice rules hold (skills follow players\' priority; artifact moves are backed; nothing churns)'+('' if not r else ': '+'; '.join(r[:6])))
        await ctx.close()
        await b.close()
    finally: srv.terminate()
    print('\n'+('ALL PASSED' if not fails else f'{len(fails)} FAILED'));sys.exit(1 if fails else 0)
asyncio.run(main())
