import os
import json
import django
import unicodedata
from xml.etree import ElementTree as elemTree
from Painttext.Patent_Attorney.api.models import MarkPatentInfo, DesignPatentInfo

# Django 환경 세팅 (프로젝트 settings 모듈 경로에 맞게 수정)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# 비밀 키 불러오기 함수
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, 'config/secrets.json'), encoding='utf-8') as f:
    secrets = json.load(f)

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        raise Exception(f'Set the {setting} env variable.')

# XML 파싱 함수 (특허청 API 결과에서 필요한 데이터 추출)
def parse_xml(app_num, xml_string_data, category):
    root = elemTree.fromstring(xml_string_data)
    keys = set(category)
    parsed = dict.fromkeys(keys, 'empty')

    try:
        body = root.find('body')
        items = body.find('items')
        item = items.find('item')

        for child in item:
            if child.tag in category and child.text:
                parsed[child.tag] = child.text

    except Exception as e:
        header = root.find('header')
        result_code = header.find('resultCode').text
        error_msg = header.find('resultMsg').text
        print(f'{app_num} 특허청 호출 에러 코드[{result_code}] : {error_msg}')
        return {}, False

    return parsed, True

# DB에 저장할 인스턴스 생성 함수 (예시)
def create_model_instance(filename, category_flag, dir_name):
    # category_flag: 0=MarkPatentInfo, 1=DesignPatentInfo
    app_num = filename
    # API 호출해서 xml_string_data 받아오는 부분 필요
    xml_string_data = ''  # 실제 API 요청 후 응답으로 채워야 함

    # 파싱에 필요한 태그 리스트 (예시)
    if category_flag == 0:
        category = ['app_num', 'title', 'agent_name', 'app_status', 'pub_date', 'pub_num', 'image_path']
    else:
        category = ['app_num', 'article_name', 'agent_name', 'app_status', 'pub_date', 'pub_num', 'image_path']

    parsed_data, success = parse_xml(app_num, xml_string_data, category)
    if not success:
        return

    if category_flag == 0:
        instance = MarkPatentInfo(
            app_num=parsed_data.get('app_num', ''),
            title=parsed_data.get('title', ''),
            agent_name=parsed_data.get('agent_name', ''),
            app_status=parsed_data.get('app_status', ''),
            pub_date=parsed_data.get('pub_date', ''),
            pub_num=parsed_data.get('pub_num', ''),
            image_path=parsed_data.get('image_path', ''),
            category=dir_name
        )
    else:
        instance = DesignPatentInfo(
            app_num=parsed_data.get('app_num', ''),
            article_name=parsed_data.get('article_name', ''),
            agent_name=parsed_data.get('agent_name', ''),
            app_status=parsed_data.get('app_status', ''),
            pub_date=parsed_data.get('pub_date', ''),
            pub_num=parsed_data.get('pub_num', ''),
            image_path=parsed_data.get('image_path', ''),
            category=dir_name
        )

    instance.save()
    print(f'{app_num} 데이터 저장 완료')

# main 실행부 예시
if __name__ == '__main__':
    mark_list = []  # 상표 리스트 예시 (빈 리스트면 무시)
    design_list = ['의자']  # 디자인 리스트 예시

    dirs = os.listdir('./train')
    for dir_name in dirs:
        dir_name = unicodedata.normalize('NFC', dir_name)
        if dir_name in mark_list:
            filenames = os.listdir(f'./train/{dir_name}')
            filenames = [os.path.splitext(f)[0] for f in filenames]
            for filename in filenames:
                create_model_instance(filename, 0, dir_name)
        elif dir_name in design_list:
            filenames = os.listdir(f'./train/{dir_name}')
            filenames = [os.path.splitext(f)[0] for f in filenames]
            filenames.sort()
            for count, filename in enumerate(filenames):
                if count == 100:
                    break
                create_model_instance(filename, 1, dir_name)
