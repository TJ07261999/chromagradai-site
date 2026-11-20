"""Build the ChromaGrad AI site into docs/ (served by GitHub Pages).

Legal pages come from src/{terms,privacy,terms-en,privacy-en}.html, which are HTML exports of the
Claude Docs (Tab 1 = Japanese, English tab = English). Re-export them and run: python3 build.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SRC, OUT = ROOT / "src", ROOT / "docs"
SITE = "https://www.chromagradai.com"
MAIL = "info@chromagradai.com"

FOOTER = f"""<footer class="site-footer band-greige">
  <div class="foot-top"><a class="foot-logo" href="./">ChromaGrad AI</a><a class="foot-mail" href="mailto:{MAIL}">{MAIL}</a></div>
  <div class="foot-links">
    <ul lang="ja"><li><a href="about">会社概要</a></li><li><a href="contact">お問い合わせ</a></li><li><a href="privacy">プライバシーポリシー</a></li><li><a href="terms">利用規約</a></li></ul>
    <ul lang="en"><li><a href="about-en">About</a></li><li><a href="contact-en">Contact</a></li><li><a href="privacy-en">Privacy Policy</a></li><li><a href="terms-en">Terms of Service</a></li></ul>
  </div>
  <p class="copyright">© 2026 ChromaGrad AI, LLC</p>
</footer>"""


def page(slug, lang, title, desc, body, alt):
    home = "./" if lang == "ja" else "english"
    path = "" if slug == "index" else slug
    ja_cur, en_cur = (' aria-current="true"', "") if lang == "ja" else ("", ' aria-current="true"')
    alt_ja, alt_en = (path, alt) if lang == "ja" else (alt, path)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{path}">
<link rel="alternate" hreflang="ja" href="{SITE}/{alt_ja}">
<link rel="alternate" hreflang="en" href="{SITE}/{alt_en}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/{path}">
<meta property="og:locale" content="{'ja_JP' if lang == 'ja' else 'en_US'}">
<meta name="theme-color" content="#e0e0db">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">{'本文へ移動' if lang == 'ja' else 'Skip to content'}</a>
<header class="site-header band-greige">
  <a class="logo" href="{home}">ChromaGrad AI</a>
  <nav class="lang" aria-label="Language"><a href="./" lang="ja"{ja_cur}>日本語</a><a href="english" lang="en"{en_cur}>English</a></nav>
</header>
<main id="main">
{body}
</main>
{FOOTER}
</body>
</html>
"""


def phone(tip):
    return f'<div class="art art-cool art-tall" aria-hidden="true"><div class="phone"><div class="screen"><span class="tip">{tip}</span><span class="rec"></span></div></div></div>'


def home(t):
    promises = "\n".join(
        f'<details{" open" if i == 0 else ""}><summary>{h}</summary><p>{p}</p></details>' for i, (h, p) in enumerate(t["promises"])
    )
    return f"""<section class="hero band-greige"><div class="hero-art"><h1>{t['hero']}</h1></div></section>
<section class="split band-greige">
  <div class="art art-warm" aria-hidden="true"></div>
  <div class="copy"><h2 class="display">{t['lead_h']}</h2><p>{t['lead_p']}</p><a class="btn" href="{t['lead_btn'][1]}">{t['lead_btn'][0]}</a></div>
</section>
<section class="split band-white">
  <div class="copy"><h2 class="h2">{t['prod_h']}</h2><p>{t['prod_p']}</p><a class="btn" href="{t['prod_btn'][1]}">{t['prod_btn'][0]}</a></div>
  {phone(t['tip'])}
</section>
<section class="split band-white">
  <div class="copy"><h2 class="h2">{t['prom_h']}</h2><p>{t['prom_p']}</p><a class="btn btn-outline" href="{t['prom_btn'][1]}">{t['prom_btn'][0]}</a></div>
  <div class="accordion">
{promises}
  </div>
</section>"""


