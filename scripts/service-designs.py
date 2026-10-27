"""Distinct editorial layouts and illustrative interfaces for each service."""
from pathlib import Path
from lxml import html
from html import escape
import json
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'scripts/service-content.json').read_text(encoding='utf-8'))

def render(el):return html.tostring(el,encoding='unicode',method='html',with_tail=False)
def panel(title,body,cls=''):
    return f'<div class="studio-panel {cls}"><div class="studio-bar"><span class="studio-dots" aria-hidden="true">● ● ●</span><span>{title}</span><span aria-hidden="true">↗</span></div>{body}</div>'
def build(slug,en):
    t=lambda fr,eng:eng if en else fr
    if slug=='creation-application':
        return f'''<div class="app-scene"><div class="app-orbit orbit-one"></div><div class="app-orbit orbit-two"></div><span class="app-note">{t('UNE IDÉE. MILLE POSSIBILITÉS.','ONE IDEA. ENDLESS POSSIBILITIES.')}</span><div class="app-phone"><div class="phone-camera"></div><div class="phone-top">9:41 <span>● ▰</span></div><div class="app-avatar">M<span>✦</span></div><small>{t('Bonjour, Maya','Hello, Maya')}</small><h3>{t('Tout commence<br>avec vous.','It all starts<br>with you.')}</h3><div class="app-tile"><span>✧</span><b>{t('Votre espace','Your space')}</b><small>{t('Simple. Personnel. Connecté.','Simple. Personal. Connected.')}</small><div class="app-progress"><i></i></div></div><div class="app-mini-grid"><div>◷<small>{t('Planning','Schedule')}</small></div><div>◎<small>{t('Activité','Activity')}</small></div></div><div class="phone-nav">⌂ <span>⊕</span> ◉</div></div><div class="app-floating"><span>✓</span><div><b>{t('Pensé pour le mobile','Designed for mobile')}</b><small>iOS · Android · Web</small></div></div></div>'''
    if slug=='plateformes-web':
        return panel('WORKSPACE / SITE MAGIQUE',f'''<div class="platform-shell"><aside><b>◈</b><span>{t('Vue générale','Overview')}</span><span>{t('Espaces','Spaces')}</span><span>{t('Membres','Members')}</span><span>{t('Paramètres','Settings')}</span></aside><div class="platform-board"><div class="board-heading"><div><small>{t('VOTRE ÉCOSYSTÈME','YOUR ECOSYSTEM')}</small><h3>{t('Chaque service,<br>à sa place.','Every service,<br>in its place.')}</h3></div><span class="status-pill">● {t('Connecté','Connected')}</span></div><div class="platform-modules"><div>▦<b>{t('Portail client','Client portal')}</b><small>{t('Documents & échanges','Documents & conversations')}</small></div><div>◇<b>Marketplace</b><small>{t('Offres & commandes','Offers & orders')}</small></div><div>◷<b>{t('Réservations','Bookings')}</b><small>{t('Planning & disponibilités','Schedules & availability')}</small></div></div><div class="integration-line">API <i></i> {t('Votre plateforme','Your platform')} <i></i> {t('Vos outils','Your tools')}</div></div></div>''')
    if slug=='crm-gestion':
        columns=[(t('À contacter','To contact'),['Studio Atlas','Maison Nova']),(t('En discussion','In progress'),['Projet Horizon']),(t('Proposition','Proposal'),['Atelier Amana'])]
        cards=''.join('<div class="kanban-column"><h4>'+label+' <span>'+str(len(names))+'</span></h4>'+''.join(f'<div class="deal-card"><span class="deal-tag">{t("OPPORTUNITÉ","OPPORTUNITY")}</span><b>{n}</b><small>{t("Prochaine action planifiée","Next action scheduled")}</small><div><span class="deal-avatar">{n[0]}</span><span>→</span></div></div>' for n in names)+'</div>' for label,names in columns)
        return panel(t('PIPELINE COMMERCIAL','SALES PIPELINE'),f'<div class="crm-toolbar"><h3>{t("Une relation.<br>Un suivi clair.","One relationship.<br>A clear next step.")}</h3><span class="crm-add">+ {t("Prospect","Lead")}</span></div><div class="kanban">{cards}</div><div class="crm-bottom">✓ {t("Clients, échanges et relances réunis.","Customers, conversations and follow-ups together.")}</div>')
    if slug=='centre-appels':
        return f'''<div class="call-scene"><div class="call-status"><i></i>{t('L’ESPACE DE VOS AGENTS','YOUR AGENT WORKSPACE')}</div><div class="sound-wave" aria-hidden="true">{''.join(f'<i style="--h:{v}%"></i>' for v in [14,28,45,26,64,89,46,100,72,35,62,90,40,24,57,82,45,28,13])}</div><div class="call-console"><div class="call-person"><span>SA</span><div><small>{t('FICHE CONTACT','CONTACT RECORD')}</small><h3>Samir A.</h3><p>{t('Campagne de prise de rendez-vous','Appointment booking campaign')}</p></div></div><div class="call-fields"><div><small>{t('PROCHAINE ÉTAPE','NEXT STEP')}</small><b>{t('Qualifier le besoin','Qualify the request')}</b></div><div><small>{t('SCRIPT AGENT','AGENT SCRIPT')}</small><b>{t('Écouter. Comprendre. Orienter.','Listen. Understand. Guide.')}</b></div></div><div class="call-actions"><span>◷ {t('Rappel','Callback')}</span><span>✓ {t('Qualification','Outcome')}</span><span>↗ {t('Suivi','Follow-up')}</span></div></div></div>'''
    if slug=='logiciels-sur-mesure':
        return f'''<div class="software-blueprint"><span class="blueprint-label">SYSTEM DESIGN / 01</span><div class="flow-node flow-input"><small>01 / INPUT</small><b>{t('Vos données','Your data')}</b><span>CSV · API · {t('Formulaires','Forms')}</span></div><div class="flow-line" aria-hidden="true">↓</div><div class="flow-node flow-engine"><small>02 / LOGIC</small><b>{t('Vos règles métier','Your business rules')}</b><code>if (validated) {{<br>&nbsp; automate(workflow);<br>}}</code></div><div class="flow-line" aria-hidden="true">↓</div><div class="flow-output"><div class="flow-node"><small>03 / OUTPUT</small><b>{t('Actions','Actions')}</b></div><div class="flow-node"><small>04 / INSIGHTS</small><b>{t('Rapports','Reports')}</b></div></div><span class="blueprint-foot">{t('UNE ARCHITECTURE À VOTRE MESURE','ARCHITECTURE BUILT AROUND YOU')}</span></div>'''
    if slug=='google-ads':
        return f'''<div class="ads-scene"><div class="search-box"><span>⌕</span>{t('Le service que votre client recherche','The service your customer is looking for')}<span>↵</span></div><div class="search-result"><small>{t('Sponsorisé · exemple d’annonce','Sponsored · illustrative ad')}</small><span>votre-entreprise.com</span><h3>{t('Votre offre. Au bon moment.','Your offer. At the right moment.')}</h3><p>{t('Une réponse claire à un besoin précis. Une page dédiée pour passer à l’action.','A clear answer to a specific need. A dedicated page for the next step.')}</p><div>{t('Découvrir l’offre','Explore the offer')} ↗</div></div><div class="ads-route"><span>01<br><b>{t('Recherche','Search')}</b></span><i>→</i><span>02<br><b>{t('Annonce','Ad')}</b></span><i>→</i><span>03<br><b>{t('Conversion','Conversion')}</b></span></div></div>'''
    if slug=='publicite-reseaux-sociaux':
        return f'''<div class="social-scene"><div class="social-poster poster-back"><small>STORY / 01</small><b>{t('FAITES<br>PARLER<br>DE VOUS.','MAKE<br>YOURSELF<br>KNOWN.')}</b><span>✳</span></div><div class="social-poster poster-front"><div class="social-profile"><i>m</i> {t('votre.marque','your.brand')} <span>•••</span></div><div class="social-art"><span>{t('UNE IDÉE<br>QUI RESTE.','AN IDEA<br>THAT STAYS.')}</span><i>✦</i></div><div class="social-reactions">♡ &nbsp; ◯ &nbsp; ↗ <span>▱</span></div><p>{t('Un message juste.<br>Un format qui vous ressemble.','The right message.<br>A format that feels like you.')}</p></div><div class="social-sticker">{t('CRÉER.<br>TESTER.<br>AJUSTER.','CREATE.<br>TEST.<br>REFINE.')}</div></div>'''
    return f'''<div class="hosting-scene"><div class="hosting-orbit"><span>✦</span><div class="hosting-core">◈<b>SITE MAGIQUE</b><small>{t('À VOS CÔTÉS','BY YOUR SIDE')}</small></div></div><div class="hosting-stack"><div><span class="status-dot"></span><b>HTTPS</b><small>{t('Connexion sécurisée','Secure connection')}</small><span>✓</span></div><div><span class="status-dot"></span><b>{t('Hébergement','Hosting')}</b><small>{t('Votre projet en ligne','Your project online')}</small><span>✓</span></div><div><span class="status-dot"></span><b>Support</b><small>{t('Un interlocuteur identifié','A dedicated contact')}</small><span>↗</span></div></div></div>'''

