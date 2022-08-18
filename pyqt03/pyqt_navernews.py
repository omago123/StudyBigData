import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from urllib.parse import quote
import urllib.request
import json
import webbrowser
import pandas as pd

# 클래스 OOP
class qTemplate(QWidget):    
    start = 1
    maxDisplay = 100
    saveResult = []
    prevSearch = ''

    def __init__(self) -> None: # 생성자
        super().__init__() 
        uic.loadUi('./pyqt03/navernews_2.ui', self)
        self.initUI()

    def initUI(self) -> None:
        self.addControls()
        self.show()

    def addControls(self) -> None: # 위젯 정의, 이벤트(시그널) 처리
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        self.txtSearch.returnPressed.connect(self.btnSearchClicked)
        self.tblResult.itemSelectionChanged.connect(self.tblResultSelected)

        self.btnNext.clicked.connect(self.btnNextClicked)
        self.btnSave.clicked.connect(self.btnSaveClicked)

    def btnNextClicked(self) -> None:
        self.start = self.start + self.maxDisplay
        self.btnSearchClicked()

    def btnSaveClicked(self) -> None:
        if len(self.saveResult) > 0:
            df = pd.DataFrame(self.saveResult)
            df.to_csv(f'./pyqt03/{self.txtSearch.text()}_뉴스검색결과.csv', encoding='utf-8', index=True)
        
        QMessageBox.information(self, '저장', '파일저장완료!!')
        # 저장후 모든 변수 초기화
        self.saveResult = []
        self.start = 1
        self.txtSearch.setText("")
        self.lblStatus.setText('Data :')
        self.lblStatus2.setText('저장할데이터 > 0개')
        self.tblResult.setRowCount(0)
        self.btnNext.setEnabled(True)

    def tblResultSelected(self) -> None:
        selected = self.tblResult.currentRow() # 현재 선택된 열의 인덱스
        link = self.tblResult.item(selected, 1).text()
        webbrowser.open(link)

    def btnSearchClicked(self) -> None: # 슬롯(이벤트핸들러)        
        jsonResult = []
        totalResult = []
        keyword = 'news'
        search_word = self.txtSearch.text()
        display_count = self.maxDisplay

        # QMessageBox.information(self, '결과', search_word)
        jsonResult = self.getNaverSearch(keyword, search_word, self.start, display_count)
        # print(jsonResult)

        for post in jsonResult['items']:
            totalResult.append(self.getPostData(post))

        # print(totalResult)
        total_count = jsonResult['total']
        self.makeTable(totalResult)
        curr_count = (self.start+display_count)-1
        self.lblStatus.setText(f'Data : {curr_count}/{total_count}')

        # 저장위치에 추가
        for post in totalResult:
            self.saveResult.append(post[0])

        self.lblStatus2.setText(f'저장할데이터 > {len(self.saveResult)}')
        if curr_count >= 1000:
            self.btnNext.setDisabled(True)
        else:
            self.btnNext.setEnabled(True)

    def makeTable(self, result):
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblResult.setColumnCount(2)
        self.tblResult.setRowCount(len(result)) # displayCount에 따라서 변경, 현재는 50
        self.tblResult.setHorizontalHeaderLabels(['기사제목','뉴스링크'])
        self.tblResult.setColumnWidth(0, 350)
        self.tblResult.setColumnWidth(1, 100)
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers) # readonly

        i = 0
        for item in result:
            title = self.strip_tag(item[0]['title'])
            link = item[0]['originallink']
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))
            self.tblResult.setItem(i, 1, QTableWidgetItem(link))
            i += 1

    def strip_tag(self, title): # html 태그를 없애주는 함수
        ret = title.replace('&lt;', '<')
        ret = ret.replace('&gt;', '>')
        ret = ret.replace('&quot;', '"')
        ret = ret.replace('&apos;', "'")
        ret = ret.replace('&amp;', '&')
        ret = ret.replace('<b>', '')
        ret = ret.replace('</b>', '')
        return ret

    def getPostData(self, post):
        temp = []
        title = self.strip_tag(post['title'])
        description = post['description']
        originallink = post['originallink']
        link = post['link']
        pubDate = post['pubDate']

        temp.append({'title':title
                    ,'description':description
                    ,'originallink':originallink
                    ,'link':link
                    ,'pubDate':pubDate}) # 220818 pubDate 빠진거 추가

        return temp

    # 네이버API 크롤링 함수
    def getNaverSearch(self, keyword, search, start, display):
        url = f'https://openapi.naver.com/v1/search/{keyword}.json' \
              f'?query={quote(search)}&start={start}&display={display}'
        print(url)
        req = urllib.request.Request(url)
        # 네이버 인증 추가
        req.add_header('X-Naver-Client-Id', 'JqpkgFJJbXWXTzhAEa4i')
        req.add_header('X-Naver-Client-Secret', 'tSLsq0RhsE')

        res = urllib.request.urlopen(req)
        if res.getcode() == 200:
            print('URL request succeed')
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