HOME_JA = dict(
    hero="映像の力を、<br>AI でだれの手にも。",
    lead_h="プロの技を、<br>スマホ1台に。",
    lead_p="ChromaGrad AI は、動画の企画・撮影・編集を AI で支えるソフトウェアをつくる会社です。伝わる動画には、企画、撮影、編集のそれぞれに経験と時間がかかります。私たちはそのノウハウを AI に込めて、だれでもスマホ1台で伝わる映像をつくれるようにします。",
    lead_btn=("会社概要を見る", "about"),
    prod_h="最初のプロダクト<br>「撮影アシスト」",
    prod_p="企画とカット割りの相談、撮影中の案内、編集とテロップ付けまでを手伝う iPhone・iPad 用のアプリです。お客様の動画を AI の学習に使うことはなく、作った動画の権利はお客様に残ります。App Store で近日公開予定です。",
    prod_btn=("お問い合わせ", "contact"),
    tip="もう一歩さがると、全身が入ります",
    prom_h="私たちの約束",
    prom_p="お客様の動画には、ご本人や一緒に写る人の大切な情報が含まれます。だからこそ私たちは、動画の扱い方をはっきり決めて、公開しています。",
    prom_btn=("詳しく見る", "privacy"),
    promises=[
        ("動画を AI の学習に使いません", "お客様の動画、声、文章を、AI の学習にも広告にも使いません。AI の処理を任せる事業者にも、学習に使わない契約や設定で送っています。"),
        ("送る前に、必ず同意をいただきます", "動画を外部の AI に送る前に、アプリの中で同意をいただきます。同意は、いつでも取り消せます。取り消しても、端末の中だけで動く機能はそのまま使えます。"),
        ("期限を決めて、データを消します", "作品を消すと、サーバーにあるデータも消えます。残ったものも、最後の処理から30日で自動的に消します。作った動画の権利は、お客様に残ります。"),
    ],
)
HOME_EN = dict(
    hero="The power of video,<br>in everyone’s hands.",
    lead_h="Pro skills,<br>in your pocket.",
    lead_p="ChromaGrad AI builds software that uses AI to help people plan, shoot, and edit video. A video that truly connects takes experience and time at every stage, from planning to shooting to editing. We’re building that know-how into AI, so anyone can make compelling video with nothing more than a smartphone.",
    lead_btn=("About us", "about-en"),
    prod_h="Our first product:<br>Shoot Assist",
    prod_p="Shoot Assist is an app for iPhone and iPad that supports you from start to finish: it helps you plan your video and shot list, guides you while you film, and handles editing and captions. We never use your videos to train AI, and you keep all rights to what you create. Coming soon to the App Store.",
    prod_btn=("Contact us", "contact-en"),
    tip="Take one step back to fit your whole body in the frame",
    prom_h="Our commitments",
    prom_p="Your videos hold personal information about you and the people who appear in them. That’s why we’ve set clear rules for how we handle them, and we make those rules public.",
    prom_btn=("Learn more", "privacy-en"),
    promises=[
        ("We never use your videos to train AI", "We don’t use your videos, voice, or text to train AI, and we don’t use them for advertising. When outside providers handle AI processing for us, we send your data only under terms and settings that keep it out of model training."),
        ("We ask for your consent before sending anything", "Before any video is sent to an outside AI service, we ask for your consent in the app. You can withdraw it at any time, and features that run entirely on your device will keep working."),
        ("We delete your data on a set schedule", "When you delete a project, its data is deleted from our servers too. Anything left behind is deleted automatically 30 days after it was last processed. You keep all rights to the videos you create."),
    ],
)


def about(h1, intro, rows):
    dl = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows)
    return f"""<section class="page band-greige"><div class="split">
  <div class="copy"><h1>{h1}</h1><p>{intro}</p><dl class="info">{dl}</dl></div>
  <div class="art art-mist art-tall" aria-hidden="true"></div>
</div></section>"""


def contact(h1, intro, btn):
    return f"""<section class="page band-greige"><div class="split">
  <div class="copy"><h1>{h1}</h1><p>{intro}</p><a class="mail-big" href="mailto:{MAIL}">{MAIL}</a><br><a class="btn" href="mailto:{MAIL}">{btn}</a></div>
  <div class="art art-dusk art-tall" aria-hidden="true"></div>
</div></section>"""


MAILTO = f'<a href="mailto:{MAIL}">{MAIL}</a>'
ADDR = "9344 National Blvd. Unit 14, Los Angeles, California 90034, United States"

REFS = {
    "terms": '<p class="note">参考：<a href="https://policies.google.com/terms/generative-ai/use-policy">Google「Generative AI Prohibited Use Policy」</a>／<a href="https://elevenlabs.io/use-policy">ElevenLabs「Prohibited Use Policy」</a></p>',
    "terms-en": '<p class="note">References: <a href="https://policies.google.com/terms/generative-ai/use-policy">Google’s “Generative AI Prohibited Use Policy”</a> / <a href="https://elevenlabs.io/use-policy">ElevenLabs’ “Prohibited Use Policy”</a></p>',
}


def legal(key, switch):
    html = (SRC / f"{key}.html").read_text(encoding="utf-8")
    m = re.match(r"\s*<h1[^>]*>(.*?)</h1>\s*", html, re.S)
    title, body = m.group(1), html[m.end():]
    if key in REFS:  # links promised by Article 8 ("links are provided ... on our website")
        art8 = re.search(r"<h2[^>]*>(第8条|Article 8 )", body)
        end = body.index("</ol>", art8.end()) + len("</ol>")
        body = body[:end] + "\n" + REFS[key] + body[end:]
    body = re.sub(r"<table>", '<div class="table-wrap"><table>', body).replace("</table>", "</table></div>")
    return title, f'<section class="legal band-white"><article class="doc">\n<h1>{title}</h1>\n<p class="lang-switch">{switch}</p>\n{body}</article></section>'


