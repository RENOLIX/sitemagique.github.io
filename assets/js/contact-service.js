(() => {
  const en = document.documentElement.lang === 'en';
  const services = {
    'creation-application': ['Création d’applications', 'Application development'],
    'plateformes-web': ['Plateformes web & SaaS', 'Web platforms & SaaS'],
    'crm-gestion': ['CRM & gestion commerciale', 'CRM & business management'],
    'centre-appels': ['Solutions pour centres d’appels', 'Call-centre solutions'],
    'logiciels-sur-mesure': ['Logiciels sur mesure', 'Custom software'],
    'google-ads': ['Google Ads', 'Google Ads'],
    'publicite-reseaux-sociaux': ['Publicité sur les réseaux sociaux', 'Social media advertising'],
    'hebergement-support': ['Hébergement & support', 'Hosting & support']
  };
  const selected = services[new URLSearchParams(location.search).get('service')];
  if (!selected) return;
  const label = selected[en ? 1 : 0];
  const heading = document.querySelector('main h2');
  if (heading) {
    const note = document.createElement('p');
    note.className = 'cs-text';
    note.textContent = (en ? 'Your project: ' : 'Votre projet : ') + label;
    heading.after(note);
  }
  const message = en ? `Hello SITE MAGIQUE, I would like to discuss a project: ${label}.` : `Bonjour SITE MAGIQUE, je souhaite échanger sur un projet : ${label}.`;
  document.querySelectorAll('main a[href^="https://wa.me/"]').forEach(a => {
    const link = new URL(a.href); link.searchParams.set('text', message); a.href = link.toString();
  });
  document.querySelectorAll('main a[href^="mailto:"]').forEach(a => {
    a.href = 'mailto:contact@sitemagique.com?subject=' + encodeURIComponent((en ? 'Project: ' : 'Projet : ') + label) + '&body=' + encodeURIComponent(message);
  });
})();
