(() => {
  const header = document.getElementById('cs-navigation');
  if (!header) return;

  const updateHeader = () => {
    const isScrolled = window.scrollY >= 100;
    document.body.classList.toggle('scroll', isScrolled);
    header.classList.toggle('is-scrolled', isScrolled);
  };

  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });
})();
