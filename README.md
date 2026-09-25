# Portfolio | Abou Camara

Personal site: growth, sales systems, development and design.

**Live:** https://aboucamara.org

## Structure

```
index.html               Home: services, work, about, credentials, pricing, contact
certificates.html        All certificates, filterable by category
legal.html               Legal notice (publisher, host, intellectual property)
privacy.html             Privacy policy (Law 09-08 and GDPR)
terms.html               Terms of use of the site
case-lead-scoring.html   Case study: lead scoring engine
style.css                Shared stylesheet for all three pages
images/                  Hero photo, portrait, project screenshots
images/certs/            Certificate thumbnails
_headers                 Security headers (CSP, HSTS...) read by Cloudflare
.well-known/security.txt Where to report a security issue
certs/                   Original certificate files (PDF / JPG)
```

No build step, no dependencies. Plain HTML and CSS. Open `index.html` in a browser
and what you see is what ships.

## Editing

**Add a project screenshot:** drop the file in `images/` and point the `<img src>`
at it. The placeholder disappears on its own once the file exists.

**Add a certificate:** duplicate an `<article class="cert">` block in
`certificates.html`, set `data-cat` to one of `dev` / `data` / `leadership`,
add the thumbnail to `images/certs/` and the original to `certs/`.

**Replace the portrait:** overwrite `images/abou.jpg`, keep the filename.

**Replace the hero photo:** overwrite `images/hero.webp`. Keep it 16:9 with the
person in the right third: the headline sits on the left, and the floating cards are
positioned in % of the photo, so they stay on the same spot at every screen width.

## Notes

- File names are lowercase on purpose: GitHub Pages is case-sensitive, Windows is not.
  A capital letter that works locally will 404 once deployed.
- Fonts are loaded from Google Fonts: Fraunces (display) and DM Sans (body), plus
  Caveat (subset to a single line) for the handwritten note on the portrait.
- Security: see `SECURITY.md`. The pages load no inline script, so never add an
  `onclick=""` or `<script>...</script>` in the HTML: put it in `motion.js`, or the
  Content-Security-Policy will block it.
