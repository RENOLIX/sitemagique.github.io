
(() => {
  const init = () => {
    const section = document.getElementById('tech-stack-showcase');
    if (!section || section.dataset.avReady === 'true') return;
    section.dataset.avReady = 'true';
    const copy = section.querySelector('[data-av-copy]');
    const meta = section.querySelector('[data-av-meta]');
    const story = section.querySelector('.sm-av-story');
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
    const range = (value, start, end) => clamp((value - start) / (end - start), 0, 1);
    const updateStory = () => {
      if (reduced) return;
      const rect = story.getBoundingClientRect();
      const travel = Math.max(1, story.offsetHeight - window.innerHeight);
      const progress = clamp(-rect.top / travel, 0, 1);
      const copyProgress = range(progress, .02, .27);
      const metaProgress = range(progress, .16, .43);
      copy.style.opacity = copyProgress;
      copy.style.filter = 'blur(' + ((1 - copyProgress) * 20) + 'px)';
      copy.style.transform = 'translateY(' + ((1 - copyProgress) * 10) + '%)';
      meta.style.opacity = metaProgress;
      meta.style.filter = 'blur(' + ((1 - metaProgress) * 20) + 'px)';
      meta.style.transform = 'translateY(' + ((1 - metaProgress) * 20) + '%)';
    };
    if (reduced) {
      copy.style.opacity = meta.style.opacity = 1;
      copy.style.filter = meta.style.filter = 'none';
      copy.style.transform = meta.style.transform = 'none';
    } else {
      let ticking = false;
      const requestUpdate = () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(() => { updateStory(); ticking = false; });
      };
      window.addEventListener('scroll', requestUpdate, { passive: true });
      window.addEventListener('resize', requestUpdate, { passive: true });
      updateStory();
    }
    const revealItems = [...section.querySelectorAll('[data-av-reveal]')];
    if (reduced || !('IntersectionObserver' in window)) {
      revealItems.forEach((item) => item.classList.add('is-visible'));
      return;
    }
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { threshold: .16, rootMargin: '0px 0px -8% 0px' });
    revealItems.forEach((item) => observer.observe(item));
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
