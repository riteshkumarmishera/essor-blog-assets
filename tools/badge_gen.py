import random
from playwright.sync_api import sync_playwright

W, H = 1536, 864
OUT = "./"  # output folder; run from a scratch dir

# ---- icon library (viewBox 0 0 100 100), bold filled shapes ----
def magnifier(d, a):
    return f'''<circle cx="42" cy="42" r="24" fill="none" stroke="{d}" stroke-width="10"/>
<circle cx="42" cy="42" r="14" fill="{a}" opacity=".35"/>
<rect x="60" y="56" width="14" height="34" rx="7" fill="{d}" transform="rotate(-45 67 73)"/>'''

def sun(d, a):
    rays = "".join(
        f'<rect x="46" y="6" width="8" height="18" rx="4" fill="{a}" transform="rotate({i*45} 50 50)"/>'
        for i in range(8))
    return rays + f'<circle cx="50" cy="50" r="20" fill="{a}"/>'

def pump_bottle(d, a):
    return f'''<rect x="44" y="8" width="26" height="9" rx="4" fill="{d}"/>
<rect x="64" y="8" width="16" height="6" rx="3" fill="{d}"/>
<rect x="45" y="16" width="10" height="14" fill="{d}"/>
<rect x="30" y="30" width="40" height="62" rx="12" fill="{a}"/>
<rect x="38" y="50" width="24" height="18" rx="5" fill="#FFFFFF" opacity=".85"/>'''

def spine(d, a):
    xs = [50, 46, 44, 46, 52]
    ws = [26, 30, 34, 38, 42]
    out = ""
    for i, (x, w) in enumerate(zip(xs, ws)):
        y = 8 + i * 17
        out += f'<rect x="{x - w/2}" y="{y}" width="{w}" height="12" rx="6" fill="{d}"/>'
        if i < 4:
            out += f'<rect x="{x - w/2 + 6}" y="{y + 12}" width="{w - 12}" height="5" rx="2.5" fill="{a}"/>'
    return out

def table(d, a):
    return f'''<rect x="10" y="44" width="80" height="14" rx="7" fill="{d}"/>
<path d="M14 44 Q14 30 30 30 L34 30 L34 44 Z" fill="{a}"/>
<rect x="22" y="58" width="9" height="30" rx="4" fill="{d}"/>
<rect x="69" y="58" width="9" height="30" rx="4" fill="{d}"/>
<rect x="26" y="74" width="48" height="7" rx="3.5" fill="{d}"/>'''

def calendar(d, a):
    return f'''<rect x="12" y="18" width="76" height="70" rx="12" fill="{d}"/>
<rect x="12" y="18" width="76" height="22" rx="12" fill="{a}"/>
<rect x="12" y="30" width="76" height="10" fill="{a}"/>
<rect x="28" y="8" width="9" height="20" rx="4.5" fill="{d}"/>
<rect x="63" y="8" width="9" height="20" rx="4.5" fill="{d}"/>
<path d="M32 62 L45 74 L70 50" fill="none" stroke="#FFFFFF" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'''

def roller(d, a):
    return f'''<rect x="10" y="10" width="62" height="26" rx="13" fill="{a}"/>
<rect x="10" y="10" width="62" height="10" rx="5" fill="#FFFFFF" opacity=".35"/>
<path d="M72 23 L84 23 L84 48 L50 48 L50 58" fill="none" stroke="{d}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>
<rect x="43" y="56" width="14" height="36" rx="7" fill="{d}"/>'''

def swatches(d, a):
    return f'''<rect x="22" y="14" width="30" height="72" rx="8" fill="#C9B6EC" transform="rotate(-22 37 86)"/>
<rect x="35" y="12" width="30" height="72" rx="8" fill="{a}" transform="rotate(-4 50 84)"/>
<rect x="48" y="14" width="30" height="72" rx="8" fill="{d}" transform="rotate(16 63 86)"/>
<circle cx="64" cy="74" r="5" fill="#FFFFFF"/>'''

def cabinet(d, a):
    return f'''<rect x="12" y="12" width="76" height="70" rx="8" fill="{d}"/>
<rect x="19" y="19" width="29" height="56" rx="4" fill="{a}"/>
<rect x="52" y="19" width="29" height="56" rx="4" fill="{a}"/>
<rect x="40" y="38" width="5" height="16" rx="2.5" fill="{d}"/>
<rect x="55" y="38" width="5" height="16" rx="2.5" fill="{d}"/>
<rect x="18" y="82" width="64" height="8" rx="3" fill="{d}" opacity=".7"/>'''

