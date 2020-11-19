from main import *


class MyClothesWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        uic.loadUi('my_clothes.ui', self)
        self.setGeometry(0, 55, 572, 541)

        self.footwear = QWidget(self)
        self.scrollArea_3 = QScrollArea(self.footwear)
        self.scrollArea_3.setGeometry(24, 40, 529, 391)
        self.widget_footwear = QWidget(self)
        self.widget_footwear.setMinimumSize(529, 391)

        self.jackets = QWidget(self)
        self.scrollArea_4 = QScrollArea(self.jackets)
        self.scrollArea_4.setGeometry(24, 40, 529, 391)
        self.widget_jackets = QWidget(self)
        self.widget_jackets.setMinimumSize(529, 391)

        self.widget_outwear.setStyleSheet("background-color: rgb(253, 253, 255);")
        self.widget_underwear.setStyleSheet("background-color: rgb(253, 253, 255);")
        self.widget_footwear.setStyleSheet("background-color: rgb(253, 253, 255);")
        self.widget_jackets.setStyleSheet("background-color: rgb(253, 253, 255);")

        self.footwear.setGeometry(0, 0, 565, 451)
        self.jackets.setGeometry(0, 0, 565, 451)

        """Создание словаря с вещами для отображения"""
        self.connect_to_db = sqlite3.connect('wardrobe.sqlite')
        dict_clothes = get_dict_clothes(self.connect_to_db, self.parent().user_id)
        self.dict_clothes = {}
        for garment in dict_clothes:
            self.dict_clothes[garment[2]] = self.dict_clothes.get(garment[2], []) + [(garment[0],
                                                                                      garment[1],
                                                                                      garment[4])]
        """Заполнение лайаотами все категории с помощью словаря с одеждой"""
        for type in self.dict_clothes.keys():
            if type.lower() == "outwear":
                self.widget_outwear.setLayout(self.create_layout_for_widget(type, self.widget_outwear))
            elif type.lower() == "underwear":
                self.widget_underwear.setLayout(self.create_layout_for_widget(type, self.widget_underwear))
            elif type.lower() == "footwear":
                self.widget_footwear.setLayout(self.create_layout_for_widget(type, self.widget_footwear))
            else:
                self.widget_jackets.setLayout(self.create_layout_for_widget(type, self.widget_jackets))

        self.scrollArea.setWidget(self.widget_outwear)
        self.scrollArea_2.setWidget(self.widget_underwear)
        self.scrollArea_3.setWidget(self.widget_footwear)
        self.scrollArea_4.setWidget(self.widget_jackets)

        self.stackedWidget.addWidget(self.footwear)
        self.stackedWidget.addWidget(self.jackets)


        self.btn_outwear.clicked.connect(self.show_widget)
        self.btn_underwear.clicked.connect(self.show_widget)
        self.btn_footwear.clicked.connect(self.show_widget)
        self.btn_jackets.clicked.connect(self.show_widget)

        self.btn_outwear.setStyleSheet(ANIMATION_BTN)
        self.btn_underwear.setStyleSheet(ANIMATION_BTN)
        self.btn_footwear.setStyleSheet(ANIMATION_BTN)
        self.btn_jackets.setStyleSheet(ANIMATION_BTN)


    def show_widget(self):
        if self.sender().text().lower() == "outwear":
            self.stackedWidget.setCurrentIndex(0)
        elif self.sender().text().lower() == "underwear":
            self.stackedWidget.setCurrentIndex(1)
        elif self.sender().text().lower() == "footwear":
            self.stackedWidget.setCurrentIndex(2)
        else:
            self.stackedWidget.setCurrentIndex(3)

    def create_layout_for_widget(self, type: str, parent):
        """Добавление в layout карточек с вещами и их названием"""
        layout = Qt.QGridLayout(parent)
        i = 0
        j = 0
        for clothes in self.dict_clothes[type]:
            if i == 3:
                i = 0
                j += 1
            layout.addWidget(self.create_card_clothes(clothes), j, i)
            i += 1
        layout.setVerticalSpacing(25)
        return layout

    def create_card_clothes(self, clothes_info: tuple):
        self.card_clothes = QLabel(self)
        self.label_weather = QLabel(clothes_info[1], self.card_clothes)
        self.label_name = QLabel(clothes_info[2].title(), self.card_clothes)
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_name.setFont(font)
        self.label_name.setGeometry(0, 140, 133, 15)
        self.label_weather.setGeometry(10, 160, 133, 15)
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_weather.setFont(font)
        self.label_name.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.label_name.setStyleSheet("font-weight: 500;")
        self.pixmap = QPixmap(PATH_FOLDER_PHOTO + str(clothes_info[0]) + ".jpg")
        self.card_clothes.setPixmap(self.pixmap.scaled(153, 141))
        self.card_clothes.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.make_shadow()
        self.card_clothes.setGraphicsEffect(self.shadow)
        self.card_clothes.setMaximumSize(133, 181)
        self.card_clothes.setMinimumSize(133, 181)
        return self.card_clothes

    def make_shadow(self):
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(25)
        self.shadow.setXOffset(3)
        self.shadow.setYOffset(8)
        self.shadow.setColor(QColor(0, 0, 0, 18))