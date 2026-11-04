"""일정 비교(compare.html)와 일정별 상세(trip-6/9.html)를 만든다.

실행: python3 -I build_pages.py
내용은 data/trips.json. 시트를 고치면 이 파일과 files/의 PDF·이미지를 함께 고친다.
plan의 줄 앞 '**'는 소제목, '~'는 트레킹 경로 줄이다.
"""
import glob, html, json, os, re

META = {
    '6': dict(name='6일 아라콜·이식쿨', nights='4박 6일', span='2027.7.20 ~ 7.25 (예시)', tag='필수 코스를 빠르게', course='alakul',
              air='티웨이 직항', trek='2일', main='아라콜, 이식쿨 남쪽 투어, 촐폰아타 반나절', peak='약 3,900m', stay='시로타 1박, 알틴아라샨 1박',
              city='비슈케크', inner='전용차량, 지프',
              card='이식쿨 남쪽 협곡을 보고 아라콜 호수와 패스를 넘은 뒤, 알틴아라샨 온천에서 쉽니다. 촐폰아타는 마지막 날 반나절 들릅니다.',
              lead='짧은 휴가로 아라콜과 이식쿨 핵심을 보는 일정입니다. 도착 다음 날부터 움직여 고소 적응 시간이 짧습니다.'),
    '9': dict(name='9일 송쿨·아라콜', nights='7박 9일', span='2027.7.20 ~ 7.28 (예시)', tag='송쿨 유르트와 호숫가 휴양', course='alakul',
              air='티웨이 직항', trek='2일', main='송쿨 유르트, 아라콜, 이식쿨 남쪽 투어, 촐폰아타 1박', peak='약 3,900m', stay='송쿨 유르트 1박, 시로타 1박, 알틴아라샨 1박',
              city='비슈케크, 카라콜', inner='전용차량, 지프',
              card='해발 3,000m 송쿨에서 하루 자며 몸을 적응시키고 아라콜을 넘습니다. 남쪽 투어는 이틀로 나누고 촐폰아타에서 1박하며 쉽니다.',
              lead='송쿨 유르트 1박으로 고소에 적응한 뒤 아라콜을 걷고, 촐폰아타 호숫가에서 쉬며 마치는 일정입니다.'),
}
# 일자별 (그날 최고 고도, 자는 곳 고도). 0은 기내·이동으로 표시하지 않는다.
ALT = {
    '6': [(750, 750), (3030, 1690), (2900, 2900), (3900, 2520), (2520, None), (0, None)],
    '9': [(750, 750), (3450, 3020), (3020, 1690), (3030, 1750), (2900, 2900), (3900, 2520), (2520, 1640), (1640, None), (0, None)],
}
NAV = [('index.html', '코스 지도'), ('compare.html', '일정 비교'), ('trip-6.html', '6일 아라콜·이식쿨'), ('trip-9.html', '9일 송쿨·아라콜')]
ALT_NOTE = '막대는 그날 오른 최고 지점, 점은 자는 곳입니다. 점이 없는 날은 기내 숙박입니다. 알려진 지역 고도로 잡은 대략값입니다.'


def esc(s):
    return html.escape(s, quote=False)


def red(s):
    return re.sub(r'\[[^\]\n]*확인[^\]\n]*\]', lambda m: f'<span class="chk">{m[0]}</span>', esc(s))


