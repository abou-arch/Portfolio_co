# Portfolio — Abou Camara

Personal site: growth, sales systems, development and design.

**Live:** https://aboucamara.org

## Structure

```
index.html               Home — services, work, about, credentials, pricing, contact
certificates.html        All certificates, filterable by category
case-lead-scoring.html   Case study — lead scoring engine
style.css                Shared stylesheet for all three pages
images/                  Project screenshots + portrait
images/certs/            Certificate thumbnails
certs/                   Original certificate files (PDF / JPG)
```

No build step, no dependencies. Plain HTML and CSS — open `index.html` in a browser
and what you see is what ships.

## Editing

**Add a project screenshot** — drop the file in `images/` and point the `<img src>`
at it. The placeholder disappears on its own once the file exists.

**Add a certificate** — duplicate an `<article class="cert">` block in
`certificates.html`, set `data-cat` to one of `dev` / `data` / `leadership`,
add the thumbnail to `images/certs/` and the original to `certs/`.

**Replace the portrait** — overwrite `images/abou.jpg`, keep the filename.

## Notes

- File names are lowercase on purpose: GitHub Pages is case-sensitive, Windows is not.
  A capital letter that works locally will 404 once deployed.
- Fonts are loaded from Google Fonts: Fraunces (display) and DM Sans (body).
