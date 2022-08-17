import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from urllib.parse import quote 
import json  # 검색결과를 json 타입으로 받음
import urllib.request  # URL openAPI 검색위해
import webbrowser 



# 클래스 oop
class qTemplate(QWidget):
    # 생성자
    def __init__(self) -> None:  # -> None return 하는 값이 없다. init은 기본적으로 None이다. - > str : string값을 return 한다.
        super().__init__()
        uic.loadUi('./pyqt02/navernews.ui',self)
        self.initUI()

    def initUI(self) -> None:
        self.addControls()
        self.show()

    def addControls(self) -> None: # 위젯 정의, 이벤트 (시그널) 처리
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        self.txtSearch.returnPressed.connect(self.btnSearchClicked) # 검색어를 입력 후 enter를 쳤을 때 다음 단계로 넘어가게 함
        self.tblResult.itemSelectionChanged.connect(self.tblResultSelected)

    def tblResultSelected(self) -> None:
        selected = self.tblResult.currentRow() # 현재 선택된 열의 인덱스
        link = self.tblResult.item(selected, 1).text()
        webbrowser.open(link)
    
    def btnSearchClicked(self) -> None: # 슬롯(이벤트핸들러)
        jsonResult = []
        totalResult = []
        keyword = 'news'
        search_word = self.txtSearch.text()
        display_count = 50

        jsonResult = self.getNaverSearch(keyword, search_word, 1, display_count)
        # print(jsonResult)
        for post in jsonResult['items']:
            totalResult.append(self.getPostData(post))
        
        # print(totalResult)
        self.makeTable(totalResult)
        return 

   
    def makeTable(self, result):
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblResult.setColumnCount(2)
        self.tblResult.setRowCount(len(result))  # displayCount에 따라서 변경, 현재는 50
        self.tblResult.setHorizontalHeaderLabels(['기사제목','뉴스링크'])
        self.tblResult.setColumnWidth(0,350)
        self.tblResult.setColumnWidth(1,100)
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers) # readonly

        i = 0
        for item in result:
            title = self.strip_tag(item[0]['title'])
            link = item[0]['org_link']
            self.tblResult.setItem(i,0, QTableWidgetItem(title))
            self.tblResult.setItem(i,1, QTableWidgetItem(link))
            i += 1
    
    def strip_tag(self, title):  # html 태그를 없애주는 함수
        ret = title.replace('&lt;','<')
        ret = ret.replace('&gt;','>')
        ret = ret.replace('&quot;', '"')
        ret = ret.replace('&apos;', "'")
        ret = ret.replace('&amp;', '&')
        ret = ret.replace('<b>','')
        ret = ret.replace('</b>','')

        return ret
    


    def getPostData(self, post):
        temp = []
        title = post['title']
        description = post['description']
        org_link = post['originallink']
        link = post['link']
        pubDate = post['pubDate']

        temp.append({'title':title
                     ,'description':description
                     ,'org_link':org_link
                     ,'link':link})
        return temp


    # 네이버API 크롤링 함수
    def getNaverSearch(self, keyword, search, start, display):
        url = f'https://openapi.naver.com/v1/search/{keyword}.json' \
              f'?query={quote(search)}&start={start}&display={display}'
        req = urllib.request.Request(url)
        # 네이버 인증 추가
        # req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        req.add_header('X-Naver-Client-Id', 'GWWUHPgV0uguJWvgsMFu')
        req.add_header('X-Naver-Client-Secret', 'slKycSCDf4')

        res = urllib.request.urlopen(req) # request 대한 response
        if res.getcode() == 200:
            print('URL request success')
        else:
            print('URL request failed')

        ret = res.read().decode('utf-8')
        if ret == None:
            return None
        else:
            return json.loads(ret)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()