def page(cur, title, body):
    on = ' aria-current="page"'
    nav = ''.join(f'<a href="{h}"{on if h == cur else ""}>{n}</a>' for h, n in NAV)
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | 이식쿨 트레킹</title><link href="site.css?v=1" rel="stylesheet"></head>
<body><header class="hdr"><a class="logo" href="index.html">두드림 이식쿨 트레킹</a><nav aria-label="주 메뉴">{nav}</nav></header>
<main class="wrap">{body}</main>
<footer class="ft">두드림여행사 · 010-2782-2660 · dodreamtour.com</footer></body></html>
'''


def alt_svg(key):
    rows = ALT[key]
    band = 30 if len(rows) > 20 else 44
    width = 46 + band * len(rows) + 6
    base, k = 176, 128 / 5200
    y = lambda v: base - v * k
    s = []
    for g in (2000, 4000):
        s.append(f'<line x1="0" x2="{width}" y1="{y(g):.1f}" y2="{y(g):.1f}" stroke="#a5abb3" stroke-dasharray="4 4"/>'
                 f'<text x="0" y="{y(g) - 4:.1f}">{g:,}m</text>')
    for i, (h, sl) in enumerate(rows):
        bx = 46 + i * band + 3
        w = band - 8
        c = bx + w / 2
        over = h >= 3500
        if h:
            s.append(f'<rect x="{bx}" y="{y(h):.1f}" width="{w}" height="{base - y(h):.1f}" rx="3" fill="{"#2a78d6" if over else "#d9d8d1"}"><title>{i + 1}일차 {h:,}m</title></rect>')
        if over:
            s.append(f'<text x="{c}" y="{y(h) - 5:.1f}" text-anchor="middle" class="v">{h:,}</text>')
        if sl:
            s.append(f'<circle cx="{c}" cy="{y(sl):.1f}" r="4" fill="#111" stroke="#fff" stroke-width="1.4"><title>자는 곳 {sl:,}m</title></circle>')
        s.append(f'<text x="{c}" y="{base + 15}" text-anchor="middle">{i + 1}</text>')
    return f'<svg class="alt" viewBox="0 0 {width} 200" style="min-width:{width}px" role="img" aria-label="{META[key]["name"]} 일자별 고도">{"".join(s)}</svg>'


def cards():
    c = ''.join(f'<a class="card" href="trip-{k}.html"><b>{m["name"]}</b><div class="d">{m["nights"]} · {m["tag"]}</div>'
                f'<p>{m["card"]}</p><span class="go">일정 보기 →</span></a>' for k, m in META.items())
    return f'<div class="cards">{c}</div>'


def compare():
    rows = [('기간', 'nights'), ('출발·귀국', 'span'), ('항공 (2026년 기준)', 'air'), ('트레킹 일수', 'trek'), ('주요 코스', 'main'),
            ('최고 고도', 'peak'), ('산악 숙박', 'stay'), ('도시', 'city'), ('내부 이동', 'inner')]
    tr = ''.join(f'<tr><td>{n}</td>' + ''.join(f'<td>{META[k][f]}</td>' for k in META) + '</tr>' for n, f in rows)
    head = ''.join(f'<th><a href="trip-{k}.html">{META[k]["name"]}</a></th>' for k in META)
    alt = ''.join(f'<p class="fig">{META[k]["name"]}</p><div class="scroll">{alt_svg(k)}</div>' for k in META)
    return page('compare.html', '일정 비교', f'''
<h1>이식쿨 트레킹 2종 비교</h1>
<p class="lead">짧은 휴가로 필수 코스를 모두 보려면 6일, 송쿨 유르트와 촐폰아타 1박까지 여유 있게 다니려면 9일을 권합니다. 아라콜 코스는 두 상품이 같습니다.</p>
{cards()}
<h2>핵심 지표</h2>
<div class="scroll"><table class="cmp"><tr><th>지표</th>{head}</tr>{tr}
<tr><td>인원·요금</td><td colspan="2">출발 8~20명 · 1인 요금 <span class="chk">[확인 필요]</span></td></tr></table></div>
<h2>일자별 고도</h2>
<p class="cap" style="margin:0 0 14px">3,500m를 넘는 날은 두 상품 모두 아라콜 패스를 넘는 하루입니다.</p>
{alt}
<p class="cap">{ALT_NOTE}</p>
<h2>확인할 점</h2>
<ul class="cap">
<li>항공은 2026년 하계 스케줄 기준입니다. 2027년 운항 여부와 시각은 확인이 필요합니다.</li>
<li>6일 상품은 도착 이틀 뒤 해발 약 2,900m에서 자고 다음 날 패스를 넘어 고소 적응 시간이 짧습니다.</li>
<li>시로타 숙소 형태와 카라콜 계곡 차량 진입 범위, 유람선 운항 시간은 확인이 필요합니다. 유람선은 날씨로 취소될 수 있습니다.</li>
</ul>''')


def day_html(d):
    items = []
    stay = ''
    for l in [l.strip() for l in d['plan'].split('\n') if l.strip()]:
        if l.startswith('숙박'):
            stay = l.split(':', 1)[-1].strip()
            continue
        cls = ''
        if l.startswith('**'):
            cls, l = ' class="t"', l[2:]
        elif l.startswith('~'):
            cls, l = ' class="r"', l[1:]
        items.append(f'<li{cls}>{red(l)}</li>')
    join = lambda s, sep: sep.join(x.strip() for x in s.split('\n') if x.strip())
    meta = [('교통', join(d['move'], ' · ')), ('시간', join(d['time'], ' · ')),
            ('식사', join(d['meal'].replace('조:', '조').replace('중:', '중').replace('석:', '석'), ' · '))]
    if stay:
        meta.insert(0, ('숙박', stay))
    m = ''.join(f'<span><b>{n}</b> {red(v)}</span>' for n, v in meta if v)
    return (f'<article class="day"><div><div class="no">{esc(d["no"])}</div><div class="dt">{esc(d["date"])}</div></div>'
            f'<div><div class="route">{esc(join(d["area"], " → "))}</div><ul>{"".join(items)}</ul><div class="meta">{m}</div></div></article>')


def sheet_modal(key, t):
    """일정표를 이미지로 먼저 보여 주고, 그 안에서 PDF를 내려받게 한다."""
    pages = sorted(glob.glob(os.path.join(here, 'files', f'trip-{key}-p*.png')), key=lambda p: int(re.search(r'-p(\d+)\.png', p)[1]))
    title = esc(t['title'])
    name = t['title'].replace(' ', '_') + '_일정표'
    imgs = ''.join(f'<img src="files/{os.path.basename(p)}" alt="{title} 일정표 {i}쪽" loading="lazy">'
                   for i, p in enumerate(pages, 1))
    return f'''<dialog class="sheet" id="sheet" aria-labelledby="sheet-title">