def build():
    pages = {
        "index": ("ja", "ChromaGrad AI — 動画の企画・撮影・編集を AI で", "ChromaGrad AI は、動画の企画・撮影・編集を AI で支えるソフトウェアをつくる会社です。最初のプロダクトは、iPhone・iPad 用アプリ「撮影アシスト」です。", home(HOME_JA), "english"),
        "english": ("en", "AI for planning, shooting, and editing video — ChromaGrad AI", "ChromaGrad AI builds software that helps anyone plan, shoot, and edit video with AI. Our first product is Shoot Assist, an app for iPhone and iPad.", home(HOME_EN), ""),
        "about": ("ja", "会社概要 — ChromaGrad AI", "ChromaGrad AI, LLC の会社概要です。米国ロサンゼルスを拠点に、動画の企画・撮影・編集を AI で支える iPhone・iPad 用アプリ「撮影アシスト」を開発しています。",
                  about("会社概要", "ChromaGrad AI は、動画の企画・撮影・編集を AI で支えるソフトウェアをつくる会社です。米国カリフォルニア州ロサンゼルスを拠点に、iPhone・iPad 用アプリ「撮影アシスト」を開発しています。",
                        [("会社名", "ChromaGrad AI, LLC"), ("所在地", ADDR), ("代表者", "宮地 綸（Member）"), ("事業内容", "AI を使った動画制作アプリ「撮影アシスト」の開発と運営"), ("お問い合わせ", MAILTO)]), "about-en"),
        "about-en": ("en", "About us — ChromaGrad AI", "About ChromaGrad AI, LLC. Based in Los Angeles, we build Shoot Assist, an iPhone and iPad app that uses AI to help people plan, shoot, and edit video.",
                     about("About us", "ChromaGrad AI builds software that uses AI to help people plan, shoot, and edit video. Based in Los Angeles, California, we’re developing Shoot Assist, an app for iPhone and iPad.",
                           [("Company", "ChromaGrad AI, LLC"), ("Address", ADDR), ("Representative", "Tsukasa Miyaji (Member)"), ("Business", "Development and operation of Shoot Assist, an AI-powered video creation app"), ("Contact", MAILTO)]), "about"),
        "contact": ("ja", "お問い合わせ — ChromaGrad AI", "撮影アシストについてのご質問や、取材・協業のご相談は、こちらのメールアドレスへお寄せください。",
                    contact("お問い合わせ", "撮影アシストについてのご質問や、取材・協業のご相談は、メールでお気軽にお寄せください。", "メールを送る"), "contact-en"),
        "contact-en": ("en", "Contact us — ChromaGrad AI", "Questions about Shoot Assist, press inquiries, or partnership ideas? Get in touch with ChromaGrad AI by email.",
                       contact("Contact us", "Have a question about Shoot Assist, or want to talk about press or partnerships? Email us anytime.", "Email us"), "contact"),
    }
    for key, lang, alt, switch in [
        ("terms", "ja", "terms-en", '<a href="terms-en" lang="en">English version</a>'),
        ("privacy", "ja", "privacy-en", '<a href="privacy-en" lang="en">English version</a>'),
        ("terms-en", "en", "terms", '<a href="terms" lang="ja">日本語版</a>'),
        ("privacy-en", "en", "privacy", '<a href="privacy" lang="ja">日本語版</a>'),
    ]:
        title, body = legal(key, switch)
        short = {"terms": "利用規約", "privacy": "プライバシーポリシー", "terms-en": "Terms of Service", "privacy-en": "Privacy Policy"}[key]
        pages[key] = (lang, f"{short} — ChromaGrad AI", re.sub("<[^>]+>", "", title), body, alt)

    for slug, (lang, title, desc, body, alt) in pages.items():
        (OUT / f"{slug}.html").write_text(page(slug, lang, title, desc, body, alt), encoding="utf-8")

    # ponytail: tiny self-check — every relative link must point at a page we just wrote
    names = {p.stem for p in OUT.glob("*.html")} | {""}
    for f in OUT.glob("*.html"):
        for href in re.findall(r'href="(?!/)([^"#:]+)"', f.read_text(encoding="utf-8")):  # root-absolute ones live only in 404.html
            target = href.lstrip("./").removesuffix(".html")
            assert target in names or (OUT / href).exists(), f"{f.name}: broken link {href}"
    print("built", len(pages), "pages; links ok")


if __name__ == "__main__":
    build()
