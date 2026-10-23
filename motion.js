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
          // stagger elements that appear together, then drop the delay so later
          // transitions (hover, filters) are not held back by it
          en.target.style.transitionDelay = Math.min(i * 80, 240) + 'ms';
          en.target.addEventListener('transitionend', () => { en.target.style.transitionDelay = ''; }, { once: true });
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

  /* ── contact form → Make webhook (Google Sheet), email as fallback ── */
  const form = $('#cf');
  if (form) {
    const ok  = $('#ok');
    const err = $('#err');
    const btn = form.querySelector('button[type="submit"]');
    const label = btn ? btn.innerHTML : '';
    const openedAt = Date.now();

    const mailto = d => 'mailto:aboucamara1107@gmail.com'
      + '?subject=' + encodeURIComponent('New project: ' + d.get('name'))
      + '&body='    + encodeURIComponent([
        'Name: '    + d.get('name'),
        'Email: '   + d.get('email'),
        'Subject: ' + d.get('subject'),
        'Budget: '  + d.get('budget'),
        '',
        d.get('message')
      ].join('\n'));

    form.addEventListener('submit', async e => {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      const d = new FormData(form);
      // Only bots fill the honeypot; leave it out otherwise so the scenario's "does not exist" filter passes.
      if (!d.get('website')) d.delete('website');
      // Bot checks, verified by the Make scenario: a key only this script adds,
      // and the time since the page opened (bots submit almost instantly).
      d.append('k', 'site-v1');
      d.append('t', String(Date.now() - openedAt));
      d.append('lang', document.documentElement.lang || 'en');
      d.append('page', location.href);
      if (ok)  ok.style.display  = 'none';
      if (err) err.style.display = 'none';
      if (btn) { btn.disabled = true; btn.textContent = form.dataset.sending || 'Sending…'; }

      // URL-encoded body keeps this a "simple" CORS request: no preflight.
      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), 15000);
      try {
        const res = await fetch(form.action, {
          method: 'POST',
          body: new URLSearchParams(d),
          signal: ctrl.signal
        });
        if (!res.ok) throw new Error(res.status);
        form.reset();
        if (ok) { ok.style.display = 'block'; ok.focus(); }
      } catch (_) {
        if (err) {
          const a = err.querySelector('a');
          if (a) a.href = mailto(d);
          err.style.display = 'block';
          err.focus();
        } else {
          location.href = mailto(d);
        }
      } finally {
        clearTimeout(timer);
        if (btn) { btn.disabled = false; btn.innerHTML = label; }
      }
    });
  }
})();
