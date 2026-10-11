# Site source

Pages are generated, not hand-edited. Edit the partials, then run `python3 tools/build.py` from the repo root.

- `src/sections/*.html`: one file per section of the site
- `src/style.css`, `src/pages.css`: styles (built into `site.css`)
- `src/app.js`, `src/pages.js`, `src/home_splash.js`: scripts (built into `site.js`)
- `tools/build.py`: assembles `index.html`, `about/`, `shows/`, `press/`, `site.css`, `site.js`, `sitemap.xml`
- Which sections go on which page: the `PAGES` table in `tools/build.py`
