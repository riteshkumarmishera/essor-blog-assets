from playwright.sync_api import sync_playwright

W, H = 1200, 700

# Chart 1: vertical bar chart of real patient demand across specialties
data1 = [
    ("Urgent care\nnear me", 4090000),
    ("Dentist\nnear me", 1830000),
    ("Walk-in clinic\nnear me", 201000),
    ("Doctor\nnear me", 135000),
]
max_v1 = max(v for _, v in data1)

chart_top = 150
chart_bottom = 560
chart_h = chart_bottom - chart_top

bars1 = ""
bw = 180
gap = 90
start_x = 120
for i, (label, v) in enumerate(data1):
    x = start_x + i * (bw + gap)
    h = int((v / max_v1) * chart_h)
    y = chart_bottom - h
    bars1 += f'''
    <rect x="{x}" y="{y}" width="{bw}" height="{h}" rx="10" fill="#0E8C7F"/>
    <text x="{x+bw/2}" y="{y-16}" font-size="26" font-weight="700" fill="#0B4F47" text-anchor="middle">{v:,}</text>
    '''
    for li, line in enumerate(label.split("\n")):
        bars1 += f'<text x="{x+bw/2}" y="{chart_bottom+30+li*26}" font-size="22" fill="#2b2b2b" text-anchor="middle">{line}</text>'

svg1 = f'''<svg width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" style="background:#FFF7EC;font-family:Arial,Helvetica,sans-serif">
<text x="60" y="60" font-size="30" font-weight="700" fill="#0B4F47">Real monthly US search volume</text>
<text x="60" y="95" font-size="22" fill="#555">patient-facing searches, pulled from Ubersuggest</text>
<line x1="90" y1="{chart_bottom}" x2="1140" y2="{chart_bottom}" stroke="#999" stroke-width="2"/>
{bars1}
</svg>'''

with open("medical-seo-patient-demand.html", "w") as f:
    f.write(f"<html><body style='margin:0'>{svg1}</body></html>")

with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page(viewport={"width": W, "height": H})
    pg.goto("file://" + __import__("os").path.abspath("medical-seo-patient-demand.html"))
    pg.screenshot(path="medical-seo-patient-demand.png")
    br.close()
print("chart 1 ok")
