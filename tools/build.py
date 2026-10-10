"""Build the site: wrap each page body in src/pages/ with the shared head,
header, mobile menu and footer, and write plain HTML to the repo root.

    python3 tools/build.py

Pages in src/pages/ are English and land at the root; pages in
src/pages/fr/ are French and land in fr/. Each source starts with a META
comment (path, current, title, desc, optional alt, base, noindex, extra_head).
The generated .html files are committed: the host serves them as they are.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'src' / 'pages'
OUT = ROOT

I = {
 'arrow': '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 'back': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 18l-6-6 6-6"/></svg>',
 'out': '<svg class="out" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M8 7h9v9"/></svg>',
 'chev': '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>',
 'check': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>',
 'strategy': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3v18h18"/><path d="M7 15l4-5 4 3 5-7"/></svg>',
 'sales': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4" fill="currentColor"/></svg>',
 'code': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 6L2 12l6 6M16 6l6 6-6 6"/></svg>',
 'design': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><path d="M2 2l7.6 7.6"/><circle cx="11" cy="11" r="2"/></svg>',
 'cal': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="3"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
 'mail': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="3"/><path d="M22 7l-10 6L2 7"/></svg>',
 'book': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/></svg>',
 'file': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/></svg>',
 'layers': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/></svg>',
 'cap': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 10L12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/></svg>',
 'note': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 013 3L7 19l-4 1 1-4z"/></svg>',
 'flow': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="6" height="6" rx="1.5"/><rect x="15" y="15" width="6" height="6" rx="1.5"/><path d="M9 6h4a2 2 0 012 2v7"/></svg>',
 'cart': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2 3h3l2.6 12.2a2 2 0 002 1.6h8.3a2 2 0 002-1.6L21.5 8H6"/></svg>',
 'shield': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>',
 'db': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/></svg>',
 'user': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg>',
 'filter': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 4h18l-7 9v6l-4 2v-8z"/></svg>',
 'gear': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 00.3 1.8l.1.1a2 2 0 11-2.8 2.8l-.1-.1a1.7 1.7 0 00-1.8-.3 1.7 1.7 0 00-1 1.5V21a2 2 0 11-4 0v-.1a1.7 1.7 0 00-1.1-1.5 1.7 1.7 0 00-1.8.3l-.1.1a2 2 0 11-2.8-2.8l.1-.1a1.7 1.7 0 00.3-1.8 1.7 1.7 0 00-1.5-1H3a2 2 0 110-4h.1a1.7 1.7 0 001.5-1.1 1.7 1.7 0 00-.3-1.8l-.1-.1a2 2 0 112.8-2.8l.1.1a1.7 1.7 0 001.8.3H9a1.7 1.7 0 001-1.5V3a2 2 0 114 0v.1a1.7 1.7 0 001 1.5 1.7 1.7 0 001.8-.3l.1-.1a2 2 0 112.8 2.8l-.1.1a1.7 1.7 0 00-.3 1.8V9a1.7 1.7 0 001.5 1H21a2 2 0 110 4h-.1a1.7 1.7 0 00-1.5 1z"/></svg>',
 'chart': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 20V12M12 20V5M19 20v-9"/></svg>',
 'truck': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1 6h13v10H1zM14 10h4l3 3v3h-7z"/><circle cx="5.5" cy="18.5" r="1.8"/><circle cx="17.5" cy="18.5" r="1.8"/></svg>',
 'phone': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/></svg>',
 'github': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2C6.48 2 2 6.48 2 12c0 4.42 2.87 8.17 6.84 9.5.5.09.68-.22.68-.48v-1.7c-2.78.6-3.37-1.34-3.37-1.34-.45-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.9 1.53 2.34 1.09 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.64 0 0 .84-.27 2.75 1.02a9.6 9.6 0 015 0c1.91-1.29 2.75-1.02 2.75-1.02.55 1.37.2 2.39.1 2.64.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.69-4.57 4.94.36.31.68.92.68 1.85v2.74c0 .27.18.58.69.48A10 10 0 0022 12c0-5.52-4.48-10-10-10z"/></svg>',
 'linkedin': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 11-.01 5.001A2.5 2.5 0 014.98 3.5zM3 8.98h4v12H3v-12zM9 8.98h3.8v1.64h.05c.53-1 1.83-2.06 3.77-2.06 4.03 0 4.78 2.65 4.78 6.1v6.32h-4v-5.6c0-1.34-.03-3.06-1.87-3.06-1.87 0-2.16 1.46-2.16 2.96v5.7H9v-12z"/></svg>',
 'menu': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M4 8h16M4 16h16"/></svg>',
 'close': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
}

MARK = ('<svg class="mark" viewBox="0 0 64 64" aria-hidden="true">'
        '<path fill="currentColor" d="M30.2 5L33 10.6L16.8 55H13.2ZM30.2 5H35.8L52.8 55H43.6ZM22.9 37.2H39V40H21.9ZM9 53.6H21.2V56H9ZM38.6 53.6H57.4V56H38.6Z"/>'
        '<path class="star" d="M26 42.4Q26.6 47.1 31.3 47.7Q26.6 48.3 26 53Q25.4 48.3 20.7 47.7Q25.4 47.1 26 42.4Z"/></svg>')

FONTS = ('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..500;1,6..72,300..500'
         '&family=DM+Sans:opsz,wght@9..40,400..600&display=swap')


T = {
 'en': dict(
   skip='Skip to content', home='Home', services='Services', projects='Projects', certs='Certifications',
   about='About', resources='Resources', contact='Contact', cta='Work together', overview='Overview',
   svc_foot='Four disciplines, one system.', prj_foot='Four projects so far.', all_projects='All projects',
   reply='I reply within 48 working hours', tagline='Systems that bring you customers',
   rights='All rights reserved.', place='Fès, Morocco · Working remotely', open='Open menu', close='Close menu',
   menu='Menu', main='Main', footer='Footer', home_label='Abou Camara, home', switch='FR', switch_label='Version française',
   locale='en_GB',
   svc=[('strategy', 'Consulting &amp; Strategy', 'Working out what to do first', 'service-strategy.html'),
        ('sales', 'Sales Systems', 'Finding and following up leads', 'service-sales-systems.html'),
        ('code', 'Development &amp; Automation', 'Websites, tools and automations', 'service-development.html'),
        ('design', 'Product Design', 'Interfaces that are easy to use', 'service-product-design.html')],
   prj=[('project-eidia.html', 'eidia', 'Eidia Orientation', 'Student guidance web app'),
        ('project-yems.html', 'yems-home', 'YEM&rsquo;S', 'E-commerce · Brand · Full-stack'),
        ('case-lead-scoring.html', None, 'Lead Automation', 'Make · Google Sheets · Webhooks'),
        ('project-olist.html', 'olist', 'Olist E-commerce Dashboard', 'Data analysis · In progress')]),
 'fr': dict(
   skip='Aller au contenu', home='Accueil', services='Services', projects='Projets', certs='Certifications',
   about='À propos', resources='Ressources', contact='Contact', cta='Travailler ensemble', overview='Vue d&rsquo;ensemble',
   svc_foot='Quatre disciplines, un seul système.', prj_foot='Études de cas en anglais.', all_projects='Tous les projets',
   reply='Je réponds sous 48 heures ouvrées', tagline='Des systèmes qui vous amènent des clients',
   rights='Tous droits réservés.', place='Fès, Maroc · Travail à distance', open='Ouvrir le menu', close='Fermer le menu',
   menu='Menu', main='Navigation principale', footer='Pied de page', home_label='Abou Camara, accueil', switch='EN', switch_label='English version',
   locale='fr_FR',
   svc=[('strategy', 'Conseil &amp; Stratégie', 'Savoir par quoi commencer', 'service-strategy.html'),
        ('sales', 'Systèmes de vente', 'Trouver et relancer les prospects', 'service-sales-systems.html'),
        ('code', 'Développement &amp; Automatisation', 'Sites, outils et automatisations', 'service-development.html'),
        ('design', 'Product Design', 'Des interfaces faciles à utiliser', 'service-product-design.html')],
   prj=[('project-eidia.html', 'eidia', 'Eidia Orientation', 'Application d&rsquo;orientation'),
        ('project-yems.html', 'yems-home', 'YEM&rsquo;S', 'E-commerce · Marque · Full-stack'),
        ('case-lead-scoring.html', None, 'Lead Automation', 'Make · Google Sheets · Webhooks'),
        ('project-olist.html', 'olist', 'Olist E-commerce Dashboard', 'Analyse de données · En cours')]),
}


class Ctx:
    """Where links point from a given page.
    b  = prefix to the site root (English-only pages, assets)
    lb = prefix to pages in the same language as this one"""
    def __init__(self, meta):
        self.lang = meta.get('lang', 'en')
        self.t = T[self.lang]
        self.home = meta['current'] == 'home'
        self.b = meta.get('base', '../' if self.lang == 'fr' else '')
        self.lb = '' if self.lang == 'fr' else self.b
        self.h = '' if self.home else self.lb + 'index.html'
        self.home_href = '#top' if self.home else self.lb + 'index.html'
        # language switch: the counterpart page if there is one, else the other home
        alt = meta.get('alt')
        if self.lang == 'fr':
            self.switch_href = self.b + (alt or 'index.html')
        else:
            self.switch_href = self.b + 'fr/' + (alt or 'index.html')


def header(cur, c):
    t, b, lb, h = c.t, c.b, c.lb, c.h
    def cu(k): return ' aria-current="page"' if cur == k else ''
    go = I['arrow'].replace('class="arrow"', 'class="go"')
    svc = ''.join(
        f'<a class="drop-item" href="{lb}{a}"><span class="drop-ico">{I[ic]}</span>'
        f'<span><b>{n}</b><small>{d}</small></span>{go}</a>'
        for ic, n, d, a in t['svc'])
    def thumb(img):
        if img:
            return f'<span class="drop-thumb"><img src="{b}images/work/{img}-thumb.webp" alt="" width="240" height="150" loading="lazy" decoding="async"></span>'
        return f'<span class="drop-thumb" style="display:grid;place-items:center;color:var(--gold)">{I["flow"]}</span>'
    prj = ''.join(
        f'<a class="drop-item" href="{b}{u}">{thumb(img)}<span><b>{n}</b><small>{d}</small></span>{go}</a>'
        for u, img, n, d in t['prj'])
    msvc = ''.join(f'<a href="{lb}{a}">{n}</a>' for ic, n, d, a in t['svc']) + f'<a href="{h}#services">{t["overview"]}</a>'
    mprj = ''.join(f'<a href="{b}{u}">{n}</a>' for u, img, n, d in t['prj'])
    brand = f'<a href="{c.home_href}" class="brand" aria-label="{t["home_label"]}">{MARK}<span class="rule" aria-hidden="true"></span><span class="name">Abou Camara</span></a>'
    other = 'fr' if c.lang == 'en' else 'en'
    lang_link = f'<a href="{c.switch_href}" class="lang" hreflang="{other}" lang="{other}" aria-label="{t["switch_label"]}">{t["switch"]}</a>'
    return f'''<a class="skip" href="#main">{t['skip']}</a>

<!-- ═════════ NAV ═════════ -->
<header id="hdr"{' class="solid"' if cur != 'home' else ''}>
  <nav class="wrap" aria-label="{t['main']}">
    {brand}
    <ul class="menu">
      <li><a href="{c.home_href}"{cu('home')}>{t['home']}</a></li>
      <li><a href="{h}#services"{cu('services')}>{t['services']} {I['chev']}</a>
        <div class="drop">{svc}<div class="drop-foot"><span>{t['svc_foot']}</span><a href="{h}#services">{t['overview']} {I['arrow']}</a></div></div></li>
      <li><a href="{b}work.html"{cu('work')}>{t['projects']} {I['chev']}</a>
        <div class="drop">{prj}<div class="drop-foot"><span>{t['prj_foot']}</span><a href="{b}work.html">{t['all_projects']} {I['arrow']}</a></div></div></li>
      <li><a href="{b}certificates.html"{cu('certs')}>{t['certs']}</a></li>
      <li><a href="{h}#about"{cu('about')}>{t['about']}</a></li>
      <li><a href="{b}resources.html"{cu('resources')}>{t['resources']}</a></li>
    </ul>
    <div class="nav-end">
      {lang_link}
      <a href="{h}#contact" class="btn btn-outline-gold btn-sm nav-cta">{t['cta']} {I['arrow']}</a>
      <button class="burger" id="burger" type="button" aria-label="{t['open']}" aria-expanded="false" aria-controls="mnav">{I['menu']}</button>
    </div>
  </nav>
</header>

<div class="mnav" id="mnav" aria-hidden="true" role="dialog" aria-modal="true" aria-label="{t['menu']}">
  <div class="wrap mnav-top">
    {brand}
    <button class="burger" id="mnav-close" type="button" aria-label="{t['close']}">{I['close']}</button>
  </div>
  <div class="wrap mnav-body">
    <ul class="mnav-list">
      <li><a href="{c.home_href}"{cu('home')}>{t['home']}</a></li>
      <li><details><summary>{t['services']} {I['chev']}</summary><div class="mnav-sub">{msvc}</div></details></li>
      <li><details><summary>{t['projects']} {I['chev']}</summary><div class="mnav-sub">{mprj}<a href="{b}work.html">{t['all_projects']}</a></div></details></li>
      <li><a href="{b}certificates.html"{cu('certs')}>{t['certs']}</a></li>
      <li><a href="{h}#about">{t['about']}</a></li>
      <li><a href="{b}resources.html"{cu('resources')}>{t['resources']}</a></li>
    </ul>
  </div>
  <div class="wrap mnav-foot">
    <a href="{h}#contact" class="btn btn-gold btn-full">{t['cta']} {I['arrow']}</a>
    <small>{t['reply']} · <a href="{c.switch_href}" hreflang="{other}" lang="{other}">{t['switch_label']}</a></small>
  </div>
</div>
'''


def footer(c):
    t, b, h = c.t, c.b, c.h
    return f'''
<!-- ═════════ FOOTER ═════════ -->
<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        <a href="{c.home_href}" class="brand" aria-label="{t['home_label']}">{MARK}<span class="rule" aria-hidden="true"></span><span class="name">Abou Camara</span></a>
        <p class="tagline">{t['tagline']}</p>
      </div>
      <nav class="foot-nav" aria-label="{t['footer']}">
        <a href="{h}#services">{t['services']}</a>
        <a href="{b}work.html">{t['projects']}</a>
        <a href="{b}certificates.html">{t['certs']}</a>
        <a href="{h}#about">{t['about']}</a>
        <a href="{b}resources.html">{t['resources']}</a>
        <a href="{h}#contact">{t['contact']}</a>
      </nav>
      <div class="socials">
        <a class="soc" href="https://www.linkedin.com/in/abou-camara-3b731b380/" target="_blank" rel="noopener" aria-label="LinkedIn">{I['linkedin']}</a>
        <a class="soc" href="https://github.com/abou-arch?tab=repositories" target="_blank" rel="noopener" aria-label="GitHub">{I['github']}</a>
        <a class="soc" href="mailto:aboucamara1107@gmail.com" aria-label="Email">{I['mail']}</a>
      </div>
    </div>
    <div class="copy">
      <span>© <span data-year>2026</span> Abou Camara. {t['rights']}</span>
      <span>{t['place']}</span>
    </div>
  </div>
</footer>

<script src="{b}motion.js" defer></script>
</body>
</html>
'''


def page_url(path):
    return 'https://aboucamara.org/' + ('' if path == 'index.html' else path.removesuffix('index.html') if path.endswith('/index.html') else path)


def head(meta, c):
    b = c.b
    url = page_url(meta['path'])
    robots = '\n<meta name="robots" content="noindex">' if meta.get('noindex') else ''
    canon = '' if meta.get('noindex') else f'\n<link rel="canonical" href="{url}">'
    alts = ''
    if 'alt' in meta and not meta.get('noindex'):
        en_path, fr_path = (meta['path'], 'fr/' + meta['alt']) if c.lang == 'en' else (meta['alt'], meta['path'])
        alts = (f'\n<link rel="alternate" hreflang="en" href="{page_url(en_path)}">'
                f'\n<link rel="alternate" hreflang="fr" href="{page_url(fr_path)}">'
                f'\n<link rel="alternate" hreflang="x-default" href="{page_url(en_path)}">')
    return f'''<!DOCTYPE html>
<html lang="{c.lang}" class="no-js">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta['title']}</title>
<meta name="description" content="{meta['desc']}">{robots}{canon}{alts}
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{meta['title']}">
<meta property="og:description" content="{meta['desc']}">
<meta property="og:image" content="https://aboucamara.org/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{c.t['locale']}">
<meta property="og:site_name" content="Abou Camara">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{meta['title']}">
<meta name="twitter:description" content="{meta['desc']}">
<meta name="twitter:image" content="https://aboucamara.org/og-image.png">
<meta name="theme-color" content="#0B0B0D">
<meta name="color-scheme" content="dark">

<link rel="icon" href="{b}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{b}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="{b}style.css">{meta.get('extra_head','')}
</head>
<body>
'''


def build():
    sources = sorted(SRC.glob('*.html')) + sorted((SRC / 'fr').glob('*.html'))
    for page in sources:
        raw = page.read_text(encoding='utf-8')
        m = re.match(r'<!--META(.*?)-->\n', raw, re.S)
        meta = {}
        for line in m.group(1).strip().splitlines():
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip().replace('\\n', '\n')
        if page.parent.name == 'fr':
            meta['lang'] = 'fr'
        c = Ctx(meta)
        body = raw[m.end():]
        body = re.sub(r'\{\{(\w+)\}\}', lambda mm: MARK if mm.group(1) == 'mark' else I[mm.group(1)], body)
        html = head(meta, c) + header(meta['current'], c) + '\n<main id="main">\n' + body.strip('\n') + '\n</main>\n' + footer(c)
        out = OUT / meta['path']
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding='utf-8')
        print('wrote', meta['path'])


if __name__ == '__main__':
    build()
