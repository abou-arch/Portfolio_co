# Security

This is a static site: plain HTML, CSS and one small script, no server code,
no database, no cookies and no account system.

## Reporting a vulnerability

Email **aboucamara1107@gmail.com** with a short description and the steps to
reproduce it. You will get a reply within 48 hours. Please do not open a public
issue for a security problem.

The same contact is published at `/.well-known/security.txt`.

## What is in place

- `_headers`: Content-Security-Policy (scripts from this site only, no inline
  script), HSTS, X-Frame-Options DENY and frame-ancestors 'none' against
  clickjacking, nosniff, strict Referrer-Policy, Permissions-Policy.
- The same CSP is repeated in a `<meta>` tag on each page, as a fallback if the
  site is ever served without `_headers`.
- The contact form never sends data anywhere: it opens the visitor's mail app.
  Inputs are length-limited and line breaks are stripped from the subject.
- `.assetsignore` keeps repo files (`.git`, config, Markdown notes) from being served.

## Keep in mind

- Never commit API keys or webhook URLs (Make, Zapier...). Keep them in local
  files listed in `.gitignore`.
- Update the `Expires` date in `.well-known/security.txt` before September 2027.
