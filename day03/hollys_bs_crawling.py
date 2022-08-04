# 할리스커피숍  매장정보 크롤링
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime

from day03.coffeebean_crawling import getCoffeeBeanStoreInfo


def getHollysStoreInfo(result):
    for page in range(1,2):
        Hollys_url = f'https://www.hollys.co.kr/store/korea/korStore2.do?pageNo={page}'
        html  = urllib.request.urlopen(Hollys_url)
        soup = BeautifulSoup(html, 'html.parser')
        tbody = soup.find('tbody')

        for store in tbody.find_all('tr'):
            if len(store) <= 3: break

            store_td = store.find_all('td')

            store_name = store_td[1].string
            store_sido = store_td[0].string
            store_address =store_td[3].string
            store_phone = store_td[5].string

            result.append([store_name]+[store_sido]+[store_address]+[store_phone])

    columns =['store','sido-gu','address','phone']
    hollys_df = pd.DataFrame(result,columns=columns)
    # hollys_df.to_csv('C:/localRepository/StudyBigData/day03/hollys_shop_info.csv',index=True, encoding='utf-8')
    hollys_df.to_csv('../day03/hollys_shop_info.csv',index=True, encoding='utf-8')
    print('저장완료')
    del result[:]
    print('완료')


def main():
    result = []
    print('할리스 매장 크롤링 >>> ')
    getCoffeeBeanStoreInfo(result)


if __name__ == '__main__':
    main()
