"""Build the service pages and repair shared links in the static FR/EN site."""
from pathlib import Path
from lxml import html, etree
from html import escape as esc
from urllib.parse import urlsplit
import json, re, copy

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'scripts/service-content.json').read_text(encoding='utf-8'))
VERSION = '20261027-1'
PHOTO = '/assets/images/services-beach.png'
def fragment(s): return html.fromstring(s)
def serial(e): return html.tostring(e, encoding='unicode', method='html', with_tail=False)
def url(slug, lang): return ('/en/' if lang == 'en' else '/') + slug.strip('/') + '/'
def document(path): return (ROOT/path).read_text(encoding='utf-8')
def put(path, text):
    p = ROOT/path; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding='utf-8')
def replace_element(text, tag, replacement): return re.sub(fr'<{tag}\b[^>]*>.*?</{tag}>', lambda m: replacement, text, count=1, flags=re.S)

NAV = {}; FOOTER = {}
for lang in ['fr','en']:
    text = document('en/index.html' if lang == 'en' else 'index.html')
    header = fragment(re.search(r'<header\b.*?</header>',text,re.S)[0])
    dropdowns = header.xpath('.//li[contains(concat(" ",@class," ")," cs-dropdown ")]')
    services = dropdowns[1]; services.set('class','cs-li cs-dropdown sm-services-menu')
    panel = services.xpath('./ul')[0]
    for child in list(panel): panel.remove(child)
    entries = [('web-design','Sites web & e-commerce','Websites & e-commerce')]
    entries += [(x['slug'],x['fr']['label'],x['en']['label']) for x in DATA]
    entries.insert(6,('seo-services','Référencement SEO','Search engine optimisation'))
    entries.append(('white-label-partnerships','Tous nos services','All services'))
    for slug, fr, en in entries:
        panel.append(fragment(f'<li class="cs-drop-li"><a class="cs-li-link cs-drop-link" href="{url(slug,lang)}">{esc(en if lang=="en" else fr)}</a></li>'))
    for item in dropdowns:
        item.attrib.pop('tabindex',None)
        trigger = item.xpath('./span|./button')[0]; trigger.tag='button'; trigger.set('type','button'); trigger.set('class','cs-li-link sm-menu-trigger'); trigger.set('aria-expanded','false')
    NAV[lang] = serial(header)
    footer = fragment(re.search(r'<footer\b.*?</footer>',text,re.S)[0])
    quick = footer.xpath('.//ul[contains(@class,"cs-ul-1")]')[0]
    for child in list(quick): quick.remove(child)
    for slug,fr,en in [('', 'Accueil','Home'),('about','À propos','About'),('web-design','Sites web','Websites'),('creation-application','Applications','Applications'),('logiciels-sur-mesure','Logiciels','Software'),('crm-gestion','CRM & gestion','CRM & management'),('centre-appels','Centres d’appels','Call centres'),('plateformes-web','Plateformes web','Web platforms'),('white-label-partnerships','Tous nos services','All services'),('blog','Blog','Blog')]:
        href=url(slug,lang).replace('//','/')
        quick.append(fragment(f'<li class="cs-li"><a class="cs-link" href="{href}">{esc(en if lang=="en" else fr)}</a></li>'))
    FOOTER[lang]=serial(footer)

