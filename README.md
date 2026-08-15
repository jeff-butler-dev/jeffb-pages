# Personal Pages Catalog

Public static-page catalog deployed with GitHub Pages.

- Live site: `https://jeff-butler-dev.github.io/jeffb-pages/`
- Deployable content: [`site/`](./site/)
- Public publication rules: [`PUBLICATION_POLICY.md`](./PUBLICATION_POLICY.md)

## Add a public page

1. Create `site/<page-name>/index.html`.
2. Add a generic card to `site/index.html`.
3. Run `python scripts/public_site_check.py` from the repository root.
4. Manually review the diff against `PUBLICATION_POLICY.md`.
5. Commit and push to `main`. The deployment workflow runs the same safety scan before publishing.

Do not place credentials or personal data in `site/`. The site is public and the current GitHub Pages hostname contains the GitHub account name.
