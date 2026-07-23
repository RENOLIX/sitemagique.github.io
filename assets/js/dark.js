(() => {
  const body = document.body;
  const toggle = document.querySelector('#dark-mode-toggle');
  const storedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  if (storedTheme === 'dark' || (!storedTheme && prefersDark)) body.classList.add('dark-mode');
  toggle?.addEventListener('click', () => {
    const enabled = body.classList.toggle('dark-mode');
    localStorage.setItem('theme', enabled ? 'dark' : 'light');
    toggle.setAttribute('aria-pressed', String(enabled));
  });
})();
