(() => {
  document.querySelectorAll('.cs-faq-item .cs-button').forEach((button) => {
    button.addEventListener('click', () => {
      const item = button.closest('.cs-faq-item');
      const wasOpen = item?.classList.contains('active');
      item?.parentElement?.querySelectorAll('.cs-faq-item.active').forEach((openItem) => {
        openItem.classList.remove('active');
      });
      if (!wasOpen) item?.classList.add('active');
      button.setAttribute('aria-expanded', String(!wasOpen));
    });
  });

  document.querySelectorAll('[data-filter]').forEach((filter) => {
    filter.addEventListener('click', () => {
      const target = filter.getAttribute('data-filter');
      document.querySelectorAll('.cs-faq-group').forEach((group) => {
        group.classList.toggle('cs-hidden', target !== 'all' && group.id !== target);
      });
    });
  });
})();
