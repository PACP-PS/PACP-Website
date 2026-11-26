# -*- coding: utf-8 -*-
"""Generate the English edition under DEST/en/ from the built Arabic pages."""
import re, html
from pathlib import Path
from en_translations import T

AR = re.compile(r"[؀-ۿ]")
INNER = "PACP-Reference-Design-Cloudflare-v9"
PAGES = ["about", "auth", "contact", "membership", "news", "portal", "resources", "training", "verify"]
EN_PAGES = set(PAGES)
KEYS = sorted(T, key=len, reverse=True)

LANG_CSS = (
    "<style id='pacp-lang-style'>.pacp-lang{position:fixed;top:12px;inset-inline-end:12px;z-index:9999;"
    "background:#0a5c3e;color:#fff!important;font:700 13px Alexandria,system-ui,sans-serif;padding:7px 14px;"
    "border-radius:99px;text-decoration:none;box-shadow:0 4px 14px #0a5c3e40;direction:ltr}"
    ".pacp-lang:hover{background:#c4122f}</style>"
)
EN_CSS = (
    "<style id='pacp-en-style'>html[dir=ltr] body{text-align:left}"
    "html[dir=ltr]{font-family:Alexandria,system-ui,sans-serif}"
    "html[dir=ltr] .links,html[dir=ltr] .nav{direction:ltr}"
    "html[dir=ltr] dl{text-align:left}html[dir=ltr] .hero-copy{text-align:left}"
    "html[dir=ltr] h1,html[dir=ltr] h2,html[dir=ltr] h3{letter-spacing:0;line-height:1.25}"
    "html[dir=ltr] .brand small{letter-spacing:0}</style>"
)


def tr_text(s):
    """Translate a text/attribute value if its stripped, unescaped form is a known key."""
    raw = html.unescape(s)
    core = raw.strip()
    if core in T:
        lead = raw[: len(raw) - len(raw.lstrip())]
        trail = raw[len(raw.rstrip()):]
        return lead + T[core] + trail
    return None


def esc_text(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def esc_attr(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")


def translate_markup(t, left):
    """Translate text nodes and attributes outside <script>/<style>; `left` collects misses."""
    parts = re.split(r"(<script[^>]*>.*?</script>|<style[^>]*>.*?</style>)", t, flags=re.S)
    out = []
    for p in parts:
        if p.startswith("<script"):
            out.append(translate_script(p, left))
            continue
        if p.startswith("<style"):
            out.append(p)
            continue

        def attr(m):
            v = m.group(3) if m.group(3) is not None else m.group(4)
            if not AR.search(v):
                return m.group(0)
            r = tr_text(v)
            if r is None:
                left.append(("attr", html.unescape(v)))
                return m.group(0)
            return f'{m.group(1)}{m.group(2)}="{esc_attr(r)}"'

        p = re.sub(r"""(\s)((?:alt|title|aria-label|placeholder|content|value))=(?:"([^"]*)"|'([^']*)')""", attr, p)

        def node(m):
            v = m.group(1)
            if not AR.search(v):
                return m.group(0)
            r = tr_text(v)
            if r is None:
                left.append(("text", html.unescape(v).strip()))
                return m.group(0)
            return ">" + esc_text(r) + "<"

        p = re.sub(r">([^<]+)<", node, p)
        out.append(p)
    return "".join(out)


def translate_script(s, left):
    for k in KEYS:
        if k in s:
            s = s.replace(k, T[k])
    for m in re.findall(r"[^\n]{0,30}[؀-ۿ][^\n]{0,30}", s):
        left.append(("script", m))
    return s


def to_absolute(t):
    t = t.replace('src="../../assets/', f'src="/{INNER}/assets/')
    t = t.replace('href="../assets/pacp-shared-theme.css"', f'href="/{INNER}/design/assets/pacp-shared-theme.css"')
    t = t.replace("'../assets/pacp-supabase-auth.mjs'", f"'/{INNER}/design/assets/pacp-supabase-auth.mjs'")
    t = t.replace("'card.html?'", f"'/{INNER}/design/pages/card.html?'")
    t = t.replace("toLocaleDateString('ar')", "toLocaleDateString('en-GB')")
    return t


def rewrite_links(t):
    # absolute links to translated pages -> /en/...
    for n in EN_PAGES:
        t = t.replace(f'href="/{INNER}/design/pages/{n}.html', f'href="/en/{INNER}/design/pages/{n}.html')
    return t


def build(dest):
    dest = Path(dest)
    left = []
    jobs = [("index.html", "en/index.html", "/", "/en/")]
    for n in PAGES:
        rel = f"{INNER}/design/pages/{n}.html"
        jobs.append((rel, "en/" + rel, "/" + rel, "/en/" + rel))
    for src, dst, ar_url, en_url in jobs:
        t = (dest / src).read_text(encoding="utf8")
        if src == "index.html":
            t = re.sub(r"getElementById\('lang'\)\.addEventListener\('click',\(\)=>alert\([^)]*\)\);",
                       "getElementById('lang').addEventListener('click',()=>{location.href='/'});", t)
        t = to_absolute(t)
        t = rewrite_links(t)
        t = translate_markup(t, left)
        t = t.replace('<html lang="ar" dir="rtl">', '<html lang="en" dir="ltr">', 1)
        alt = (f'<link rel="alternate" hreflang="ar" href="https://www.pacp.ps{ar_url}">'
               f'<link rel="alternate" hreflang="en" href="https://www.pacp.ps{en_url}">')
        pill = f'<a class="pacp-lang" href="{ar_url}" lang="ar" hreflang="ar">العربية</a>'
        if src == "index.html":
            # the page already has an EN button -> turn into AR switch
            t = re.sub(r"getElementById\('lang'\)\.addEventListener\('click',\(\)=>alert\([^)]*\)\);",
                       "getElementById('lang').addEventListener('click',()=>{location.href='/'});", t)
            t = t.replace("EN 🌐</button>", "العربية 🌐</button>")
            pill = ""
        t = t.replace("</head>", alt + LANG_CSS + EN_CSS + "</head>", 1)
        if pill:
            t = t.replace("<body>", "<body>" + pill, 1) if "<body>" in t else t.replace("</body>", pill + "</body>", 1)
        (dest / dst).parent.mkdir(parents=True, exist_ok=True)
        (dest / dst).write_text(t, encoding="utf8")

        # Arabic page: add switch to English + hreflang
        a = (dest / src).read_text(encoding="utf8")
        if "pacp-lang-style" not in a:
            apill = "" if src == "index.html" else f'<a class="pacp-lang" href="{en_url}" lang="en" hreflang="en">English</a>'
            a = a.replace("</head>", alt + LANG_CSS + "</head>", 1)
            if src == "index.html":
                a = re.sub(r"getElementById\('lang'\)\.addEventListener\('click',\(\)=>alert\([^)]*\)\);",
                           "getElementById('lang').addEventListener('click',()=>{location.href='/en/'});", a)
                a = a.replace('title="النسخة الإنجليزية قيد الإعداد"', 'title="English version"')
            elif apill:
                a = a.replace("<body>", "<body>" + apill, 1) if "<body>" in a else a.replace("</body>", apill + "</body>", 1)
            (dest / src).write_text(a, encoding="utf8")
    return left
