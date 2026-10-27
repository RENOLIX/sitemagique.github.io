"""Read-only check of external links; provider bot blocks are reported separately."""
from pathlib import Path
from lxml import html
from urllib.parse import urlsplit
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor
import json
ROOT=Path(__file__).resolve().parents[1]
links=set()
for f in ROOT.rglob('*.html'):
    for a in html.fromstring(f.read_text(encoding='utf-8')).xpath('//a[@href]'):
        u=a.get('href');p=urlsplit(u)
        if p.scheme in ['https','http'] and p.netloc not in ['sitemagique.com','www.sitemagique.com'] and p.netloc!='wa.me':links.add(u)
def inspect(u):
    try:
        with urlopen(Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as r:return {'url':u,'status':r.status,'final_url':r.url}
    except HTTPError as e:return {'url':u,'status':e.code}
    except Exception as e:return {'url':u,'error':str(e)[:160]}
with ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(inspect,sorted(links)))
print(json.dumps(results,ensure_ascii=False,indent=2))