themes={
'creation-application':('app','De l’idée à l’écran.','From idea to screen.','Les expériences que nous créons','The experiences we build'),
'plateformes-web':('platform','Votre écosystème digital.','Your digital ecosystem.','Les briques de votre plateforme','Your platform’s building blocks'),
'crm-gestion':('crm','Moins de dispersion. Plus de relation.','Less scattered work. Stronger relationships.','Tout le cycle client, connecté','Your entire customer cycle, connected'),
'centre-appels':('call','L’humain au bout du fil.','People at the other end.','Chaque étape de la conversation','Every stage of the conversation'),
'logiciels-sur-mesure':('software','Votre métier. Vos règles. Votre outil.','Your business. Your rules. Your tool.','De vos processus à votre logiciel','From processes to software'),
'google-ads':('ads','La bonne recherche. La bonne rencontre.','The right search. The right connection.','Un parcours orienté conversion','A conversion-focused journey'),
'publicite-reseaux-sociaux':('social','Votre marque mérite d’être remarquée.','Your brand deserves attention.','Une campagne, plusieurs leviers','One campaign, several opportunities'),
'hebergement-support':('hosting','En ligne. Et bien accompagné.','Online. And supported.','La continuité de votre projet','Continuity for your project')}

for item in DATA:
 slug=item['slug']; theme,frtitle,entitle,frfeatures,enfeatures=themes[slug]
 for lang in ['fr','en']:
    en=lang=='en'; path=ROOT/('en' if en else '')/slug/'index.html'; d=html.document_fromstring(path.read_text(encoding='utf-8'))
    main=d.get_element_by_id('main'); main.set('class','sm-service theme-'+theme)
    main.xpath('.//h1')[0].text=entitle if en else frtitle
    old=main.xpath('.//figure[contains(@class,"sm-service-visual")]|.//div[contains(@class,"service-art")]')[0]
    art=html.fromstring('<div class="service-art" role="img" aria-label="'+escape(item[lang]['label']+' — '+('illustrative interface' if en else 'illustration de fonctionnement'),quote=True)+'">'+build(slug,en)+'<span class="art-caption">'+('Illustration of the service · not a live account' if en else 'Illustration du service · interface de présentation')+'</span></div>')
    old.getparent().replace(old,art)
    features=main.get_element_by_id('fonctionnalites'); features.xpath('.//h2')[0].text=enfeatures if en else frfeatures
    features.set('class','sm-section feature-'+theme)
    # Each page has its own reading order, not just different colours.
    use=main.xpath('./section')[2]; method=main.xpath('./section')[3]; faq=main.xpath('./section')[4]
    if theme in ['software','call']:main.remove(use); main.insert(2,use)
    if theme=='hosting':main.remove(faq); main.insert(3,faq)
    if theme=='social':main.remove(method); main.insert(3,method)
    # Meaningful feature accents and vocabulary specific to the service.
    icons={'app':['◉','▣','✦','◎','↗','⊕'],'platform':['01','02','03','04','05','06'],'crm':['CONTACTS','PIPELINE','ACTIONS','VENTES' if not en else 'SALES','ÉQUIPE' if not en else 'TEAM','DATA'],'call':['01 / AGENT','02 / CAMPAGNE' if not en else '02 / CAMPAIGN','03 / LEADS','04 / SUIVI' if not en else '04 / FOLLOW-UP','05 / MANAGER','06 / API'],'software':['INPUT','PROCESS','AUTOMATE','CONNECT','CONTROL','DELIVER'],'ads':['CIBLER' if not en else 'TARGET','STRUCTURER' if not en else 'STRUCTURE','CONVAINCRE' if not en else 'PERSUADE','CONVERTIR' if not en else 'CONVERT','MESURER' if not en else 'MEASURE','OPTIMISER' if not en else 'OPTIMISE'],'social':['01 ✳','02 ↗','03 ✦','04 ◎','05 →','06 ⊕'],'hosting':['↗','◇','▤','◉','✓','⊕']}
    for i,el in enumerate(features.xpath('.//span[@class="sm-feature-number"]')):el.text=icons[theme][i]
    if not d.xpath('//link[contains(@href,"service-themes.css")]'):
      link=html.Element('link',rel='stylesheet',href='/assets/css/service-themes.css?v=20261027-2'); d.find('head').append(link)
    for el in d.xpath('//meta[@property="og:image" or @name="twitter:image"]'):el.set('content','https://sitemagique.com/assets/images/site-magique-logo.png')
    path.write_text('<!DOCTYPE html>\n'+render(d),encoding='utf-8')
print('Applied 8 distinct art directions, layouts and service illustrations in French and English.')
