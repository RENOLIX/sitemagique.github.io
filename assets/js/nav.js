(() => {
  const navigation = document.querySelector('#cs-navigation');
  const toggle = navigation?.querySelector('.cs-toggle');
  const menu = navigation?.querySelector('#cs-expanded');
  const closeMenu = () => {
    navigation?.classList.remove('cs-active');
    toggle?.classList.remove('cs-active');
    toggle?.setAttribute('aria-expanded', 'false');
    menu?.setAttribute('aria-expanded', 'false');
  };
  toggle?.addEventListener('click', () => {
    const open = !navigation.classList.contains('cs-active');
    navigation.classList.toggle('cs-active', open);
    toggle.classList.toggle('cs-active', open);
    toggle.setAttribute('aria-expanded', String(open));
    menu?.setAttribute('aria-expanded', String(open));
  });
  navigation?.querySelectorAll('.cs-dropdown > .cs-li-link').forEach((item) => {
    item.addEventListener('click', (event) => {
      if (window.matchMedia('(max-width: 63.9375rem)').matches) {
        event.preventDefault();
        item.parentElement?.classList.toggle('cs-active');
      }
    });
  });
  navigation?.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
})();
