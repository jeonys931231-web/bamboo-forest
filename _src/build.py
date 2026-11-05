"""Build the stand-alone site from the artifact source and the site templates.

usage: build.py <artifact.html> <site_src dir> <out dir> <site url>

- index.html: the artifact fragment wrapped in a full document, with search metadata
  (title, description, canonical, Open Graph, structured data, verification tags) and config.js.
- about.html, robots.txt, sitemap.xml, llms.txt: rendered from site_src with the site address,
  so moving to another address later means changing one argument.
"""
import sys, json, html, datetime
from pathlib import Path

src_path, site_src, out_dir, site = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4].rstrip('/') + '/'
updated = datetime.date.today().isoformat()

NAME = '피부관리사 대나무숲'
ALT_NAMES = ['피부관리사 메타버스', '관리사 대나무숲']
INDEX_TITLE = '피부관리사 대나무숲 | 피부관리사 익명 메타버스'
INDEX_DESC = '피부관리사들이 마스크팩을 붙인 캐릭터로 대나무숲을 함께 걸으며 오늘 있었던 일을 익명으로 털어놓는 무료 메타버스. 회원가입 없이 폰과 PC에서 바로 들어와요.'
ABOUT_DESC = '피부관리사 대나무숲은 피부관리사들이 마스크팩을 붙인 캐릭터로 대나무숲을 함께 걸으며 오늘 있었던 일을 익명으로 털어놓는 무료 메타버스예요. 회원가입 없이 들어오고, 한 말은 10초 뒤 지워져요.'
APP_DESC = '피부관리사들이 마스크팩을 붙인 캐릭터로 대나무숲을 함께 걸으며 실시간으로 익명 대화를 나누는 무료 웹 메타버스. 한 말은 10초 뒤 서버에서 지워진다.'
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Crect width='64' height='64' rx='14' fill='%232E6C4B'/%3E"
           "%3Cellipse cx='32' cy='35' rx='19' ry='21' fill='%23D4EBD9'/%3E"
           "%3Cellipse cx='24.5' cy='31' rx='4.4' ry='2.8' fill='%232E6C4B'/%3E"
           "%3Cellipse cx='39.5' cy='31' rx='4.4' ry='2.8' fill='%232E6C4B'/%3E"
           "%3Cellipse cx='32' cy='44' rx='4.2' ry='2.1' fill='%232E6C4B'/%3E%3C/svg%3E")

verify = json.loads((site_src / 'verify.json').read_text(encoding='utf-8'))
VERIFY = '\n'.join(f'<meta name="{n}" content="{html.escape(v, quote=True)}">' for n, v in (
    ('google-site-verification', verify.get('google', '')),
    ('naver-site-verification', verify.get('naver', '')),
    ('msvalidate.01', verify.get('bing', ''))) if v)

website = {'@type': 'WebSite', '@id': site + '#website', 'name': NAME, 'alternateName': ALT_NAMES, 'url': site, 'inLanguage': 'ko-KR'}
app = {'@type': 'WebApplication', '@id': site + '#app', 'name': NAME, 'alternateName': ALT_NAMES, 'url': site,
       'description': APP_DESC, 'applicationCategory': 'SocialNetworkingApplication', 'operatingSystem': '웹 브라우저(PC·모바일)',
       'isAccessibleForFree': True, 'inLanguage': 'ko-KR', 'image': site + 'og.jpg',
       'audience': {'@type': 'Audience', 'audienceType': '피부관리사'},
       'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'KRW'}}
def ld(graph): return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1).replace('</', '<\\/')

# ---------- index.html ----------
src = src_path.read_text(encoding='utf-8')
src = src.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
src = src.replace('<title>피부관리사 대나무숲</title>', f'<title>{INDEX_TITLE}</title>', 1)
cut = src.index('<canvas id="forest"')
head_part, body_part = src[:cut].rstrip() + '\n', src[cut:]
head = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="{INDEX_DESC}">
<link rel="canonical" href="{site}">
<meta name="theme-color" content="#2E6C4B">
{VERIFY}
<meta property="og:type" content="website">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{NAME}">
<meta property="og:description" content="{INDEX_DESC}">
<meta property="og:url" content="{site}">
<meta property="og:image" content="{site}og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{FAVICON}">
<link rel="apple-touch-icon" href="icon.png">
<script type="application/ld+json">
{ld([website, app])}
</script>
<style>body{{margin:0}}img{{max-width:100%}}</style>
<script src="config.js"></script>
{head_part}</head>
<body>
'''
(out_dir / 'index.html').write_text(head.replace('\n\n<meta property="og:type"', '\n<meta property="og:type"') + body_part.rstrip() + '\n</body>\n</html>\n', encoding='utf-8')

# ---------- about.html ----------
faq = json.loads((site_src / 'faq.json').read_text(encoding='utf-8'))
faq_html = '\n'.join(f'        <div><dt>{html.escape(q)}</dt><dd>{html.escape(a)}</dd></div>' for q, a in faq)
faq_ld = {'@type': 'FAQPage', '@id': site + 'about.html#faq',
          'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}
crumbs = {'@type': 'BreadcrumbList', 'itemListElement': [
    {'@type': 'ListItem', 'position': 1, 'name': NAME, 'item': site},
    {'@type': 'ListItem', 'position': 2, 'name': '소개', 'item': site + 'about.html'}]}
about = (site_src / 'about.html').read_text(encoding='utf-8')
for k, v in {'{{JSONLD}}': ld([website, app, faq_ld, crumbs]), '{{FAQ_HTML}}': faq_html, '{{DESC}}': ABOUT_DESC,
             '{{FAVICON}}': FAVICON, '{{VERIFY}}\n': (VERIFY + '\n') if VERIFY else '', '{{SITE}}': site, '{{UPDATED}}': updated}.items():
    about = about.replace(k, v)
(out_dir / 'about.html').write_text(about, encoding='utf-8')

# ---------- robots.txt, sitemap.xml, llms.txt ----------
for name in ('robots.txt', 'sitemap.xml', 'llms.txt'):
    (out_dir / name).write_text((site_src / name).read_text(encoding='utf-8').replace('{{SITE}}', site).replace('{{UPDATED}}', updated), encoding='utf-8')

left = [p.name for p in out_dir.glob('*') if p.suffix in ('.html', '.txt', '.xml') and '{{' in p.read_text(encoding='utf-8')]
print('built', site, '| unreplaced placeholders in:', left or 'none')
