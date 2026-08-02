/* ══════════════════════════════════════════════════════════════════════
   Abou Camara — shared interaction layer
   Every block is guarded, so the same file runs on all three pages.
   ══════════════════════════════════════════════════════════════════════ */
(() => {
  'use strict';

  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── year ──────────────────────────────────────────────────────────── */
  const yr = $('#yr');
  if (yr) yr.textContent = new Date().getFullYear();

  /* ── sticky nav ────────────────────────────────────────────────────── */
  const hdr = $('#hdr');
  if (hdr) {
    const stick = () => hdr.classList.toggle('stuck', scrollY > 16);
    stick();
    addEventListener('scroll', stick, { passive: true });
  }

  /* ── mobile menu ───────────────────────────────────────────────────── */
  const burger = $('#burger');
  const menu   = $('#menu');
  if (burger && menu) {
    burger.addEventListener('click', () => {
      const open = menu.classList.toggle('open');
      burger.setAttribute('aria-expanded', String(open));
    });
    $$('a', menu).forEach(a => a.addEventListener('click', () => {
      menu.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
    }));
  }

  /* ── scroll progress ───────────────────────────────────────────────────
     Modern browsers drive this from CSS (animation-timeline: scroll()).
     Only fall back to JS where that isn't supported.                      */
  const bar = $('.progress');
  if (bar && !CSS.supports('animation-timeline', 'scroll()')) {
    let tick = false;
    const draw = () => {
      const max = document.documentElement.scrollHeight - innerHeight;
      bar.style.transform = `scaleX(${max > 0 ? scrollY / max : 0})`;
      tick = false;
    };
    addEventListener('scroll', () => {
      if (!tick) { tick = true; requestAnimationFrame(draw); }
    }, { passive: true });
    draw();
  }

  /* ── hero line reveal ──────────────────────────────────────────────── */
  const lines = $('.lines');
  if (lines) requestAnimationFrame(() => lines.classList.add('go'));

  /* ── reveal on scroll ──────────────────────────────────────────────── */
  const targets = $$('.rv');
  if (targets.length) {
    if (calm) {
      targets.forEach(el => el.classList.add('on'));
    } else {
      const io = new IntersectionObserver((entries, obs) => {
        entries.forEach((en, i) => {
          if (!en.isIntersecting) return;
          en.target.style.transitionDelay = Math.min(i * 70, 280) + 'ms';
          en.target.classList.add('on');
          obs.unobserve(en.target);
        });
      }, { threshold: .08, rootMargin: '0px 0px -60px 0px' });
      targets.forEach(el => io.observe(el));
    }
  }

  /* ── metrics: rule sweep + count-up ────────────────────────────────── */
  const metrics = $('.metrics');
  if (metrics) {
    const run = () => {
      metrics.classList.add('seen');
      $$('[data-to]', metrics).forEach(el => {
        const to     = parseFloat(el.dataset.to);
        const suffix = el.dataset.suffix || '';
        if (calm) { el.textContent = to + suffix; return; }
        const dur = 1400;
        const t0  = performance.now();
        const step = now => {
          const p = Math.min((now - t0) / dur, 1);
          const e = 1 - Math.pow(1 - p, 3);           // easeOutCubic
          el.textContent = Math.round(to * e) + suffix;
          if (p < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
      });
    };
    new IntersectionObserver((en, obs) => {
      if (en[0].isIntersecting) { run(); obs.disconnect(); }
    }, { threshold: .4 }).observe(metrics);
  }

  /* ── spotlight follow ──────────────────────────────────────────────────
     Writes CSS custom properties the stylesheet reads. Pointer-only, so
     touch devices never pay for it.                                       */
  const lit = $$('.card, .band');
  if (lit.length && !calm && matchMedia('(pointer: fine)').matches) {
    lit.forEach(el => {
      el.addEventListener('pointermove', e => {
        const r = el.getBoundingClientRect();
        el.style.setProperty('--mx', `${e.clientX - r.left}px`);
        el.style.setProperty('--my', `${e.clientY - r.top}px`);
      });
    });
  }

  /* ── marquee: duplicate the track so the loop is seamless ──────────── */
  const track = $('.marquee ul');
  if (track && !calm) {
    const clone = track.cloneNode(true);
    clone.setAttribute('aria-hidden', 'true');
    track.parentElement.appendChild(clone);
  }

  /* ── certificates filter ───────────────────────────────────────────── */
  const bar2 = $('.cert-bar');
  if (bar2) {
    const buttons = $$('button', bar2);
    const cards   = $$('.cert');
    const empty   = $('#empty');
    buttons.forEach(btn => btn.addEventListener('click', () => {
      buttons.forEach(b => b.classList.remove('on'));
      btn.classList.add('on');
      const f = btn.dataset.filter;
      let shown = 0;
      cards.forEach(c => {
        const show = f === 'all' || c.dataset.cat === f;
        c.classList.toggle('hide', !show);
        if (show) shown++;
      });
      if (empty) empty.style.display = shown ? 'none' : 'block';
    }));
  }

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
        + '?subject=' + encodeURIComponent('New project — ' + d.get('name'))
        + '&body='    + encodeURIComponent(body);
    });
  }
})();