def stethoscope(d, a):
    return f'''<path d="M26 10 L26 38 Q26 56 44 56 Q62 56 62 38 L62 10" fill="none" stroke="{d}" stroke-width="9" stroke-linecap="round"/>
<circle cx="26" cy="8" r="7" fill="{d}"/>
<circle cx="62" cy="8" r="7" fill="{d}"/>
<path d="M44 56 L44 72" fill="none" stroke="{d}" stroke-width="9" stroke-linecap="round"/>
<circle cx="44" cy="84" r="15" fill="{a}"/>
<circle cx="44" cy="84" r="7" fill="{d}" opacity=".5"/>'''

def medical_cross(d, a):
    return f'''<rect x="8" y="8" width="84" height="84" rx="20" fill="{a}"/>
<rect x="38" y="20" width="24" height="60" rx="8" fill="{d}"/>
<rect x="20" y="38" width="60" height="24" rx="8" fill="{d}"/>'''

def clipboard_chart(d, a):
    return f'''<rect x="18" y="12" width="64" height="80" rx="10" fill="{d}"/>
<rect x="34" y="6" width="32" height="14" rx="6" fill="{a}"/>
<rect x="28" y="34" width="44" height="42" rx="6" fill="#FFFFFF" opacity=".9"/>
<polyline points="34,62 44,50 52,58 64,42" fill="none" stroke="{a}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'''

def map_pin(d, a):
    return f'''<path d="M50 8 C28 8 12 24 12 46 C12 68 50 92 50 92 C50 92 88 68 88 46 C88 24 72 8 50 8 Z" fill="{d}"/>
<circle cx="50" cy="46" r="18" fill="{a}"/>
<circle cx="50" cy="46" r="7" fill="#FFFFFF"/>'''

def shield_check(d, a):
    return f'''<path d="M50 6 L86 20 L86 48 C86 72 68 86 50 94 C32 86 14 72 14 48 L14 20 Z" fill="{d}"/>
<path d="M33 50 L46 63 L68 36" fill="none" stroke="{a}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'''

def id_card(d, a):
    return f'''<rect x="8" y="22" width="84" height="58" rx="10" fill="{d}"/>
<circle cx="32" cy="48" r="12" fill="{a}"/>
<rect x="22" y="62" width="20" height="8" rx="4" fill="{a}"/>
<rect x="54" y="38" width="30" height="7" rx="3.5" fill="{a}"/>
<rect x="54" y="52" width="24" height="7" rx="3.5" fill="{a}"/>'''

def magnifier_question(d, a):
    return f'''<circle cx="40" cy="40" r="26" fill="none" stroke="{d}" stroke-width="10"/>
<text x="40" y="52" font-size="34" font-weight="800" fill="{d}" text-anchor="middle" font-family="Arial">?</text>
<rect x="58" y="58" width="14" height="32" rx="7" fill="{d}" transform="rotate(-45 65 74)"/>'''

def funnel(d, a):
    return f'''<polygon points="10,10 90,10 65,55 65,90 35,90 35,55" fill="{d}"/>
<rect x="30" y="20" width="40" height="8" rx="4" fill="{a}"/>
<rect x="38" y="40" width="24" height="8" rx="4" fill="{a}"/>'''

def chat_bubble(d, a):
    return f'''<path d="M10 20 Q10 10 20 10 L80 10 Q90 10 90 20 L90 58 Q90 68 80 68 L34 68 L18 86 L22 68 L20 68 Q10 68 10 58 Z" fill="{d}"/>
<circle cx="32" cy="38" r="6" fill="{a}"/>
<circle cx="50" cy="38" r="6" fill="{a}"/>
<circle cx="68" cy="38" r="6" fill="{a}"/>'''

def badge(svg, left, top, rot, z):
    return f'''<div class="badge" style="left:{left}px;top:{top}px;transform:rotate({rot}deg);z-index:{z}">
<svg viewBox="0 0 100 100">{svg}</svg></div>'''

