/* ══════════════════════════════════════════════════════════════════════
   Abou Camara — shared interaction layer
   Every block is guarded, so the same file runs on every page.
   ══════════════════════════════════════════════════════════════════════ */
(() => {
  'use strict';

  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.documentElement.classList.remove('no-js');

  /* ── year ──────────────────────────────────────────────────────────── */
  $$('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });

  /* ── sticky nav ────────────────────────────────────────────────────── */
  const hdr = $('#hdr');
  if (hdr) {
    const stick = () => hdr.classList.toggle('stuck', scrollY > 24);
    stick();
    addEventListener('scroll', stick, { passive: true });
  }

  /* ── desktop dropdowns: Escape closes the open panel ───────────────── */
  $$('.menu > li').forEach(li => {
    if (!$('.drop', li)) return;
    li.addEventListener('keydown', e => {
      if (e.key !== 'Escape') return;
      li.classList.add('closed');
      $('a', li).focus();
    });
    const reset = () => li.classList.remove('closed');
    li.addEventListener('mouseleave', reset);
    li.addEventListener('focusout', e => { if (!li.contains(e.relatedTarget)) reset(); });
  });

  /* ── mobile menu ───────────────────────────────────────────────────── */
  const burger = $('#burger');
  const mnav   = $('#mnav');
  if (burger && mnav) {
    const close = $('#mnav-close');
    const set = open => {
      mnav.classList.toggle('open', open);
      mnav.setAttribute('aria-hidden', String(!open));
      mnav.inert = !open;
      burger.setAttribute('aria-expanded', String(open));
      document.body.classList.toggle('locked', open);
      (open ? close : burger).focus();
    };
    mnav.inert = true;
    burger.addEventListener('click', () => set(true));
    close.addEventListener('click', () => set(false));
    mnav.addEventListener('keydown', e => { if (e.key === 'Escape') set(false); });
    $$('a', mnav).forEach(a => a.addEventListener('click', () => set(false)));
    matchMedia('(min-width: 1080px)').addEventListener('change', e => {
      if (e.matches && mnav.classList.contains('open')) set(false);
    });
  }

  /* ── hero line reveal ──────────────────────────────────────────────── */
  const lines = $('.lines');
  if (lines) requestAnimationFrame(() => lines.classList.add('go'));

  /* ── reveal on scroll ──────────────────────────────────────────────── */
  const targets = $$('.rv');
  if (targets.length) {
    if (calm || !('IntersectionObserver' in window)) {
      targets.forEach(el => el.classList.add('on'));
    } else {
      const io = new IntersectionObserver((entries, obs) => {
        entries.forEach((en, i) => {
          if (!en.isIntersecting) return;
          en.target.style.transitionDelay = Math.min(i * 80, 240) + 'ms';
          en.target.classList.add('on');
          obs.unobserve(en.target);
        });
      }, { threshold: .08, rootMargin: '0px 0px -40px 0px' });
      targets.forEach(el => io.observe(el));
    }
  }

  /* ── filters (projects, certifications) ────────────────────────────────
     <div data-filter-bar="grid-id"> buttons with data-filter="all|key"
     items inside #grid-id carry data-cats="key other-key"                  */
  $$('[data-filter-bar]').forEach(bar => {
    const grid    = document.getElementById(bar.dataset.filterBar);
    if (!grid) return;
    const buttons = $$('button[data-filter]', bar);
    const items   = $$('[data-cats]', grid);
    const empty   = $('.empty-note', grid.parentElement);
    const count   = $('[data-filter-count]');
    buttons.forEach(btn => btn.addEventListener('click', () => {
      buttons.forEach(b => b.setAttribute('aria-pressed', String(b === btn)));
      const f = btn.dataset.filter;
      let shown = 0;
      items.forEach(it => {
        const show = f === 'all' || it.dataset.cats.split(' ').includes(f);
        it.classList.toggle('hide', !show);
        if (show) { shown++; it.classList.add('on'); }
      });
      if (empty) empty.style.display = shown ? 'none' : 'block';
      if (count) {
        const unit = count.dataset.unit || 'item';
        count.textContent = shown + ' ' + unit + (shown === 1 ? '' : 's');
      }
    }));
  });

  /* ── contact form → pre-filled email, no server needed ─────────────── */
  const form = $('#cf');
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      const d = new FormData(form);
      const body = [
        'Name: '    + d.get('name'),
        'Email: '   + d.get('email'),
        'Subject: ' + d.get('subject'),
        'Budget: '  + d.get('budget'),
        '',
        d.get('message')
      ].join('\n');
      const ok = $('#ok');
      if (ok) ok.style.display = 'block';
      location.href = 'mailto:aboucamara1107@gmail.com'
        + '?subject=' + encodeURIComponent('New project: ' + d.get('name'))
        + '&body='    + encodeURIComponent(body);
    });
  }
})();
