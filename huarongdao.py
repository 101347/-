import os
import sys
import random
from enum import IntEnum
import numpy as np
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QGridLayout, QMessageBox, QTextEdit, QPushButton, \
    QTextBrowser
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PIL import Image
import time
from Prediction import Prediction


# 开始界面
class start(QWidget):
    def __init__(self):
        super().__init__()
        self.gltMain = QGridLayout()
        self.initUI()

    def initUI(self):
        self.gltMain.setSpacing(0)
        self.setWindowTitle('开始界面')
        self.setFixedSize(600, 700)
        # self.setWindowFlags(Qt.FramelessWindowHint)   # 去掉窗口标题栏和按钮
        self.setStyleSheet(
            "background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F0968C,stop:1 #FFFFCC)")   # 设置背景颜色
        self.text = QTextBrowser(self)
        self.text.setText('华容道')
        self.text.setFont(QFont("楷体", 45, QFont.Bold))
        self.text.setAttribute(Qt.WA_TranslucentBackground)  # 设置文本框透明
        self.text.setStyleSheet("border:none;")  # 去边框
        self.text.move(100, 50)

        self.button1 = QPushButton('进入游戏', self)
        self.button1.clicked.connect(self.get_key1)
        self.button1.setStyleSheet(
            'color: rgb(112,0,0);background-color: #FFFF66 ;border-style:none;border:1px solid #3f3f3f; padding:40px;border-radius:15px;')
        self.button1.move(400, 350)

        self.button2 = QPushButton('退出游戏', self)
        self.button2.clicked.connect(self.close)
        self.button2.setStyleSheet(
            'color: rgb(112,0,0);background-color: #FFFF66 ;border-style:none;border:1px solid #3f3f3f; padding:40px;border-radius:15px;')
        self.button2.move(400, 500)

        self.show()

    def get_key1(self):
        self.hide()
        self.Huarongdao = NumberHuaRong()  # 进入游戏界面部分


# 用枚举类表示方向
class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


