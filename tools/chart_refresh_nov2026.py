"""Regenerate keyword-demand charts so they match each post's current Ubersuggest table (Nov 2026)."""
from playwright.sync_api import sync_playwright

SUB = "Real US monthly searches and difficulty (KD, 0 to 100) from Ubersuggest, November 2026"

CHARTS = {
    "chiropractor-seo-real-demand-2026": ("What patients search for, by condition", SUB, "vol", [
        ("pediatric chiropractor near me", 12100, None), ("prenatal chiropractor near me", 8100, None),
        ("auto accident chiropractor near me", 4400, None), ("sciatica chiropractor near me", 2400, None),
        ("chiropractor near me that take insurance", 2400, None), ("back pain chiropractor near me", 1600, None)]),
    "roofing-seo-guide-real-demand-2026": ("What homeowners search when they need a roofer", SUB, "vol", [
        ("roofer near me", 165000, 58), ("roofing companies near me", 165000, 27), ("roof repair near me", 90500, 15),
        ("roof leak repair", 27100, 25), ("roof replacement cost", 18100, 23), ("roof inspection near me", 12100, 12)]),
    "self-storage-seo-real-demand-2026": ("What renters search when they need storage", SUB, "vol", [
        ("storage units near me", 1000000, 76), ("storage near me", 368000, 18), ("rv storage near me", 135000, 15),
        ("cheap storage units near me", 49500, 37), ("climate controlled storage units", 40500, 16), ("boat storage near me", 33100, 36)]),
    "acupuncturist-seo-real-difficulty-2026": ("How hard each patient search is to rank for",
        "SEO difficulty (KD, 0 to 100) from Ubersuggest, November 2026. Google withholds volume for most acupuncture terms.", "kd", [
        ("fertility acupuncturist near me", 4, None), ("acupuncture near me", 12, None), ("cupping near me", 23, None),
        ("acupuncturist near me that take insurance", 25, None), ("acupuncturist near me", 37, None), ("acupuncture for back pain", 53, None)]),
    "pool-builder-seo-real-demand-2026": ("What pool buyers search before they call", SUB, "vol", [
        ("pool contractors near me", 18100, 22), ("inground pool cost", 18100, 26), ("pool builders near me", 14800, 54),
        ("pool remodeling near me", 6600, 23), ("pool resurfacing near me", 4400, 10), ("inground pool installation near me", 1600, 38)]),
    "seo-for-landscapers-real-demand-2026": ("What homeowners search for yard work", SUB, "vol", [
        ("landscaping near me", 135000, 27), ("lawn care near me", 74000, 27), ("lawn mowing service near me", 49500, 40),
        ("landscaper near me", 40500, 38), ("landscape design near me", 14800, 27), ("hardscaping near me", 9900, 32)]),
    "hvac-local-seo-real-demand-2026": ("What homeowners search when the AC or furnace fails", SUB, "vol", [
        ("ac repair near me", 201000, 11), ("hvac companies near me", 110000, 57), ("furnace repair near me", 74000, 25),
        ("hvac repair near me", 49500, 25), ("ac replacement", 14800, 34), ("ac replacement cost", 9900, 12)]),
    "fence-real-demand-2026": ("What homeowners search when they want a fence", SUB, "vol", [
        ("fence company near me", 165000, 20), ("fence installer near me", 33100, 62), ("chain link fence installation cost", 18100, 28),
        ("fence repair near me", 14800, 18), ("vinyl fence installer", 9900, 23), ("wood fence installation cost", 9900, 24)]),
    "dry-cleaner-real-demand-2026": ("What customers search for dry cleaning and alterations", SUB, "vol", [
        ("dry cleaners near me", 673000, 27), ("alterations near me", 368000, 11), ("24 hour dry cleaner near me", 5400, 14),
        ("wedding dress cleaning", 4400, 16), ("same day dry cleaning", 4400, 22), ("eco friendly dry cleaner near me", 1600, 14)]),
    "house-cleaning-real-demand-2026": ("What homeowners search when hiring a cleaner", SUB, "vol", [
        ("maid service near me", 110000, 25), ("house cleaning service near me", 60500, 57), ("house cleaners near me", 60500, 59),
        ("deep cleaning service near me", 3600, 24), ("move out house cleaning service", 1600, 20), ("weekly house cleaning service", 1300, 36)]),
    "cleaning-company-seo-real-demand-2026": ("What homes and offices search for cleaning", SUB, "vol", [
        ("cleaning services near me", 110000, 21), ("carpet cleaning near me", 110000, 27), ("window cleaning near me", 74000, 7),
        ("commercial cleaning services near me", 27100, 21), ("janitorial services near me", 14800, 28), ("office cleaning company near me", 3600, 25)]),
    "contractor-homeowner-search-demand-2026": ("What homeowners search when hiring a contractor", SUB, "vol", [
        ("general contractor near me", 135000, 27), ("contractors near me", 135000, 27), ("construction companies near me", 74000, 27),
        ("kitchen remodeling contractor", 60500, 22), ("home renovation contractors near me", 14800, 41), ("home addition contractors near me", 4400, 25)]),
}

