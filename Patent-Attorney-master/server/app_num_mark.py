# 상표 출원 번호 크롤링링

import os
import requests
import urllib.parse
import xml.etree.ElementTree as ET

# 공공데이터포털에서 받은 인증키
API_KEY = 'My OPENAPI_KEY'

# 카테고리별 키워드
CATEGORY_KEYWORDS = {
    '과자': '과자'
}

# 저장 위치
BASE_DIR = './train'

def make_dir_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_application_numbers_by_keyword(keyword, max_count=100):
    """
    지정된 키워드로 출원번호 리스트를 가져옵니다.
    """
    base_url = "http://kipo-api.kipi.or.kr/openapi/service/trademarkInfoSearchService/getAdvancedSearch"
    params = {
        'serviceKey': API_KEY,
        'application': 'true',
        'searchKeyword': keyword,
        'numOfRows': '100',
        'pageNo': '1'
    }

    try:
        response = requests.get(base_url, params=params, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[요청 오류] {keyword}: {e}")
        return []

    try:
        root = ET.fromstring(response.content)
        items = root.find('body').find('items')
        if items is None:
            return []

        numbers = []
        for item in items.findall('item'):
            app_num = item.findtext('applicationNumber')
            if app_num:
                numbers.append(app_num)
            if len(numbers) >= max_count:
                break

        return numbers
    except Exception as e:
        print(f"[파싱 오류] {keyword}: {e}")
        return []

def save_app_numbers_to_file(category, numbers):
    """
    출원번호를 ./train/카테고리/ 폴더에 저장
    """
    dir_path = os.path.join(BASE_DIR, category)
    make_dir_if_not_exist(dir_path)

    file_path = os.path.join(dir_path, 'application_numbers.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        for num in numbers:
            f.write(num + '\n')
    print(f"[저장 완료] {category}: {len(numbers)}건 저장됨")

def main():
    for category, keyword in CATEGORY_KEYWORDS.items():
        print(f"\n[크롤링 시작] {category}")
        numbers = get_application_numbers_by_keyword(keyword)
        save_app_numbers_to_file(category, numbers)

if __name__ == "__main__":
    main()
