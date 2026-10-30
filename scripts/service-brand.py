"""Apply the shared title banner and reliable favicon declarations."""
from pathlib import Path
from copy import deepcopy
from lxml import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT/'scripts/service-content.json').read_text(encoding='utf-8'))
template = html.parse(str(ROOT/'web-design/index.html')).getroot().get_element_by_id('banner-1519')
for item in data:
    for lang in ('fr', 'en'):
        p = ROOT/('en' if lang == 'en' else '')/item['slug']/'index.html'
        d = html.document_fromstring(p.read_text(encoding='utf-8'))
        main = d.get_element_by_id('main')
        if item['slug'] == 'logiciels-sur-mesure':
            for crumb in main.xpath('.//nav[@class="sm-breadcrumb"]'):
                crumb.getparent().remove(crumb)
        for old in main.xpath('./div[@id="banner-1519"]'):
            main.remove(old)
        banner = deepcopy(template)
        banner.xpath('.//span[@class="cs-int-title"]')[0].text = item[lang]['label']
        main.insert(0, banner)
        p.write_text('<!DOCTYPE html>\n'+html.tostring(d, encoding='unicode', method='html'), encoding='utf-8')

icons = '<link rel="icon" type="image/x-icon" href="/favicon.ico?v=20261030"><link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png?v=20261030"><link rel="apple-touch-icon" sizes="180x180" href="/assets/favicons/apple-touch-icon.png?v=20261030">'
for p in ROOT.rglob('*.html'):
    s = p.read_text(encoding='utf-8')
    s = re.sub(r'<link\b(?=[^>]*\brel=["\'][^"\']*icon[^"\']*["\'])[^>]*>', '', s)
    s = s.replace('</head>', icons+'</head>')
    s = re.sub(r'(/assets/css/service-themes\.css)(?:\?[^"\s<>]*)?', r'\1?v=20261030-brand', s)
    p.write_text(s, encoding='utf-8')
print('Shared banners, typography asset version and favicon declarations updated.')
