"""Check local URLs, assets, fragments and service destinations without network requests."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from lxml import html
import json, re, sys

ROOT=Path(__file__).resolve().parents[1]
docs={p:html.fromstring(p.read_text(encoding='utf-8')) for p in ROOT.rglob('*.html') if '.git' not in p.parts}
errors=[]; checks=0
def check(u,source,base):
    global checks
    p=urlsplit(u)
    if p.netloc and p.netloc not in ['sitemagique.com','www.sitemagique.com']:return
    if p.scheme and p.scheme not in ['http','https']:return
    path=unquote(p.path)
    target=ROOT/path.lstrip('/') if path.startswith('/') else base/path
    if not path:target=source
    if target.is_dir():target=target/'index.html'
    target=target.resolve(); checks+=1
    if not target.is_file():errors.append(f'{source.relative_to(ROOT)}: missing {u}')
    elif p.fragment and target in docs and not docs[target].xpath('//*[@id=$id or @name=$id]',id=unquote(p.fragment)):
        errors.append(f'{source.relative_to(ROOT)}: missing fragment {u}')
for path,d in docs.items():
    base=ROOT if d.xpath('//base[@href="/"]') else path.parent
    for el in d.xpath('//*[@href or @src or @srcset]'):
        for attr in ['href','src']:
            if el.get(attr):check(el.get(attr),path,base)
        for src in el.get('srcset','').split(','):
            if src.strip():check(src.strip().split()[0],path,base)
    if d.xpath('//header'):
        prefix='/en/' if path.relative_to(ROOT).parts[0]=='en' else '/'
        for slug in ['creation-application','plateformes-web','crm-gestion','centre-appels','logiciels-sur-mesure','google-ads']:
            if not d.xpath('//header//a[@href=$href]',href=prefix+slug+'/'):errors.append(f'{path}: missing menu entry {slug}')
        if d.xpath('//img[contains(@src,"laptop.png")]'):errors.append(f'{path}: old laptop image remains')
for css in (ROOT/'assets/css').glob('*.css'):
    for u in re.findall(r'url\([\'"]?([^\)\'"\s]+)',css.read_text(encoding='utf-8')):
        check(u,css,css.parent)
data=json.loads((ROOT/'scripts/service-content.json').read_text(encoding='utf-8'))
for lang in ['fr','en']:
    for item in data:
        page=ROOT/('en' if lang=='en' else '')/item['slug']/'index.html'; d=docs[page]
        if len(d.xpath('//main//h1'))!=1:errors.append(f'{page}: expected one H1')
        if len(d.xpath('//main//details'))!=3:errors.append(f'{page}: FAQ missing')
        if d.xpath('//main//img[@src="/assets/images/services-beach.png"]'):errors.append(f'{page}: repeated beach photo remains')
        if not d.xpath('//main//div[contains(@class,"service-art")]'):errors.append(f'{page}: service illustration missing')
        if 'theme-' not in d.xpath('//main')[0].get('class',''):errors.append(f'{page}: service identity missing')
        if d.xpath('//base'):errors.append(f'{page}: base breaks in-page links')
print(json.dumps({'pages':len(docs),'checked_urls':checks,'errors':errors},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
