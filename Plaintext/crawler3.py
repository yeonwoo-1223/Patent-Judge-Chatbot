import os
import django
import json
import unicodedata
import requests
from urllib.parse import quote
from PIL import Image
from io import BytesIO

# BASE_DIR은 manage.py가 있는 디렉토리 기준
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Painttext.Patent_Attorney.config.settings")
django.setup()
2
from Painttext.Patent_Attorney.api.models import MarkPatentInfo, DesignPatentInfo


# ✅ API KEY 로드
with open('Painttext/Patent_Attorney/config/secrets.json', 'r', encoding='utf-8') as f:
    secrets = json.load(f)
OPENAPI_KEY = secrets["OPENAPI_KEY"]

# ✅ 이미지 저장 디렉토리
BASE_DIR = './train'


def fetch_and_save_image(image_url, save_path):
    try:
        res = requests.get(image_url)
        if res.status_code == 200:
            image = Image.open(BytesIO(res.content)).convert('RGB')
            image.save(save_path, format='JPEG')
            return True
    except Exception as e:
        print(f"[!] 이미지 저장 실패: {image_url} => {e}")
    return False


def crawl_mark_info(keyword, max_count=10):
    url = f"http://plus.kipris.or.kr/openapi/rest/TrademarkInfoSearchService/AdvancedSearch?word={quote(keyword)}&accessKey={OPENAPI_KEY}&numOfRows={max_count}"
    res = requests.get(url)
    if res.status_code != 200:
        print("[!] API 요청 실패:", res.text)
        return

    from xml.etree import ElementTree
    tree = ElementTree.fromstring(res.content)

    items = tree.findall('.//item')
    category_dir = os.path.join(BASE_DIR, keyword)
    os.makedirs(category_dir, exist_ok=True)

    for item in items:
        app_num = item.findtext('applicationNumber')
        app_name = item.findtext('applicantName')
        agent_name = item.findtext('agentName', default='-')
        status = item.findtext('applicationStatus')
        pub_date = item.findtext('publicationDate')
        pub_num = item.findtext('publicationNumber')
        title = item.findtext('title')
        image_url = item.findtext('imageFilePath')

        if not all([app_num, image_url]):
            continue

        image_filename = f"{app_num}.jpg"
        save_path = os.path.join(category_dir, image_filename)
        if not fetch_and_save_image(image_url, save_path):
            continue

        MarkPatentInfo.objects.update_or_create(
            app_num=app_num,
            defaults={
                'app_name': app_name or '미상',
                'agent_name': agent_name,
                'app_status': status or '출원중',
                'pub_date': pub_date or '00000000',
                'pub_num': pub_num or '-',
                'image_path': save_path.replace('./', ''),
                'category': keyword,
                'title': title or '무제',
            }
        )
        print(f"✔ 저장 완료: {app_num}")


def crawl_design_info(keyword, max_count=10):
    url = f"http://plus.kipris.or.kr/openapi/rest/DesignInfoSearchService/AdvancedSearch?word={quote(keyword)}&accessKey={OPENAPI_KEY}&numOfRows={max_count}"
    res = requests.get(url)
    if res.status_code != 200:
        print("[!] API 요청 실패:", res.text)
        return

    from xml.etree import ElementTree
    tree = ElementTree.fromstring(res.content)

    items = tree.findall('.//item')
    category_dir = os.path.join(BASE_DIR, keyword)
    os.makedirs(category_dir, exist_ok=True)

    for item in items:
        app_num = item.findtext('applicationNumber')
        app_name = item.findtext('applicantName')
        agent_name = item.findtext('agentName', default='-')
        status = item.findtext('applicationStatus')
        pub_date = item.findtext('publicationDate')
        pub_num = item.findtext('publicationNumber')
        article_name = item.findtext('articleName')
        image_url = item.findtext('imageFilePath')

        if not all([app_num, image_url]):
            continue

        image_filename = f"{app_num}.jpg"
        save_path = os.path.join(category_dir, image_filename)
        if not fetch_and_save_image(image_url, save_path):
            continue

        DesignPatentInfo.objects.update_or_create(
            app_num=app_num,
            defaults={
                'app_name': app_name or '미상',
                'agent_name': agent_name,
                'app_status': status or '출원중',
                'pub_date': pub_date or '00000000',
                'pub_num': pub_num or '-',
                'image_path': save_path.replace('./', ''),
                'category': keyword,
                'article_name': article_name or '무제',
            }
        )
        print(f"✔ 저장 완료: {app_num}")


# ✅ 실행 예시
if __name__ == '__main__':
    mark_keywords = []           # ex: ['스타벅스']
    design_keywords = ['의자']   # ex: ['의자', '소파']

    for keyword in mark_keywords:
        crawl_mark_info(keyword, max_count=20)

    for keyword in design_keywords:
        crawl_design_info(keyword, max_count=20)