<div class="sheet-top"><b id="sheet-title">{title} 일정표</b>
<a class="btn" href="files/trip-{key}.pdf" download="{esc(name)}.pdf">PDF 다운로드</a>
<button class="sheet-x" id="close-sheet" type="button" aria-label="닫기">×</button></div>
<div class="sheet-body">{imgs}</div></dialog>
<script>
const dlg=document.getElementById('sheet');
document.getElementById('open-sheet').onclick=()=>dlg.showModal();
document.getElementById('close-sheet').onclick=()=>dlg.close();
dlg.addEventListener('click',e=>{{if(e.target===dlg)dlg.close();}});
</script>'''


def trip(key, t):
    m = META[key]
    facts = [('기간', m['nights']), ('최고 고도', m['peak']), ('트레킹 일수', m['trek']), ('항공', m['air']),
             ('산악 숙박', m['stay']), ('1인 요금', red(t['price']))]
    f = ''.join(f'<div class="fact"><span>{a}</span><b>{b}</b></div>' for a, b in facts)
    info = [('출발 인원', t['people']), ('숙소·차량', t['base']), ('포함', t['inc']), ('불포함', t['exc']), ('참고', t['note'])]
    dl = ''.join(f'<dt>{a}</dt><dd>{red(b)}</dd>' for a, b in info if b)
    return page(f'trip-{key}.html', m['name'], f'''
<h1>{esc(t["title"])}</h1>
<p class="lead">{m["lead"]}</p>
<div class="facts">{f}</div>
<div class="acts"><a class="btn" href="index.html?course={m["course"]}">코스 지도에서 보기</a><button class="btn sec" id="open-sheet" type="button">일정표 미리보기</button><a class="btn sec" href="compare.html">일정 비교로 돌아가기</a></div>
{sheet_modal(key, t)}
<h2>일자별 일정</h2>
{"".join(day_html(d) for d in t["days"])}
<h2>일자별 고도</h2>
<div class="scroll">{alt_svg(key)}</div>
<p class="cap">{ALT_NOTE}</p>
<h2>상품 안내</h2>
<dl class="info">{dl}</dl>''')


here = os.path.dirname(os.path.abspath(__file__))
trips = json.load(open(os.path.join(here, 'data', 'trips.json'), encoding='utf8'))
assert all(len(ALT[k]) == len(t['days']) for k, t in trips.items()), {k: (len(ALT[k]), len(t['days'])) for k, t in trips.items()}
open(os.path.join(here, 'compare.html'), 'w', encoding='utf8').write(compare())
for k, t in trips.items():
    open(os.path.join(here, f'trip-{k}.html'), 'w', encoding='utf8').write(trip(k, t))
    print(k, t['title'], len(t['days']), 'days', t['people'], t['price'])
