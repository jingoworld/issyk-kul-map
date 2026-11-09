"""시트에서 PDF로 내려받은 저장 파일(JSON)로 files/trip-N.pdf와 쪽별 미리보기 이미지를 만든다.

사용법: /usr/bin/python3 make_files.py <PDF 저장 파일 2개>
xlsx 저장 파일이 섞여 있어도 건너뛴다. 상세 페이지는 build_pages.py로 따로 만든다.
"""
import base64, glob, json, os, sys
import fitz  # pymupdf

# 손님이 보는 PDF는 [고객용] 사본(같은 폴더)에서 받는다. 사본에는 [확인 필요] 문구가 없다.
IDS = {'1iIljVwPghgy7NLvWPki93Dnd5N33c6LiBpUj-kMBv00': '6',
       '1Y-Ck8uAPiOAbAIBHsmoBhh4yRlfq-0AINLiW4T0yTzg': '9'}
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, 'files')
os.makedirs(out, exist_ok=True)
for path in sys.argv[1:]:
    j = json.load(open(path, encoding='utf8'))
    b = base64.b64decode(j['content'])
    if b[:4] != b'%PDF' or j.get('id') not in IDS:
        continue
    key = IDS[j['id']]
    open(os.path.join(out, f'trip-{key}.pdf'), 'wb').write(b)
    for old in glob.glob(os.path.join(out, f'trip-{key}-p*.png')):
        os.remove(old)
    doc = fitz.open(stream=b, filetype='pdf')
    for i, page in enumerate(doc, 1):
        page.get_pixmap(dpi=130, alpha=False).save(os.path.join(out, f'trip-{key}-p{i}.png'))
    print(f'trip-{key}', j['title'], len(doc), 'pages')
