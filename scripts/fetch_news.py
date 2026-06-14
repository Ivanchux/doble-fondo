import json, re, os, unicodedata, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

FEEDS = [
    {"url": "https://e00-elmundo.uecdn.es/elmundo/rss/politica.xml",    "name": "El Mundo",        "color": "#e8400a", "id": "ElMundo"},
    {"url": "https://www.elconfidencial.com/rss/espana/",               "name": "El Confidencial", "color": "#0066cc", "id": "ElConfidencial"},
    {"url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/politica/portada", "name": "El País", "color": "#4a90d9", "id": "ElPais"},
    {"url": "https://www.abc.es/rss/feeds/abc_Espana.xml",              "name": "ABC",             "color": "#c0392b", "id": "ABC"},
    {"url": "https://www.lavanguardia.com/rss/home.xml",                "name": "La Vanguardia",   "color": "#8e44ad", "id": "LaVanguardia"},
]

ZAP_KW = [
    'zapatero', 'julio moreno', 'julio martinez', 'zarrias', 'zarrías',
    'ferraz 35', 'kreab', 'thinking heads', 'plus ultra', 'gertrudis alcazar',
    'diligencias previas 77', 'aaron fajardo', 'red influencias',
]
LEI_KW = [
    'leire', 'operacion fidelidad', 'operación fidelidad', 'cerdan', 'cerdán',
    'ferraz 12', 'pedraz', 'mercedes gonzalez guardia', 'juan sanchez yepes',
]
ALL_KW = list(set(ZAP_KW + LEI_KW + [
    'audiencia nacional', 'koldo', 'udef', 'uco', 'caso zapatero', 'jci',
]))

def norm(s):
    return unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode()

def tag_caso(item):
    t = norm(item['title'] + ' ' + item.get('desc', ''))
    is_zap = any(norm(kw) in t for kw in ZAP_KW)
    is_lei = any(norm(kw) in t for kw in LEI_KW)
    if is_zap and is_lei: return 'both'
    if is_zap: return 'zap'
    if is_lei: return 'lei'
    if any(norm(kw) in t for kw in ALL_KW): return 'gen'
    return 'other'

def strip_html(s):
    return re.sub(r'<[^>]+>', '', s or '').strip()

def parse_date(s):
    try:
        return parsedate_to_datetime(s).timestamp()
    except Exception:
        return 0

def fetch_feed(feed):
    items = []
    try:
        req = urllib.request.Request(
            feed['url'],
            headers={'User-Agent': 'Mozilla/5.0 (compatible; DoubleFondo/1.0)'}
        )
        with urllib.request.urlopen(req, timeout=12) as r:
            content = r.read()
        root = ET.fromstring(content)
        for item in root.findall('.//item')[:20]:
            title = (item.findtext('title') or '').strip()
            link  = (item.findtext('link')  or item.findtext('guid') or '').strip()
            desc  = strip_html(item.findtext('description') or '')[:260]
            pub   = (item.findtext('pubDate') or '').strip()
            if title and link:
                items.append({
                    'title':  title,
                    'link':   link,
                    'desc':   desc,
                    'date':   pub,
                    'source': feed['name'],
                    'color':  feed['color'],
                    'feedId': feed['id'],
                })
    except Exception as e:
        print(f"[WARN] {feed['name']}: {e}")
    return items

# Fetch all feeds
all_items = []
for feed in FEEDS:
    fetched = fetch_feed(feed)
    print(f"  {feed['name']}: {len(fetched)} items")
    all_items.extend(fetched)

# Dedup by title
seen, unique = set(), []
for item in all_items:
    if item['title'] not in seen:
        seen.add(item['title'])
        unique.append(item)

# Tag and sort
for item in unique:
    item['caso'] = tag_caso(item)

unique.sort(key=lambda x: parse_date(x['date']), reverse=True)

# Filter: related first, fallback to all recent
related = [i for i in unique if i['caso'] != 'other']
final   = related if len(related) >= 4 else unique[:24]

output = {
    "updated": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    "count":   len(final),
    "items":   final,
}

os.makedirs('assets', exist_ok=True)
with open('assets/noticias.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Done — {len(final)} items written to assets/noticias.json")
