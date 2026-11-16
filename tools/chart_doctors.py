from playwright.sync_api import sync_playwright

W, H = 1200, 700

pairs = [
    ("family doctor near me", 49500, "family doctor near me\naccepting new patients", 1300),
    ("primary care physician\nnear me", 40500, "primary care physician near me\naccepting new patients", 9900),
]

bar_w = 90
group_gap = 220
chart_left = 140
chart_top = 160
chart_bottom = 580
max_val = 49500

def y_for(v):
    frac = v / max_val
    return chart_bottom - frac * (chart_bottom - chart_top)

bars_svg = ""
labels_svg = ""
x = chart_left
colors = ["#4C6FFF", "#F5A524"]
for i, (label_a, val_a, label_b, val_b) in enumerate(pairs):
    for j, (label, val) in enumerate([(label_a, val_a), (label_b, val_b)]):
        bx = x + j * (bar_w + 18)
        y = y_for(val)
        h = chart_bottom - y
        bars_svg += f'<rect x="{bx}" y="{y}" width="{bar_w}" height="{h}" rx="8" fill="{colors[j]}"/>'
        bars_svg += f'<text x="{bx + bar_w/2}" y="{y - 14}" font-size="22" font-weight="700" fill="#1E2240" text-anchor="middle">{val:,}</text>'
    group_center = x + bar_w + 9
    lines = label_a.split("\n")
    for k, line in enumerate(lines):
        labels_svg += f'<text x="{group_center}" y="{chart_bottom + 34 + k*22}" font-size="16" fill="#555" text-anchor="middle">{line}</text>'
    x += group_gap

legend_svg = f'''
<rect x="700" y="60" width="18" height="18" rx="4" fill="{colors[0]}"/>
<text x="724" y="75" font-size="16" fill="#333">Broad "near me" search</text>
<rect x="700" y="86" width="18" height="18" rx="4" fill="{colors[1]}"/>
<text x="724" y="101" font-size="16" fill="#333">+ "accepting new patients"</text>
'''

svg = f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;font-family:Arial,Helvetica,sans-serif;background:#fff}}
</style></head><body>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<rect width="{W}" height="{H}" fill="#ffffff"/>
<text x="60" y="55" font-size="30" font-weight="800" fill="#1E2240">Adding "accepting new patients" doesn't erase the demand</text>
<text x="60" y="85" font-size="18" fill="#666">Real US monthly search volume, pulled from Ubersuggest</text>
{bars_svg}
{labels_svg}
{legend_svg}
<line x1="{chart_left-20}" y1="{chart_bottom}" x2="1140" y2="{chart_bottom}" stroke="#ccc" stroke-width="2"/>
</svg>
</body></html>'''

with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page(viewport={"width": W, "height": H})
    pg.set_content(svg)
    pg.screenshot(path="local-seo-for-doctors-demand.png")
    br.close()
print("ok")
