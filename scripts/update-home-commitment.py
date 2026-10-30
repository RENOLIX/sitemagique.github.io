"""Replace only the homepage commitment section, retaining its original portrait."""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
CSS = '<link rel="stylesheet" href="/assets/css/home-commitment.css?v=20261030-1">'

ICONS = {
    'hosting': '<rect x="3" y="3" width="18" height="7" rx="2"/><rect x="3" y="14" width="18" height="7" rx="2"/><path d="M7 6.5h.01M7 17.5h.01M16 6.5h2M16 17.5h2"/>',
    'shield': '<path d="M12 3 4 6v6c0 5 8 9 8 9s8-4 8-9V6l-8-3Z"/><path d="m8.5 11.5 2.5 2.5 4.5-5"/>',
    'support': '<path d="M4 13v-2a8 8 0 0 1 16 0v2M4 12H3v6h4v-6H4ZM20 12h1v6h-4v-6h3ZM20 18c0 3-3 3-6 3"/>',
    'payment': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18M7 15h4"/>',
    'check': '<path d="m6 12 4 4 8-9"/>',
}

def icon(name):
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+ICONS[name]+'</svg>'

for en in (False, True):
    t = lambda fr, eng: eng if en else fr
    p = ROOT/('en/index.html' if en else 'index.html')
    text = p.read_text(encoding='utf-8')
    benefits = [
        ('hosting', t('Hébergement gratuit à vie', 'Free lifetime hosting'), t('Votre site reste hébergé, sans frais d’hébergement supplémentaires.', 'Your website stays hosted, with no additional hosting fees.')),
        ('shield', t('Garantie à vie', 'Lifetime guarantee'), t('Un accompagnement durable pour la continuité de votre solution.', 'Long-term support for the continuity of your solution.')),
        ('support', t('Support 24h/24 et 7j/7', '24/7 support'), t('Un interlocuteur disponible, où que vous soyez.', 'A dedicated contact, wherever you are.')),
        ('payment', t('Paiements flexibles', 'Flexible payments'), t('Plusieurs moyens de paiement pour travailler simplement à distance.', 'Several payment methods to make remote collaboration simple.')),
    ]
    cards = ''.join('<li class="sm-commit-benefit"><span class="sm-commit-icon">'+icon(key)+'</span><div><h4>'+escape(title)+'</h4><p>'+escape(body)+'</p></div></li>' for key, title, body in benefits)
    section = f'''<section id="sbs-1362" class="sm-commitment" aria-labelledby="sm-commitment-title">
<div class="sm-commit-wrap">
<div class="sm-commit-heading"><div><span class="sm-commit-eyebrow">{t('Notre engagement', 'Our commitment')}</span><h2 id="sm-commitment-title" class="sm-commit-title">{t('Votre projet, livré<br>avec confiance.', 'Your project, delivered<br>with confidence.')}</h2></div><p>{t('Depuis 2016 à Alger, nous transformons vos idées en solutions digitales. Plus de 1 000 projets réalisés, avec une conviction : vous accompagner aussi sérieusement que nous créons.', 'Founded in Algiers in 2016, we turn your ideas into digital solutions. With more than 1,000 projects delivered, we put the same care into supporting you as we do into creating your project.')}</p></div>
<div class="sm-commit-panel">
<figure class="sm-commit-portrait"><div class="sm-commit-photo"><span class="sm-commit-photo-label">SITE MAGIQUE <span>· {t('Depuis 2016', 'Since 2016')}</span></span><img src="/assets/images/home-engagement-portrait.png?v=1" alt="{t('Portrait illustré de MOUHAMMOU ABDELGHANI', 'Illustrated portrait of MOUHAMMOU ABDELGHANI')}" width="941" height="1672" loading="lazy" decoding="async"></div><figcaption><img src="/assets/images/site-magique-symbol.png" alt="" width="42" height="42" loading="lazy" decoding="async"><div><strong>MOUHAMMOU ABDELGHANI</strong><span>{t('Fondateur et dirigeant', 'Founder and director')}</span></div></figcaption></figure>
<div class="sm-commit-details">
<div class="sm-commit-promise"><span class="sm-commit-promise-icon">{icon('check')}</span><div><span class="sm-commit-kicker">{t('Paiement après réalisation', 'Payment after delivery')}</span><h3>{t('Vous validez le résultat.<br>Vous payez ensuite.', 'You approve the result.<br>Then you pay.')}</h3><p>{t('Vous découvrez votre projet et validez sa réalisation avant de le régler. Une collaboration claire, dès le premier échange.', 'Review your project and approve the work before paying. A clear collaboration, right from our first conversation.')}</p></div></div>
<ul class="sm-commit-benefits">{cards}</ul>
<div class="sm-commit-bottom"><div><span class="sm-commit-kicker">{t('À chaque idée, sa solution', 'A solution for every idea')}</span><p>{t('Sites web · Boutiques · Applications<br>Logiciels · Plateformes', 'Websites · Stores · Applications<br>Software · Platforms')}</p></div><a class="cs-button-solid" href="{'/en/contact/' if en else '/contact/'}">{t('Parlons de votre projet', 'Let’s discuss your project')}<span aria-hidden="true"> ↗</span></a></div>
</div></div></div></section>'''
    updated, count = re.subn(r'<section\b(?=[^>]*\bid="sbs-1362")[^>]*>.*?</section>', lambda _: section, text, flags=re.S)
    if count != 1:
        raise ValueError(f'{p}: expected exactly one commitment section, found {count}')
    if '/assets/css/home-commitment.css' not in updated:
        updated = updated.replace('</head>', CSS+'</head>')
    p.write_text(updated, encoding='utf-8')
print('Homepage commitment section replaced in French and English.')