def page(bg1, bg2, blob, icons, confetti_colors, seed):
    random.seed(seed)
    dots = ""
    for _ in range(26):
        x, y = random.randint(20, W - 20), random.randint(20, H - 20)
        if 300 < x < 1240 and 140 < y < 720:
            continue
        s = random.choice([7, 9, 11, 13])
        c = random.choice(confetti_colors)
        dots += f'<div class="dot" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c}"></div>'
    b = (badge(icons[0], 250, 330, -9, 2) +
         badge(icons[1], 618, 150, 4, 1) +
         badge(icons[2], 980, 320, 8, 3))
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0}}
.c{{width:{W}px;height:{H}px;position:relative;overflow:hidden;background:linear-gradient(135deg,{bg1},{bg2})}}
.blob{{position:absolute;border-radius:50%;background:{blob}}}
.dot{{position:absolute;border-radius:50%}}
.badge{{position:absolute;width:310px;height:310px;border-radius:68px;background:#fff;
box-shadow:0 28px 60px rgba(0,0,0,.28);display:flex;align-items:center;justify-content:center}}
.badge svg{{width:200px;height:200px}}
</style></head><body><div class="c">
<div class="blob" style="width:620px;height:620px;left:-200px;top:-260px"></div>
<div class="blob" style="width:700px;height:700px;right:-220px;bottom:-330px"></div>
<div class="blob" style="width:220px;height:220px;left:760px;top:600px;opacity:.6"></div>
{dots}{b}</div></body></html>'''

designs = {
    "local-seo-for-dermatologists-featured-v3": dict(
        bg1="#EC6A8E", bg2="#D4436C", blob="rgba(255,255,255,.13)",
        icons=[magnifier("#7A1638", "#7A1638"), sun("#7A1638", "#F5A524"), pump_bottle("#7A1638", "#E2557C")],
        conf=["#FFFFFF", "#FFD27A", "#7A1638"], seed=3),
    "chiropractor-seo-featured-v5": dict(
        bg1="#3A9BE0", bg2="#1F74BE", blob="rgba(255,255,255,.13)",
        icons=[spine("#0F3D6B", "#F5A524"), table("#0F3D6B", "#3A9BE0"), calendar("#0F3D6B", "#F5A524")],
        conf=["#FFFFFF", "#FFD27A", "#0F3D6B"], seed=5),
    "seo-for-remodelers-featured-v4": dict(
        bg1="#8B5CD6", bg2="#6A3BB5", blob="rgba(255,255,255,.12)",
        icons=[roller("#3E1C78", "#F5B942"), swatches("#3E1C78", "#F5B942"), cabinet("#3E1C78", "#B794F0")],
        conf=["#FFFFFF", "#FFD27A", "#3E1C78"], seed=8),
    "medical-seo-featured-v1": dict(
        bg1="#17B3A3", bg2="#0E8C7F", blob="rgba(255,255,255,.14)",
        icons=[stethoscope("#0B4F47", "#F5A524"), medical_cross("#0B4F47", "#E25C5C"), clipboard_chart("#0B4F47", "#F5A524")],
        conf=["#FFFFFF", "#FFD27A", "#0B4F47"], seed=21),
    "local-seo-for-doctors-featured-v1": dict(
        bg1="#4C6FFF", bg2="#3450C7", blob="rgba(255,255,255,.14)",
        icons=[map_pin("#1E2E7A", "#F5A524"), shield_check("#1E2E7A", "#38D17A"), id_card("#1E2E7A", "#F5A524")],
        conf=["#FFFFFF", "#FFD27A", "#1E2E7A"], seed=33),
    "keyword-research-healthcare-featured-v1": dict(
        bg1="#F2994A", bg2="#D4722A", blob="rgba(255,255,255,.14)",
        icons=[magnifier_question("#6B3414", "#6B3414"), funnel("#6B3414", "#FFFFFF"), chat_bubble("#6B3414", "#FFFFFF")],
        conf=["#FFFFFF", "#FFD27A", "#6B3414"], seed=47),
}

with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page(viewport={"width": W, "height": H})
    for name, d in designs.items():
        html = page(d["bg1"], d["bg2"], d["blob"], d["icons"], d["conf"], d["seed"])
        open(OUT + name + ".html", "w").write(html)
        pg.set_content(html)
        pg.screenshot(path=OUT + name + ".png")
    br.close()
print("ok")