W = 1200
BAR_LEFT, BAR_MAX = 470, 470
BAR_H, GAP, TOP = 46, 26, 140


def fmt(v):
    return f"{v:,}"


def render(name, title, sub, mode, rows):
    H = TOP + len(rows) * (BAR_H + GAP) + 30
    mx = 100 if mode == "kd" else max(r[1] for r in rows)
    svg = ""
    y = TOP
    for kw, val, kd in rows:
        w = max(val / mx * BAR_MAX, 8)
        if mode == "kd":
            color = "#14B8A6" if val <= 15 else ("#F5A524" if val <= 35 else "#E5484D")
            label = f"KD {val}"
        else:
            color = "#4C6FFF"
            label = f"{fmt(val)}/mo" + (f"  ·  KD {kd}" if kd is not None else "")
        svg += f'<text x="{BAR_LEFT-18}" y="{y+BAR_H/2+7}" font-size="19" font-weight="600" fill="#1E2240" text-anchor="end">{kw}</text>'
        svg += f'<rect x="{BAR_LEFT}" y="{y}" width="{w}" height="{BAR_H}" rx="8" fill="{color}"/>'
        svg += f'<text x="{BAR_LEFT+w+14}" y="{y+BAR_H/2+7}" font-size="20" font-weight="800" fill="#1E2240">{label}</text>'
        y += BAR_H + GAP
    legend = ""
    if mode == "kd":
        legend = ('<rect x="60" y="100" width="14" height="14" rx="3" fill="#14B8A6"/><text x="80" y="112" font-size="15" fill="#555">Easy (0-15)</text>'
                  '<rect x="190" y="100" width="14" height="14" rx="3" fill="#F5A524"/><text x="210" y="112" font-size="15" fill="#555">Moderate (16-35)</text>'
                  '<rect x="360" y="100" width="14" height="14" rx="3" fill="#E5484D"/><text x="380" y="112" font-size="15" fill="#555">Hard (36+)</text>')
    html = f'''<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0;font-family:Arial,Helvetica,sans-serif;background:#fff}}</style></head><body>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<rect width="{W}" height="{H}" fill="#ffffff"/>
<text x="60" y="52" font-size="28" font-weight="800" fill="#1E2240">{title}</text>
<text x="60" y="82" font-size="16" fill="#666">{sub}</text>
{legend}{svg}
</svg></body></html>'''
    return html, H


with sync_playwright() as p:
    br = p.chromium.launch()
    for name, (title, sub, mode, rows) in CHARTS.items():
        html, H = render(name, title, sub, mode, rows)
        pg = br.new_page(viewport={"width": W, "height": H}, device_scale_factor=1.5)
        pg.set_content(html)
        pg.screenshot(path=f"../images/{name}.jpg", type="jpeg", quality=88)
        pg.close()
    br.close()
print("ok", len(CHARTS))
