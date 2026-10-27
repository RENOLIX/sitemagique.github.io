(() => {
  const header = document.getElementById('cs-navigation');
  const toggle = header?.querySelector('.cs-toggle');
  if (!header || !toggle) return;
  const list = header.querySelector('#cs-expanded');
  const setMenu = open => {
    header.classList.toggle('cs-active', open);
    toggle.classList.toggle('cs-active', open);
    document.body.classList.toggle('cs-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    list?.setAttribute('aria-expanded', String(open));
  };
  toggle.setAttribute('aria-controls', 'cs-expanded');
  setMenu(false);
  toggle.addEventListener('click', () => setMenu(!header.classList.contains('cs-active')));
  const dropdowns = [...header.querySelectorAll('.cs-dropdown')];
  const closeDropdown = item => {
    item.classList.remove('cs-active');
    item.querySelector('.sm-menu-trigger')?.setAttribute('aria-expanded', 'false');
  };
  dropdowns.forEach((item, index) => {
    const button = item.querySelector('.sm-menu-trigger');
    const panel = item.querySelector('.cs-drop-ul');
    if (!button || !panel) return;
    panel.id = `sm-dropdown-${index}`;
    button.setAttribute('aria-controls', panel.id);
    button.setAttribute('aria-expanded', 'false');
    button.addEventListener('click', () => {
      const open = !item.classList.contains('cs-active');
      dropdowns.forEach(closeDropdown);
      item.classList.toggle('cs-active', open);
      button.setAttribute('aria-expanded', String(open));
    });
    item.addEventListener('focusout', e => { if (!item.contains(e.relatedTarget)) closeDropdown(item); });
    item.addEventListener('keydown', e => {
      if (e.key === 'Escape') { e.stopPropagation(); closeDropdown(item); button.focus(); }
    });
  });
  document.addEventListener('click', e => {
    if (!header.contains(e.target)) { dropdowns.forEach(closeDropdown); setMenu(false); }
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && header.classList.contains('cs-active')) { setMenu(false); toggle.focus(); }
  });
  header.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  window.matchMedia('(min-width:64rem)').addEventListener('change', () => { setMenu(false); dropdowns.forEach(closeDropdown); });
})();
