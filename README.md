# EU Chips Act Pillar I Monitor (alpha)

Independent weekly monitor of Pillar I of the EU Chips Act (Chips for Europe Initiative): the pilot lines, the European Chips Design Platform (EuroCDP), the Chips Competence Centres and the aCCCess network action.

- Live page: https://smarterinstruments.github.io/Pillar1-Monitor/
- Prepared by Stanislav Černý, Czech National Semiconductor Cluster
- Feedback until 1 November 2026: cerny@semicz.eu
- Not an official publication of the European Commission, the Chips JU or any project.

All data sit in one JSON block (`<script type="application/json" id="monitor-data">`) inside `index.html`; the page renders itself from it. Updates are published weekly after editorial review.

## Updating

`tools/build_public.py` turns the editorial monitor page into the public `index.html`: it keeps the page and its data, shows the Complementarity tab in aggregate (no centre names from the aCCCess survey of the competence centres) and wraps the page for GitHub Pages.

```
python3 tools/build_public.py monitor.html index.html
```
