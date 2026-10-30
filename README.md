# Portfolio | Abou Camara

Personal site: consulting, sales systems, development, automation and product design.

**Live:** https://aboucamara.org

## Structure

```
index.html               Home: hero, services, selected work, about, process, certifications, contact
service-*.html           One page per service: strategy, sales systems, development, product design
fr/                      French versions: home and the four service pages
work.html                All projects, filterable by category
project-eidia.html       Project page: Eidia Orientation
project-yems.html        Project page: YEM'S
case-lead-scoring.html   Project page + case study: Lead Automation
project-olist.html       Project page: Olist dashboard (in progress)
certificates.html        All certificates, filterable by category
resources.html           Resources (case studies now, articles later)
404.html                 Error page (uses root-absolute paths)
style.css                Shared design system for every page
motion.js                Shared interactions: nav, mobile menu, reveals, filters, contact form
favicon.svg              Monogram on dark tile; apple-touch-icon.png is the same at 180px
images/hero/             Hero still life: transparent cutout (basalt, smoked glass, brass, a tablet
                         with an abstract diagram), WebP 640/900/1100 (still-life-hero-*); the
                         earlier framed still life (still-life-*) is kept but no page uses it now
images/about/            About portrait: transparent cutout, WebP 560/900 (portrait-cutout-*); the
                         version with its wall background (portrait-*) is kept, not used now
images/services/         One interface illustration per service (home cards + service page heroes),
                         WebP 560/900
images/editorial/        Still lifes for Process, Resources, the 404 page and the dark closing block
                         of the footer (WebP, two widths each); about-approach-* is kept, not used
                         now (the hero still life uses the same objects)
src/assets/              Source files that are not served (the original cutouts: portrait, hero still life)
images/work/             Project screenshots (WebP, 640/1200 wide + menu thumbnails)
images/certs/            Certificate thumbnails (WebP used by the site, PNG/JPG sources)
certs/                   Original certificate files (PDF / JPG)
```

The pages are plain HTML, CSS and JavaScript, with no dependencies. The header, menus,
footer and `<head>` are shared, so they are generated:

```
src/pages/*.html         Page bodies, English (written to the repo root)
src/pages/fr/*.html      Page bodies, French (written to fr/)
tools/build.py           Wraps each body with the shared parts and writes the .html files
```

Edit a page in `src/pages/`, then run `python3 tools/build.py` (Python 3.9+, no packages).
Commit both the source and the generated file: the host serves the generated `.html`
as it is. Nav labels, the menu lists and the footer live at the top of `tools/build.py`,
in English and French. A page with a translation sets `alt:` in its META block; that
drives the EN/FR switch and the `hreflang` tags.

## Design system

Defined as custom properties at the top of `style.css`.

- **Palette:** warm off-white `#F5F4F0` with panels `#EEEDE8` / `#E8E7E1`, near-black ink
  `#171715`, warm greys (`#5F5E58` for secondary text), and a taupe accent `#A18B70` used only
  for decoration (the dot after a headline, the logo star). Accent text uses the darker
  `#715E49`. The footer is the only dark area (`#1C1C19`). Every text colour passes WCAG AA
  on every surface.
- **Type:** DM Sans throughout, from Google Fonts. Headlines are weight 500 with tight
  letter-spacing; the second half of a heading can sit in a lighter grey (`<em>`), only at 24px
  and above (`--soft` is 3:1). Until the font arrives, `DM Sans Fallback` (local Arial scaled to
  DM Sans' measured metrics, per weight) keeps the layout from jumping when it swaps in.
- **Images:** a still-life series (stone, smoked glass, brass, window light). Cutouts (the hero
  still life, the About portrait) are transparent WebP set straight on the page colour, never in
  a frame or on a panel. The service illustrations are interface mock-ups; the editorial still
  lifes stay in secondary sections. Generated images only illustrate ideas; projects always use
  real screenshots.
- **Logo:** "A" monogram with a small taupe star. The SVG is inlined in each page header
  and footer; `favicon.svg` is the tile version.
- **Motion:** text fades up on load; sections and cards reveal on scroll while their images
  settle into the frame; the About bust rises out of its line; images zoom slightly on hover;
  link underlines draw in; the mobile menu opens with a short stagger (and closes faster) and
  its sub-lists unfold; a reading progress line runs at the top. On the home page the name
  scrolls behind the still life; a button pauses it, it stops when the hero is off screen, and
  it stands still without JavaScript. Under `prefers-reduced-motion` each effect is handled on
  its own: nothing slides, scales or scrolls by itself, state changes are instant.
- **Without JavaScript:** content is visible (no reveal), and below 1080px a "Menu" link to the
  footer navigation replaces the burger.

## Editing

**Add a project**: add a card to `work.html` (set `data-cats` to one or more of
`web automation data ecommerce`), a row on the home page, an entry in the Projects
dropdown and mobile menu, and a page based on `project-eidia.html`.
Screenshots: WebP at 1200 and 640 px wide in `images/work/`, plus a 240×150 `-thumb.webp`.

**Add a certificate**: duplicate an `<article class="cert">` block in `certificates.html`,
set `data-cats` to `dev`, `data` or `leadership`, add the thumbnail to `images/certs/` and the
original to `certs/`, then update the counts on the filter buttons and the list on the home page.

## Content rule

Nothing on this site is invented: no client logos, testimonials, metrics or results that
haven't happened. Prototypes and work in progress are labelled as such.

## Notes

- `_headers` sets the security headers (CSP, HSTS, framing, referrer, permissions) that
  Cloudflare adds to every response. A new external service (a font host, an embed, a form
  endpoint) must be added to the Content-Security-Policy there, or the browser will block it.
- The contact form (home page, EN and FR) posts to a Make webhook, set in the form's
  `action`. The Make scenario "Portfolio – Formulaire de contact" scores the enquiry, adds it
  to the "Demandes" Google Sheet and sends an email alert. If the request fails, the form
  offers a pre-filled email instead. The hidden `website` field is a spam trap.

- The home pages (EN and FR) carry JSON-LD (`WebSite` + `Person`) in the `extra_head` of their
  META block. Keep it to facts the site already states. It is a data block, so the CSP allows it.
- `images/abou.jpg`, `images/dashboard.png`, `images/eidia.png` and `images/leads.png` come from
  the first version of the site. They are kept on purpose, even though no page uses them now.
- File names are lowercase on purpose: the host is case-sensitive, Windows is not.
  A capital letter that works locally will 404 once deployed.
