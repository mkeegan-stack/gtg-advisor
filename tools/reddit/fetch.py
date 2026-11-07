import sys, time, subprocess, re, html, json, urllib.parse, xml.etree.ElementTree as ET
UA="Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36"
NS={'a':'http://www.w3.org/2005/Atom'}
def get(url):
    r=subprocess.run(["curl","-s","-L","-A",UA,url],capture_output=True,text=True)
    return r.stdout
def parse(xml):
    try: root=ET.fromstring(xml)
    except Exception: return []
    out=[]
    for e in root.findall('a:entry',NS):
        t=e.findtext('a:title',default='',namespaces=NS)
        link=e.find('a:link',NS).get('href') if e.find('a:link',NS) is not None else ''
        upd=e.findtext('a:updated',default='',namespaces=NS) or e.findtext('a:published',default='',namespaces=NS)
        c=e.findtext('a:content',default='',namespaces=NS)
        c=re.sub(r'<[^>]+>',' ',html.unescape(c)); c=re.sub(r'\s+',' ',c).strip()
        a=e.find('a:author/a:name',NS); a=a.text if a is not None else ''
        out.append(dict(title=t,link=link,date=upd[:10],author=a,text=c))
    return out
if __name__=="__main__":
    queries=sys.argv[1:]
    res={}
    for q in queries:
        url=f"https://www.reddit.com/r/invinciblegtg/search.rss?q={urllib.parse.quote(q)}&restrict_sr=1&sort=new&t=year&limit=50"
        res[q]=parse(get(url)); time.sleep(8)
    json.dump(res,open('reddit-data/raw/search.json','w'),indent=1)
    seen=set()
    for q,items in res.items():
        print(f"\n### {q} ({len(items)})")
        for i in items[:25]:
            if i['link'] in seen: continue
            seen.add(i['link']); print(i['date'], '|', i['title'][:110])
