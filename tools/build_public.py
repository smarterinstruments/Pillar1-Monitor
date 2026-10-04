"""Build the public GitHub Pages page from the editorial (private) monitor page.

Usage: python3 tools/build_public.py <monitor.html> [index.html]

Reads the <script type="application/json" id="monitor-data"> block, shows the Complementarity
tab in aggregate (no centre names from the aCCCess survey), re-embeds the data and wraps the
page in a full HTML document for GitHub Pages.
"""
import json, copy, re, sys, pathlib

def dump(d):
    js = lambda v: json.dumps(v, ensure_ascii=False)
    keys = list(d); lines = []
    for i, k in enumerate(keys):
        v, end = d[k], (',' if i < len(keys) - 1 else '')
        if isinstance(v, list):
            lines.append(f'  {js(k)}: [\n' + ',\n'.join(f'    {js(x)}' for x in v) + f'\n  ]{end}')
        else:
            lines.append(f'  {js(k)}: {js(v)}{end}')
    return ('{\n' + '\n'.join(lines) + '\n}').replace('</', '<\\/')

def public(d):
    d = copy.deepcopy(d)
    M = d['compl']
    groups = []
    for r in M['rows']:
        g = next((x for x in groups if x['g'] == r['g']), None)
        if not g:
            g = {'g': r['g'], 'n': 0, 'counts': [0] * len(M['domains'])}; groups.append(g)
        g['n'] += 1
        for j, ch in enumerate(r['s']):
            if ch == '3': g['counts'][j] += 1
    M['agg'] = groups
    del M['rows']
    for p in M['profiles']:
        p[1] = f"{len([x for x in p[1].split(',') if x.strip()])} centres"
    M['pairs'] = [
        ["Design ↔ fabrication", "lithography, cleanroom and process development", "IC design (analog, digital, RF), ASIC/FPGA, EDA"],
        ["Design ↔ back-end", "packaging, validation and reliability testing", "design capacity and digital platforms"],
        ["Fabrication ↔ back-end", "packaging and system integration", "wafer processing and test"],
        ["Broker ↔ centres with own infrastructure (7)", "access to labs and cleanrooms for its users", "new users and demand from other countries"],
        ["Nordic-Baltic ↔ Central Europe", "EDA tools and systems engineering", "new wide-bandgap materials and graphene/2D"]]
    M['pairsNote'] = "Pairs between named centres are in the members' version."
    for r in M['regions']:
        r[1] = r[1].split(';')[0]
    counts = {'APECS': '8 centres; 14 want it', 'NanoIC': '6 centres', 'FAMES': '11 centres', 'PIXEurope': '15 centres',
              'WBG': '14 / 4 centres', 'Quantum': '8 centres', 'EuroCDP': '10 centres', 'Chips Venture': '10 centres'}
    for e in M['entry']:
        e[2] = next(v for k, v in counts.items() if e[0].startswith(k))
        e[3] = e[3].replace('; SK Chips plans a ~€20M power-module centre complementing APECS', '')
    M['method'] = ("Main focus = 3, secondary = 2, emerging = 1, not applicable = 0 across 26 domains. Demand = keyword coding of the centres' "
                   "technology priorities and cooperation wishes. Value-chain profiles use the average support score (1–5) for design, fabrication "
                   "and back-end stages. Shown in aggregate; ratings are self-assessments and some centres rate almost every domain as a main focus. "
                   "Staff numbers sometimes cover the whole host institution. Contact details from the survey are not shown.")
    M['findings'] = [f for f in M['findings']]
    return d


def build(src_html):
    m = re.search(r'(<script type="application/json" id="monitor-data">\n)(.*?)(\n</script>)', src_html, re.S)
    data = json.loads(m.group(2).replace('<\\/', '</'))
    if 'rows' in data.get('compl', {}):
        data = public(data)
    html = src_html[:m.start(2)] + dump(data) + src_html[m.end(2):]
    if not html.lstrip().lower().startswith('<!doctype'):
        head_end = html.index('</style>') + len('</style>')
        meta = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                '<meta name="description" content="Independent weekly monitor of the EU Chips Act Pillar I: pilot lines, the European Chips Design Platform, the Chips Competence Centres and the aCCCess network action. Alpha version.">\n'
                '<meta name="robots" content="noindex">\n')
        html = '<!doctype html>\n<html lang="en">\n<head>\n' + meta + html[:head_end] + '\n</head>\n<body>\n' + html[head_end:] + '\n</body>\n</html>\n'
    return html

if __name__ == '__main__':
    src = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8')
    out = build(src)
    if len(sys.argv) > 2:
        pathlib.Path(sys.argv[2]).write_text(out, encoding='utf-8')
    else:
        sys.stdout.write(out)
