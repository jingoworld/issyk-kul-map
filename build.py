"""코스 데이터(data.js)를 만든다. 실행: python3 -I build.py"""
import json, math

def load(f): return json.load(open('data/' + f))
def geo(f): return load(f + '.json')['features'][0]['geometry']['coordinates']
def dist(a, b): return math.hypot((a[0] - b[0]) * math.cos(math.radians(a[1])) * 111.32, (a[1] - b[1]) * 111.32)
def smooth(z, w=4):
    return [sum(z[max(0, i - w):i + w + 1]) / len(z[max(0, i - w):i + w + 1]) for i in range(len(z))]
def prep(c):
    z = smooth([p[2] for p in c]); out = []; d = 0
    for i, p in enumerate(c):
        if i: d += dist(c[i - 1], p)
        out.append([round(p[0], 5), round(p[1], 5), round(z[i]), round(d, 3)])
    return out
def stats(t):
    up = dn = 0; last = t[0][2]
    for p in t:
        e = p[2] - last
        if abs(e) >= 8:
            if e > 0: up += e
            else: dn -= e
            last = p[2]
    return dict(km=round(t[-1][3] - t[0][3], 1), up=round(up), dn=round(dn), max=max(p[2] for p in t), min=min(p[2] for p in t))
thin = lambda t: t[::2] + ([t[-1]] if (len(t) - 1) % 2 else [])
road = lambda f, n=6: [[round(x, 5), round(y, 5)] for x, y in load(f + '.json')['routes'][0]['geometry']['coordinates']][::n]
line = lambda f, n=6: [[round(p[0], 5), round(p[1], 5)] for p in geo(f)][::n]

up, down = geo('a_up'), geo('a_down')
A = prep(up + down[1:])
near = lambda ll: min(A, key=lambda p: dist(p, ll))
PASS = near([78.54534, 42.32639])
# 추정 위치: 시로타는 자료의 고도(2,800~3,000m), 켈디케는 자료의 고도(3,200m)로 경로 위에 잡았다
SIRO = next(p for p in A if p[2] >= 2900)
KELD = next(p for p in A if p[3] > PASS[3] and p[2] <= 3200)
LAKE = near([78.5276, 42.3189])
courses = dict(alakul=dict(
    name='아라콜 트레킹', sub='카라콜 계곡 · 시로타 · 아라콜 호수 · 아라콜 패스 · 켈디케 · 알틴아라샨',
    track=thin(A), stats=stats(A),
    note='이틀 코스입니다. 패스를 넘는 2일차가 가장 길고, 마지막은 알틴아라샨 온천 마을에서 끝납니다.',
    cuts=[dict(name='계곡 입구', km=0), dict(name='시로타', km=SIRO[3]), dict(name='아라콜 호수', km=LAKE[3]), dict(name='아라콜 패스', km=PASS[3]),
          dict(name='켈디케', km=KELD[3]), dict(name='알틴아라샨', km=A[-1][3])]))

def poi(id, name, kind, ll, text, ele=None, course=None, sub=False):
    return dict(id=id, name=name, kind=kind, lng=ll[0], lat=ll[1], ele=ele, text=text, course=course, sub=sub)
pois = [
    poi('th', '카라콜 계곡 입구', 'stay', A[0][:2], '아라콜 트레킹 시작점. 차량이 어디까지 들어가는지는 확인이 필요합니다.', A[0][2], 'alakul'),
    poi('si', '시로타', 'stay', SIRO[:2], '1일차 숙박지. 위치는 자료의 고도로 잡은 추정값입니다.', 2900, 'alakul'),
    poi('la', '아라콜 호수', 'lake', LAKE[:2], '해발 약 3,530m의 빙하호. 호수를 내려다보며 패스로 오릅니다.', 3530, 'alakul'),
    poi('pa', '아라콜 패스', 'pass', PASS[:2], '이번 일정의 최고 지점. 해발 약 3,900m입니다.', 3900, 'alakul'),
    poi('ke', '켈디케', 'lake', KELD[:2], '패스 동쪽으로 내려가는 길의 계곡. 위치는 추정값입니다.', 3200, 'alakul', True),
    poi('aa', '알틴아라샨', 'stay', A[-1][:2], '2일차 숙박지. 온천에서 쉬고 다음 날 지프로 악수까지 내려갑니다.', A[-1][2], 'alakul'),
    poi('bi', '비슈케크', 'city', [74.5698, 42.8746], '일정의 시작과 끝. 마나스 공항은 시내 북쪽에 있습니다.', 750),
    poi('ba', '발릭치', 'city', [76.1963, 42.4570], '이식쿨 서쪽 끝 도시. 여름철 비슈케크 기차가 닿습니다.', 1620, None, True),
    poi('ko', '코치코르', 'city', [75.7541, 42.2132], '송쿨로 가는 길목. 9일 상품의 점심 장소입니다.', 1800, None, True),
    poi('so', '송쿨 호수', 'lake', [75.17, 41.90], '9일 상품의 유르트 1박. 해발 약 3,000m에서 고소에 적응합니다. 숙박 위치는 확인이 필요합니다.', 3000),
    poi('as', '악사이 협곡', 'lake', [76.84518, 42.19272], '이식쿨 남쪽 호숫가의 붉은 협곡.', None),
    poi('sk', '스카즈카 협곡', 'lake', [77.35402, 42.15664], '붉은 바위가 성처럼 늘어선 협곡. 동화(스카즈카)라는 이름의 뜻 그대로입니다.', None),
    poi('ta', '타므가', 'stay', [77.54942, 42.15071], '남쪽 호숫가 마을. 남쪽 투어 중 하루 숙박합니다.', 1690),
    poi('bs', '바르스콘 폭포', 'lake', [77.60275, 41.99873], '바르스콘 계곡 안쪽의 폭포. 해발 약 3,000m까지 차로 올라갑니다.', 3000),
    poi('jo', '제티오구즈', 'lake', [78.23813, 42.33904], '붉은 바위 절벽으로 유명한 계곡.', 2050),
    poi('ka', '카라콜', 'city', [78.39686, 42.49174], '이식쿨 동쪽 도시. 9일 상품은 트레킹 전날 1박합니다.', 1750),
    poi('ak', '악수', 'city', [78.5224, 42.4997], '알틴아라샨에서 지프로 내려와 전용차량으로 갈아타는 곳.', None, None, True),
    poi('ch', '촐폰아타', 'city', [77.06652, 42.64171], '이식쿨 북쪽 휴양지. 유람선과 호숫가 산책을 합니다.', 1640),
]
jeep = [road('r_bi_ba'), road('r_ba_ko', 3), road('r_ko_so', 3), road('r_south'), road('r_bars', 3), road('r_trailhead', 3), road('r_as_ka', 3), road('r_north'), line('r_aa_as')]
data = dict(courses=courses, jeep=jeep, pois=pois)
open('data.js', 'w', encoding='utf8').write('window.TREK=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
for k, c in courses.items():
    print(k, c['stats'], len(c['track']), [(q['name'], round(q['km'], 1)) for q in c['cuts']])
