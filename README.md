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
images/hero/             Hero photo (desktop WebP + JPEG fallback, mobile crop)
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

- **Palette:** deep black `#0B0B0D`, surfaces `#141417` / `#1A1A1D`, ivory `#F8F6F1`,
  warm greys, one bronze accent `#D4AF7C` (used sparingly). The About section uses the
  light ivory variant (`.light`).
- **Type:** Newsreader (editorial serif, headings) + DM Sans (interface and text), from Google Fonts.
- **Logo:** serif "A" monogram with a small bronze star. The SVG is inlined in each page header
  and footer; `favicon.svg` is the tile version.
- **Motion:** short reveals on scroll, subtle hovers. Everything is disabled under
  `prefers-reduced-motion`.

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

- File names are lowercase on purpose: the host is case-sensitive, Windows is not.
  A capital letter that works locally will 404 once deployed.
