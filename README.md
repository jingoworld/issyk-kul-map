# 이식쿨 트레킹 코스 지도

키르기스스탄 아라콜·이식쿨 6일, 송쿨·아라콜·이식쿨 9일의 맵박스 지도와 일정 페이지. `south-america-map`을 복사해 만들었다.

- 페이지: `index.html`(코스 지도), `compare.html`(일정 비교), `trip-6/9.html`(일정 상세)
- 실행: `python3 -m http.server 3014` (launch.json `issyk-kul-map`)
- 일정표가 바뀌면 `data/trips.json`을 고치고 `python3 -I build_pages.py`. 원본 시트: 드라이브 `이식쿨아라콜_키르기스스탄4박6일_0720`, `이식쿨아라콜송쿨_키르기스스탄7박9일_0720`
- 일정표 파일: `files/trip-N.pdf`와 쪽별 이미지 `files/trip-N-pK.png`. 시트를 고치면 다시 만든 뒤 `build_pages.py`를 실행한다.
- 코스 데이터: `python3 -I build.py` → `data.js`
- 경로: OSM 등산로를 BRouter(hiking-mountain)로 연결, 차량 구간은 OSRM. 알틴아라샨-악수 지프 구간도 BRouter.
- 추정 위치: 시로타(자료 고도 2,800~3,000m → 2,900m 지점), 켈디케(자료 고도 3,200m 지점), 카라콜 계곡 입구(차도 끝으로 본 지점), 송쿨 숙박지. 현장 GPS로 `build.py`를 고친다.
- 일자별 고도 그래프(`build_pages.py`의 ALT)는 지역 고도로 잡은 대략값이다.
- CSS를 고치면 `site.css?v=N` 번호를 `index.html`과 `build_pages.py`에서 함께 올린다.
- 공개 사이트: https://jingoworld.github.io/issyk-kul-map/ (저장소 `jingoworld/issyk-kul-map`, `main` 푸시로 반영)
- 토큰: `config.js`. 공개용(`pk`)만 쓴다.
