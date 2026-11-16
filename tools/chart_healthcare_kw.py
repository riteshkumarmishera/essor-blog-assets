from playwright.sync_api import sync_playwright

W, H = 1200, 460

stages = [
    ("Symptom", '"why does my knee hurt"', 14800, "#4C6FFF"),
    ("Condition / treatment", '"knee pain treatment"', 135000, "#F5A524"),
    ("Provider", '"orthopedic surgeon near me"', 40500, "#14B8A6"),
]

max_val = 135000
bar_left = 340
bar_max_w = 680
bar_h = 70
gap = 50
top = 150

bars_svg = ""
y = top
for label, phrase, vol, color in stages:
    w = (vol / max_val) * bar_max_w
    bars_svg += f'<text x="{bar_left - 20}" y="{y + bar_h/2 - 6}" font-size="20" font-weight="700" fill="#1E2240" text-anchor="end">{label}</text>'
    bars_svg += f'<text x="{bar_left - 20}" y="{y + bar_h/2 + 18}" font-size="15" fill="#666" text-anchor="end">{phrase}</text>'
    bars_svg += f'<rect x="{bar_left}" y="{y}" width="{w}" height="{bar_h}" rx="10" fill="{color}"/>'
    bars_svg += f'<text x="{bar_left + w + 16}" y="{y + bar_h/2 + 7}" font-size="22" font-weight="800" fill="#1E2240">{vol:,}/mo</text>'
    y += bar_h + gap

svg = f'''<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;font-family:Arial,Helvetica,sans-serif;background:#fff}}
</style></head><body>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<rect width="{W}" height="{H}" fill="#ffffff"/>
<text x="60" y="55" font-size="28" font-weight="800" fill="#1E2240">One patient's search journey, mapped in real volume</text>
<text x="60" y="85" font-size="17" fill="#666">A single condition (knee pain), three real monthly US search volumes from Ubersuggest</text>
{bars_svg}
</svg>
</body></html>'''

with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page(viewport={"width": W, "height": H})
    pg.set_content(svg)
    pg.screenshot(path="keyword-research-healthcare-journey.png")
    br.close()
print("ok")
