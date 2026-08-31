
(() => {
  const init = () => {
    const section = document.getElementById('tech-stack-showcase');
    if (!section || section.dataset.enhanced === 'true') return;
    section.dataset.enhanced = 'true';
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const targets = [...section.querySelectorAll('[data-tech-reveal], [data-tech-word-reveal]')];
    if (reduced || !('IntersectionObserver' in window)) {
      targets.forEach((node) => node.classList.add('is-visible'));
      return;
    }
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
    targets.forEach((node) => observer.observe(node));
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
