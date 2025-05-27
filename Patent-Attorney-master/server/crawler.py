import os
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import time
import unicodedata

# OpenAPI 키 설정
OPENAPI_KEY = 'MY_OPENAPI_KEY'  # 공공데이터포털에서 받은 인증키

# 상표권 API URL
BASE_URL = 'http://kipo-api.kipi.or.kr/openapi/service/trademarkInfoSearchService/getAdvancedSearch'

# 저장 경로
BASE_DIR = './train'

# 요청 URL 생성 함수
def make_query_url(app_num):
    params = {
        'serviceKey': OPENAPI_KEY,
        'applicationNumber': app_num,
        'application': 'true',
        'registration': 'true',
        'refused': 'true',
        'expiration': 'true',
        'withdrawal': 'true',
        'publication': 'true',
        'cancel': 'true',
        'abandonment': 'true',
        'trademark': 'true',
        'serviceMark': 'true',
        'businessEmblem': 'true',
        'collectiveMark': 'true',
        'internationalMark': 'true',
        'character': 'true',
        'figure': 'true',
        'compositionCharacter': 'true',
        'figureComposition': 'true'
    }
    query_string = urllib.parse.urlencode(params, safe='=&')
    return f"{BASE_URL}?{query_string}"

# XML 파싱해서 이미지 경로 추출
def get_image_url(xml_string):
    root = ET.fromstring(xml_string)
    try:
        body = root.find('body')
        items = body.find('items')
        item = items.find('item')
        image_url = item.find('bigDrawing').text
        return image_url
    except:
        return None

# 이미지 저장 함수
def download_image(image_url, save_path):
    try:
        urllib.request.urlretrieve(image_url, save_path)
        return True
    except Exception as e:
        print(f"[이미지 저장 실패] {image_url} → {save_path} : {e}")
        return False

# 출원번호 단위 처리
def process_application(app_num, save_dir):
    try:
        query_url = make_query_url(app_num)
        req = urllib.request.Request(query_url)
        response = urllib.request.urlopen(req)
        xml_data = response.read().decode('utf-8')
        image_url = get_image_url(xml_data)

        if image_url:
            save_path = os.path.join(save_dir, f"{app_num}.jpg")
            success = download_image(image_url, save_path)
            if success:
                print(f"[성공] {app_num} → 저장 완료")
            else:
                print(f"[실패] {app_num} → 이미지 저장 실패")
        else:
            print(f"[실패] {app_num} → 이미지 URL 없음")
        time.sleep(0.2)  # API 과호출 방지용 대기
    except Exception as e:
        print(f"[요청 실패] {app_num} : {e}")

# 전체 디렉토리 순회하며 실행
def crawl_all():
    for dir_name in os.listdir(BASE_DIR):
        category_dir = os.path.join(BASE_DIR, dir_name)
        category_dir = unicodedata.normalize('NFC', category_dir)
        txt_path = os.path.join(category_dir, 'application_numbers.txt')

        if not os.path.exists(txt_path):
            print(f"[건너뜀] {dir_name} : application_numbers.txt 없음")
            continue

        with open(txt_path, 'r', encoding='utf-8') as f:
            app_numbers = [line.strip() for line in f if line.strip()]

        for app_num in app_numbers[:100]:  # 100개 제한
            process_application(app_num, category_dir)

if __name__ == '__main__':
    crawl_all()