# 游戏界面
class NumberHuaRong(QWidget):
    #   随机选取图片
    def select_picture(self):
        self.pic_no = random.randint(0, len(fs))
        img = Image.open('./无框字符/' + fs[self.pic_no])
        self.save_path = r"picture"
        self.save(self.save_path, self.cut_image(img))

    # 切分成3*3
    def cut_image(self, image):
        width, height = image.size
        item_width = int(width / 3)
        box_list = []
        for i in range(0, 3):
            for j in range(0, 3):
                box = (j * item_width, i * item_width, (j + 1) * item_width, (i + 1) * item_width)
                box_list.append(box)
        image_list = [image.crop(box) for box in box_list]
        return image_list

    # 将9张子图存入'picture'文件夹
    def save(self, path, image_list):
        if not os.path.exists(path):
            os.mkdir('picture')  # 在当前文件夹创建文件夹
        index = 1
        for image in image_list:
            image.save("./picture/" + str(index) + '.jpg')
            index += 1

    def __init__(self):
        self.select_picture()
        super().__init__()
        self.lock = 0  # 键盘输入控制
        self.blocks = []
        self.gltMain = QGridLayout()
        self.re_count = 0
        self.best = 1000000
        self.initUI()

    def initUI(self):
        self.gltMain.setSpacing(0)   # 设置方块间隔

        self.button1 = QPushButton('开始游戏', self)
        self.button1.setStyleSheet('color:rgb(150, 0, 0)')
        self.button1.clicked.connect(self.get_key1)
        self.button1.move(250, 10)

        self.button2 = QPushButton('重新打乱', self)
        self.button2.setStyleSheet('color:rgb(150, 0, 0)')
        self.button2.clicked.connect(self.get_key2)
        self.button2.move(250, 40)

        self.button3 = QPushButton('获取提示', self)
        self.button3.setStyleSheet('background-color: rgb(255,204,255)')
        self.button3.clicked.connect(self.get_key3)
        self.button3.move(250, 70)

        self.text1 = QTextBrowser(self)
        self.text1.setText('请点击"开始游戏"')
        self.text1.setStyleSheet("background-color: rgb(200,200,200)")  # 6A5ACD
        self.gltMain.addWidget(self.text1, 0, 0, 1, 1)

        self.text2 = QTextBrowser(self)
        self.text2.setText("挑战记录")
        self.text2.setStyleSheet("background-color: rgb(200,200,200)")
        self.gltMain.addWidget(self.text2, 0, 2, 1, 3)

        self.onInit()
        self.setLayout(self.gltMain)
        self.setFixedSize(600, 700)   # 设置宽和高
        self.setWindowTitle('华容道')   # 设置标题
        self.setStyleSheet("background-color: white")   # 设置背景颜色
        self.show()

    def get_key1(self):
        self.onInit()
        # 打乱数组
        for i in range(500):
            random_num = random.randint(0, 2)
            self.move(Direction(random_num))
        self.updatePanel()
        self.text1.setText("请通过wasd按键进行游戏")
        self.lock = 1

    def get_key2(self):
        self.get_key1()

    # AI
    def get_key3(self):
        key = Prediction().pre_next(np.array(self.blocks), self.zero_row, self.zero_column)
        if key == 0:
            self.text1.setText("提示：按'w'键向上走")
        if key == 1:
            self.text1.setText("提示：按'a'键向右走")
        if key == 2:
            self.text1.setText("提示：按's'键向下走")
        if key == 3:
            self.text1.setText("提示：按'd'键向右走")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "是否确定退出?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # 强制调换
    def swap(self):
        time.sleep(1)
        self.text1.setText("进行强制调换!")
        if self.flag == 1:
            self.move(Direction.DOWN)
        if self.flag == 2:
            self.move(Direction.UP)
        if self.flag == 3:
            self.move(Direction.RIGHT)
        if self.flag == 4:
            self.move(Direction.LEFT)
        self.updatePanel()
        self.lock = 1

    # 初始化布局
    def onInit(self):
        self.blocks = []
        self.count = 0  # 步数（排行用）
        self.numbers = list(range(1, 9))
        self.numbers.append(0)
        self.step = 10
        for row in range(3):
            self.blocks.append([])
            for column in range(3):
                temp = self.numbers[row * 3 + column]
                if temp == 0:
                    self.zero_row = row
                    self.zero_column = column
                self.blocks[row].append(temp)
        self.updatePanel()

    # 监听键盘输入
    def keyPressEvent(self, event):
        if self.step == 0:
            self.swap()
            self.step = 10
        else:
            if self.lock:
                key = event.key()
                if key == Qt.Key_W:
                    self.f = 1
                    self.move(Direction.UP)
                    self.step -= 1
                if key == Qt.Key_S:
                    self.f = 2
                    self.move(Direction.DOWN)
                    self.step -= 1
                if key == Qt.Key_A:
                    self.f = 3
                    self.move(Direction.LEFT)
                    self.step -= 1
                if key == Qt.Key_D:
                    self.f = 4
                    self.move(Direction.RIGHT)
                    self.step -= 1
                if self.step == 0:
                    self.lock = 0
                    self.text1.setText("按下任意键进行强制调换")
                    self.flag = self.f
                else:
                    self.text1.setText("剩余%d步进行强制调换" % self.step)
                self.updatePanel()
                if self.checkResult():
                    if QMessageBox.Ok == QMessageBox.information(self, '结果', '恭喜你成功复原'):
                        self.onInit()

    # 方块移动算法
    def move(self, direction):
        self.count += 1
        if direction == Direction.DOWN:  # 上
            if self.zero_row != 2:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row + 1][self.zero_column]
                self.blocks[self.zero_row + 1][self.zero_column] = 0
                self.zero_row += 1
        if direction == Direction.UP:  # 下
            if self.zero_row != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row - 1][self.zero_column]
                self.blocks[self.zero_row - 1][self.zero_column] = 0
                self.zero_row -= 1
        if direction == Direction.RIGHT:  # 左
            if self.zero_column != 2:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column + 1]
                self.blocks[self.zero_row][self.zero_column + 1] = 0
                self.zero_column += 1
        if direction == Direction.LEFT:  # 右
            if self.zero_column != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column - 1]
                self.blocks[self.zero_row][self.zero_column - 1] = 0
                self.zero_column -= 1

    def updatePanel(self):
        for row in range(3):
            for column in range(3):
                self.lab = QLabel()
                self.lab.setPixmap(QPixmap('./picture/%d.jpg' % self.blocks[row][column]))
                self.lab.setScaledContents(True)
                self.gltMain.addWidget(self.lab, row + 1, column)
        self.setLayout(self.gltMain)

    # 检测是否完成
    def checkResult(self):
        # 先检测最右下角是否为0
        if self.blocks[2][2] != 0:
            return False

        for row in range(3):
            for column in range(3):
                # 运行到此处说名最右下角已经为0，pass即可
                if row == 2 and column == 2:
                    pass
                # 值是否对应w
                elif self.blocks[row][column] != row * 3 + column + 1:
                    return False
        self.text1.setText("点击“开始游戏”进行下一局")
        self.select_picture()
        self.lock = 0
        self.step = 10
        self.rank()
        return True

    def rank(self):
        self.count -= 500  # 扣去随机打乱移动的500次
        if self.count < self.best:
            self.best = self.count
        self.text2.setText(
            "本局步数: " + str(self.count) + "\n" + "上局步数: " + str(self.re_count) + "\n" + "最佳成绩: " + str(self.best))
        self.re_count = self.count


if __name__ == '__main__':
    step = 10   # 用于强制调换的步数变量
    fs = []   # 用于存储图片名的列表
    fs = os.listdir('./无框字符/')
    app = QApplication(sys.argv)
    ex = start()
    sys.exit(app.exec_())
