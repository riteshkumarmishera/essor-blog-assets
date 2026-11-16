from playwright.sync_api import sync_playwright
import os

W, H = 1200, 620

tiles = [
    ("72%", "searched for or chose a new healthcare provider in the past 12 months"),
    ("75%", "won't book with a provider rated below 4.0 stars"),
    ("66%", "say a provider's reply to a review changes their trust in it"),
]

tile_w = 340
gap = 40
start_x = (W - (tile_w * 3 + gap * 2)) // 2

svg_tiles = ""
for i, (big, small) in enumerate(tiles):
    x = start_x + i * (tile_w + gap)
    svg_tiles += f'''
    <rect x="{x}" y="140" width="{tile_w}" height="300" rx="20" fill="#FFFFFF" stroke="#E3DCCB" stroke-width="2"/>
    <text x="{x+tile_w/2}" y="250" font-size="64" font-weight="800" fill="#0E8C7F" text-anchor="middle">{big}</text>
    '''
    words = small.split()
    lines = []
    cur = ""
    for w in words:
        if len(cur + " " + w) > 28:
            lines.append(cur.strip())
            cur = w
        else:
            cur += " " + w
    lines.append(cur.strip())
    for li, line in enumerate(lines):
        svg_tiles += f'<text x="{x+tile_w/2}" y="{300+li*28}" font-size="21" fill="#3a3a3a" text-anchor="middle">{line}</text>'

svg = f'''<svg width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" style="background:#FFF7EC;font-family:Arial,Helvetica,sans-serif">
<text x="60" y="60" font-size="30" font-weight="700" fill="#0B4F47">Patients already hold providers to a higher bar</text>
<text x="60" y="95" font-size="22" fill="#555">From rater8's 2026 Patient Choice Report, a survey of almost 1,000 US patients</text>
{svg_tiles}
</svg>'''

with open("medical-seo-patient-research.html", "w") as f:
    f.write(f"<html><body style='margin:0'>{svg}</body></html>")

with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page(viewport={"width": W, "height": H})
    pg.goto("file://" + os.path.abspath("medical-seo-patient-research.html"))
    pg.screenshot(path="medical-seo-patient-research.png")
    br.close()
print("chart 2 ok")
