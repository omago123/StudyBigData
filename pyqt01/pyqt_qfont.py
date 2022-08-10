import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt


# 클래스 oop
class qTemplate(QWidget):
    # 생성자
    def __init__(self) -> None:  # -> None return 하는 값이 없다. init은 기본적으로 None이다. - > str : string값을 return 한다.
        super().__init__()
        self.initUI()

    # 화면정의를 위한 사용자 함수
    def initUI(self) -> None:
        self.setGeometry(1000,300,900,700)
        self.setWindowTitle('QTemplate')
        self.text = 'What a wonderful world~'
        self.show()

        
    def paintEvent(self, event) -> None:
        paint = QPainter()
        paint.begin(self)
        # 그리는 함수 추가
        # class 내부함수에는 항상 self가 붙음 자기자신을 지칭
        self.drawText(event, paint)
        paint.end()


    def drawText(self, event, paint):
        paint.setPen(QColor(50,50,50))
        paint.setFont(QFont('NanumGothic', 20))
        paint.drawText(105, 100, 'HELL WORLD~')
        paint.setFont(QFont('Impact', 20))
        paint.setPen(QColor(0,250,10))
        paint.drawText(event.rect(), Qt.AlignCenter, self.text)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()