for lang in ['fr','en']:
    en=lang=='en'; pre='/en/' if en else '/'
    template = document('en/web-design/index.html' if en else 'web-design/index.html')
    for item in DATA:
        d=item[lang]; slug=item['slug']; pageurl=url(slug,lang)
        title=d['label']+' | SITE MAGIQUE'
        photo_alt='Tropical beach beside a wooden villa' if en else 'Plage tropicale et villa en bois au bord de la mer'
        feature_html=''.join(f'<article class="sm-feature"><span class="sm-feature-number">{i+1:02}</span><h3>{esc(t)}</h3><p>{esc(p)}</p></article>' for i,(t,p) in enumerate(d['features']))
        faqs=''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in d['faq'])
        steps=[('Discovery','Your goals, users, constraints and priorities.'),('Design','Journeys and deliverables to review before production.'),('Implementation','Development or setup, with progress reviews.'),('Validation & delivery','Checks, your approval, deployment and onboarding.')] if en else [('Cadrage','Vos objectifs, utilisateurs, contraintes et priorités.'),('Conception','Des parcours et livrables à valider avant la réalisation.'),('Réalisation','Développement ou configuration, avec des points d’avancement.'),('Validation & livraison','Vérifications, votre validation, mise en service et prise en main.')]
        steps_html=''.join(f'<li><strong>0{i+1}</strong><h3>{t}</h3><p>{p}</p></li>' for i,(t,p) in enumerate(steps))
        deliver=['A clear scope and itemised proposal','Deliverables reviewed with your team','Checks for the agreed user journeys','Handover and an identified support contact'] if en else ['Un périmètre clair et un devis détaillé','Des livrables validés avec votre équipe','Des vérifications sur les parcours convenus','Une prise en main et un interlocuteur identifié']
        related=[x for x in DATA if x['slug'] != slug][:3]
        if slug in ['crm-gestion','centre-appels','plateformes-web','creation-application']:
            related=[x for x in DATA if x['slug'] in ['crm-gestion','centre-appels','plateformes-web','creation-application'] and x['slug']!=slug]
        related_html=''.join(f'<a href="{url(x["slug"],lang)}">{esc(x[lang]["label"])} <span aria-hidden="true">↗</span></a>' for x in related)
        contact=pre+'contact/?service='+slug
        main=f'''<main id="main" class="sm-service">
<section class="sm-service-hero"><div class="sm-wrap">
<div class="sm-hero-grid"><div><span class="sm-eyebrow">SITE MAGIQUE / {esc(d['label'])}</span><h1>{esc(d['title'])}</h1><p>{esc(d['intro'])}</p><div class="sm-actions"><a class="cs-button-solid" href="{contact}">{'Discuss your project' if en else 'Parlons de votre projet'}</a><a class="sm-text-link" href="#fonctionnalites">{'Explore the service' if en else 'Découvrir la solution'}</a></div><p class="sm-note">{'Custom proposal · Remote collaboration worldwide' if en else 'Devis personnalisé · Accompagnement à distance partout dans le monde'}</p></div><figure class="sm-service-visual"><img src="{PHOTO}" alt="{photo_alt}" width="1200" height="2133" fetchpriority="high"></figure></div></div></section>
<div class="sm-highlights"><div><strong>{'A solution for your business' if en else 'Une solution pour votre métier'}</strong>{'Scope defined together' if en else 'Un périmètre défini ensemble'}</div><div><strong>{'Clear project milestones' if en else 'Des étapes claires'}</strong>{'Review progress with your team' if en else 'Vous suivez et validez l’avancement'}</div><div><strong>{'A dedicated contact' if en else 'Un interlocuteur disponible'}</strong>{'From discovery to delivery' if en else 'Du cadrage à la livraison'}</div></div>
<section id="fonctionnalites" class="sm-section"><div class="sm-wrap"><div class="sm-section-intro"><span class="sm-eyebrow">{'The scope' if en else 'Le périmètre'}</span><h2>{'Built around your needs' if en else 'Conçu autour de vos besoins'}</h2><p>{'Modules and services are selected together and detailed in your proposal.' if en else 'Les modules et prestations sont sélectionnés ensemble et détaillés dans votre devis.'}</p></div><div class="sm-feature-grid">{feature_html}</div></div></section>
<section class="sm-section sm-tinted"><div class="sm-wrap sm-split"><div><span class="sm-eyebrow">{'Your everyday work' if en else 'Votre quotidien'}</span><h2>{'A project grounded in your reality' if en else 'Un projet ancré dans votre réalité'}</h2><p>{esc(d['use'])}</p><a class="sm-text-link" href="{contact}">{'Tell us about your needs' if en else 'Expliquez-nous votre besoin'} ↗</a></div><div><h3>{'What we define together' if en else 'Ce que nous définissons ensemble'}</h3><ul class="sm-deliverables">{''.join('<li>'+esc(x)+'</li>' for x in deliver)}</ul></div></div></section>
<section class="sm-section"><div class="sm-wrap"><span class="sm-eyebrow">{'Our approach' if en else 'Notre méthode'}</span><h2>{'From the first conversation to delivery' if en else 'Du premier échange à la mise en service'}</h2><ol class="sm-steps">{steps_html}</ol></div></section>
<section class="sm-section sm-tinted"><div class="sm-wrap sm-split"><div class="sm-faq"><span class="sm-eyebrow">FAQ</span><h2>{'Your questions, answered' if en else 'Les réponses à vos questions'}</h2>{faqs}</div><aside class="sm-budget"><span class="sm-eyebrow">{'Your project' if en else 'Votre projet'}</span><h2>{'A proposal that fits your scope' if en else 'Un devis adapté à votre périmètre'}</h2><p>{'Cost and timing depend on the features, integrations and deliverables. We distinguish the service fee, optional work and third-party costs before starting.' if en else 'Le prix et le délai dépendent des fonctionnalités, des intégrations et des livrables. Nous distinguons la prestation, les options et les coûts des services tiers avant de commencer.'}</p><a class="cs-button-solid" href="{contact}">{'Request a quote' if en else 'Demander un devis'}</a></aside></div></section>
<section class="sm-section"><div class="sm-wrap"><span class="sm-eyebrow">{'Explore further' if en else 'Pour aller plus loin'}</span><h2>{'Related expertise' if en else 'Des expertises complémentaires'}</h2><div class="sm-related">{related_html}</div></div></section>
</main>'''
        text=replace_element(template,'main',main)
        head=fragment(re.search(r'<head>.*?</head>',text,re.S)[0])
        # lxml wraps a standalone head in html; edit the actual head.
        if head.tag!='head': head=head.find('head')
        for el in head.xpath('.//title|.//link[@rel="canonical" or @rel="alternate"]|.//meta[@name="description" or @name="keywords" or starts-with(@name,"twitter:") or starts-with(@property,"og:")]|.//script[@type="application/ld+json"]'):
            el.getparent().remove(el)
        meta=f'<title>{esc(title)}</title><meta name="description" content="{esc(d["intro"],quote=True)}"><link rel="canonical" href="https://sitemagique.com{pageurl}"><link rel="alternate" hreflang="fr" href="https://sitemagique.com/{slug}/"><link rel="alternate" hreflang="en" href="https://sitemagique.com/en/{slug}/"><link rel="alternate" hreflang="x-default" href="https://sitemagique.com/{slug}/"><meta property="og:title" content="{esc(title,quote=True)}"><meta property="og:description" content="{esc(d["intro"],quote=True)}"><meta property="og:url" content="https://sitemagique.com{pageurl}"><meta property="og:type" content="website"><meta property="og:image" content="https://sitemagique.com{PHOTO}"><meta property="og:locale" content="{"en_GB" if en else "fr_FR"}"><meta name="twitter:card" content="summary_large_image">'
        schema={'@context':'https://schema.org','@type':'Service','name':d['label'],'description':d['intro'],'url':'https://sitemagique.com'+pageurl,'provider':{'@type':'Organization','name':'SITE MAGIQUE','url':'https://sitemagique.com/'}}
        newhead=serial(head).replace('</head>',meta+'<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False)+'</script></head>')
        text=replace_element(text,'head',newhead)
        put(pageurl.lstrip('/')+'index.html',text)

def update_anchor(match,lang):
    raw=match[0]; a=fragment(raw); label=' '.join(a.text_content().split()).lower(); href=a.get('href',''); old=urlsplit(href).path
    target=None
    # Service card destinations are determined by their title, not their old URL.
    title=a.xpath('.//h3'); key=title[0].text_content().lower() if title else label
    if 'application' in key or 'web and mobile apps' in key:target='creation-application'
    elif 'crm' in key:target='crm-gestion'
    elif 'centre' in key and ('appel' in key or 'call-' in key) or 'call-centre' in key:target='centre-appels'
    elif 'plateforme' in key or 'saas' in key or key=='web platforms':target='plateformes-web'
    elif 'logiciel' in key or 'custom software' in key or key=='software':target='logiciels-sur-mesure'
    elif 'google ads' in key:target='google-ads'
    elif 'réseaux sociaux' in key or 'social media advertising' in key:target='publicite-reseaux-sociaux'
    elif 'référencement seo' in key or key=='seo' or (title and key.startswith('seo')):target='seo-services'
    elif 'hébergement' in key or 'hosting' in key:target='hebergement-support'
    elif title and any(x in key for x in ['sites web','landing page','sites vitrines','boutiques en ligne','business websites','online stores','websites &']):target='web-design'
    # Only rewrite local links; contact CTAs should remain contact CTAs.
    if target and not urlsplit(href).netloc and ('cs-link' in a.get('class','') or 'cs-drop-link' in a.get('class','')):
        return re.sub(r'href="[^"]*"',f'href="{url(target,lang)}"',raw,count=1)
    if old in ['/google-ppc-services/','/en/google-ppc-services/']:
        return re.sub(r'href="[^"]*"',f'href="{url("logiciels-sur-mesure",lang)}"',raw,count=1)
    if '/white-label-partnerships/' in href and '#' in href:
        anchors={'crm':'crm-gestion','centre-appels':'centre-appels','plateformes':'plateformes-web'}
        if href.split('#')[-1] in anchors:return re.sub(r'href="[^"]*"',f'href="{url(anchors[href.split("#")[-1]],lang)}"',raw,count=1)
    if '#blog-post' in href:
        return raw.replace('#blog-post','/')
    return raw

for path in ROOT.rglob('*.html'):
    if '.git' in path.parts:continue
    rel=path.relative_to(ROOT); lang='en' if rel.parts[0]=='en' else 'fr'
    text=path.read_text(encoding='utf-8')
    if '<header' not in text:continue
    text=re.sub(r'<base\b[^>]*>','',text)
    text=replace_element(text,'header',NAV[lang]); text=replace_element(text,'footer',FOOTER[lang])
    text=re.sub(r'<a\b[^>]*>.*?</a>',lambda m:update_anchor(m,lang),text,flags=re.S)
    # Only the device photographs shown in the reference are replaced.
    def picture(m):
        if not re.search(r'laptop(?:-m)?\.(?:png|webp)',m[0]):return m[0]
        start=re.match(r'<picture[^>]*>',m[0])[0]
        return start+f'<img src="{PHOTO}" alt="{"Tropical beach beside a wooden villa" if lang=="en" else "Plage tropicale et villa en bois au bord de la mer"}" width="1200" height="2133" decoding="async" loading="lazy"></picture>'
    text=re.sub(r'<picture\b.*?</picture>',picture,text,flags=re.S)
    text=re.sub(r'/assets/js/nav\.js(?:\?[^"\s]*)?',f'/assets/js/nav.js?v={VERSION}',text)
    text=re.sub(r'/assets/css/root\.css(?:\?[^"\s]*)?',f'/assets/css/root.css?v=20261030-cta',text)
    if '/assets/css/services.css' not in text:text=text.replace('</head>',f'<link rel="stylesheet" href="/assets/css/services.css?v={VERSION}"></head>')
    # Normalize internal directory links and remove invalid preload URLs.
    text=re.sub(r'<link\b[^>]*href=""[^>]*>','',text)
    text=re.sub(r'href="(/(?:en/)?contact)"',r'href="\1/"',text)
    text=text.replace('href="g"','href="'+('/en/blog/' if lang=='en' else '/blog/')+'"')
    # A few legacy article images contain a stray src="g".
    text=text.replace('src="g"','src="/assets/images/home-engagement-portrait.png"')
    if str(rel).replace('\\','/') in ['index.html','en/index.html']:
        text=text.replace('>Applications &amp; logiciels</h3>','>Création d’applications</h3>').replace('>Applications & logiciels</h3>','>Création d’applications</h3>').replace('>Applications &amp; software</h3>','>Application development</h3>').replace('>Applications & software</h3>','>Application development</h3>')
    if rel.parent.name=='contact' and '/assets/js/contact-service.js' not in text:
        text=text.replace('</body>',f'<script defer src="/assets/js/contact-service.js?v={VERSION}"></script></body>')
    # Keep the language switch and active navigation accurate for this page.
    page='/'+str(rel.parent).replace('\\','/').strip('.')+'/'
    page=page.replace('//','/')
    frpage=page[3:] if page.startswith('/en/') else page
    enpage='/en'+frpage
    def switch(m):
        block=m[0]
        block=re.sub(r'(<a\b[^>]*href=")[^"]*("[^>]*hreflang="fr")',lambda x:x[1]+frpage+x[2],block)
        block=re.sub(r'(<a\b[^>]*href=")[^"]*("[^>]*hreflang="en")',lambda x:x[1]+enpage+x[2],block)
        return block
    text=re.sub(r'<div class="cs-lang-switcher".*?</div>',switch,text,flags=re.S)
    text=text.replace('class="cs-li-link cs-active"','class="cs-li-link"')
    if not text.lstrip().lower().startswith('<!doctype'):text='<!DOCTYPE html>\n'+text
    path.write_text(text,encoding='utf-8')

# The legacy software URL stays usable for bookmarks, with the new canonical page.
for lang in ['fr','en']:
    text=document(url('logiciels-sur-mesure',lang).lstrip('/')+'index.html')
    destination=url('logiciels-sur-mesure',lang)
    text=text.replace('</head>',f'<meta http-equiv="refresh" content="0;url={destination}"></head>')
    put(url('google-ppc-services',lang).lstrip('/')+'index.html',text)

pages=[]
for path in ROOT.rglob('index.html'):
    if '.git' in path.parts or 'google-ppc-services' in path.parts:continue
    rel=path.parent.relative_to(ROOT).as_posix()
    page='/' if rel=='.' else '/'+rel+'/'
    pages.append('https://sitemagique.com'+page)
put('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('<url><loc>'+x+'</loc></url>\n' for x in sorted(pages))+'</urlset>\n')
print(f'Generated {len(DATA)*2} service pages; shared navigation, images and links updated.')
import runpy
runpy.run_path(str(ROOT/'scripts/service-designs.py'))
