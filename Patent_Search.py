from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote
from time import sleep

def Search():
    keyword = input('특허법원에서 찾을 문서를 입력하세요: ')
    page = int(input('몇 쪽까지 찾아볼까요? '))
    keyword_encoded = quote(keyword)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    count = 0
    for p in range(1, page + 1):
        print(f"\n\n{p} 페이지\n" + "=" * 10)
        url = f"https://patent.scourt.go.kr/dcboard/new/DcNewsListAction.work?gubun=44&cbub_code=&searchGubun=subject&searchValue={keyword_encoded}&pageIndex={p}"
        driver.get(url)
        sleep(2)  # 페이지 로딩 대기 (필요시 시간 늘리기)

        links = driver.find_elements(By.CSS_SELECTOR, "td.title a")
        for link in links:
            print("제목:", link.text.strip())
            print("링크:", link.get_attribute('href'))
            count += 1

    print(f"\n총 {count}개의 결과가 검색되었습니다.")
    driver.quit()

Search()
