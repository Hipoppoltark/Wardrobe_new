import sqlite3
import sys

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import QTransform
from PyQt5 import uic, Qt, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QStatusBar, QScrollArea
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QColor, QFont
import os
import datetime as dt
from random import choice

from data_user import get_dict_clothes

from config import *


class MainWidget(QWidget):
    """Виджет главного окна (включает добавление одежды и генерацию образа)"""
    def __init__(self, parent):
        super().__init__(parent=parent)
        uic.loadUi('widget.ui', self)
        self.setGeometry(0, 55, 572, 541)

        self.InitUi()

        self.type_clothes = [self.radioButton, self.radioButton_2, self.radioButton_3, self.radioButton_4]
        self.radioButton.setChecked(True)
        self.weather_season = [self.radioButton_6, self.radioButton_7, self.radioButton_8, self.radioButton_21]
        self.radioButton_21.setChecked(True)

    def InitUi(self):
        self.btn_add_photo.setStyleSheet(ANIMATION_BTN)
        self.btn_add_photo.clicked.connect(self.add_photo)

        self.btn_add_clothes.clicked.connect(self.add_clothes_to_db)

        self.connect_to_db = sqlite3.connect('wardrobe.sqlite')

        dict_clothes = get_dict_clothes(self.connect_to_db, self.parent().user_id)
        self.dict_clothes = {}
        for garment in dict_clothes:
            self.dict_clothes[garment[1]] = self.dict_clothes.get(garment[1], {})
            self.dict_clothes[garment[1]][garment[2]] = self.dict_clothes[garment[1]].get(garment[2], []) + \
                                                        [(garment[0],
                                                          garment[3],
                                                          garment[4])]


        self.status = QStatusBar(self.parent())
        self.status.move(0, 585)
        self.status.resize(220, 30)

        self.pushButton_look.clicked.connect(self.change_widget)
        self.pushButton_adding.clicked.connect(self.change_widget)
        self.current_index_widget = 1

        self.months = {
            "01": "Winter",
            "02": "Winter",
            "03": "Spring",
            "04": "Spring",
            "05": "Spring",
            "06": "Summer",
            "07": "Summer",
            "08": "Summer",
            "09": "Autumn",
            "10": "Autumn",
            "11": "Autumn",
            "12": "Winter",
        }
        self.btn_generate.clicked.connect(self.generate_look_today)

        self.img_outwear.hide()
        self.img_underwear.hide()
        self.img_footwear.hide()
        self.img_jackets.hide()
        self.label_10.hide()
        self.label_11.hide()
        self.label_12.hide()
        self.label_13.hide()

        """Убрать потом"""
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(40)
        self.shadow.setXOffset(4)
        self.shadow.setYOffset(9)
        self.shadow.setColor(QColor(0, 0, 0, 30))
        self.widget.setGraphicsEffect(self.shadow)

        self.make_shadow()
        self.img_outwear.setGraphicsEffect(self.shadow)
        self.make_shadow()
        self.img_underwear.setGraphicsEffect(self.shadow)
        self.make_shadow()
        self.img_footwear.setGraphicsEffect(self.shadow)
        self.make_shadow()
        self.img_jackets.setGraphicsEffect(self.shadow)
        "0 2px 7px 0 rgba(10,10,10,.05), 3px 27px 54px -34px rgba(0,0,0,.47)"

    def make_shadow(self):
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(25)
        self.shadow.setXOffset(3)
        self.shadow.setYOffset(8)
        self.shadow.setColor(QColor(0, 0, 0, 18))

    def change_widget(self):
        """Смена виджетов (добавление одежды и генерация)"""
        self.stackedWidget.setCurrentIndex(self.current_index_widget)
        if self.current_index_widget == 0:
            self.current_index_widget = 1
        else:
            self.current_index_widget = 0

    def change_status(self, msg, color):
        self.status.setStyleSheet("color: " + color + ";")
        self.status.showMessage(msg)

    def add_photo(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Выбрать фото', '')[0]

    def find_middle_color_img(self, fname):
        im = Image.open(fname)
        pixels = im.load()
        x, y = im.size
        rgb = (0, 0, 0)
        for i in range(x):
            for j in range(y):
                now_rgb = pixels[i, j]
                rgb = [elem + now_rgb[i] for i, elem in enumerate(rgb)]
        return f"{rgb[0] // (x * y)}, {rgb[1] // (x * y)}, {rgb[2] // (x * y)}"

    def read_image(self, filename):
        try:
            fin = open(filename, "rb")
            img = fin.read()
            return img
        except IOError as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)
        finally:
            if fin:
                fin.close()

    def add_clothes_to_db(self):
        """Главная функция добавления одежды"""
        if self.check_error_in_forms_add_clothes():
            text_type_clothes = list(filter(lambda radiobtn: radiobtn.isChecked(), self.type_clothes))[0].text()
            text_weather_season = list(filter(lambda radiobtn: radiobtn.isChecked(), self.weather_season))[0].text()
            name_clothes = self.line_name_clothes.text()
            medium_color_img = self.find_middle_color_img(self.fname)
            img_for_db = sqlite3.Binary(self.read_image(self.fname))


            cur = self.connect_to_db.cursor()
            userid = self.parent().user_id
            cur.execute("INSERT INTO clothes(photo, weather, type, mediumcolor, name, userid) "
                        "VALUES (?, ?, ?, ?, ?, ?)", (img_for_db,
                                                   text_weather_season,
                                                   text_type_clothes,
                                                   medium_color_img,
                                                   name_clothes,
                                                   userid,))
            self.connect_to_db.commit()

            self.line_name_clothes.setText("")

            self.add_cache(text_weather_season, text_type_clothes, medium_color_img, name_clothes, img_for_db)

            self.change_status("Successful", "green")

    def add_cache(self, weather, type, medium_color, name_clothes, img_for_db):
        """Добавление кэша(вызывается функцией add_clothes_to_db)"""
        cur = self.connect_to_db.cursor()
        id_clothes = cur.execute("SELECT id from clothes").fetchall()
        id_clothes.sort(key=lambda x: x[0])
        self.dict_clothes[weather] = self.dict_clothes.get(weather, {})
        self.dict_clothes[weather][type] = self.dict_clothes[weather].get(
            type, []
        ) + [(id_clothes[-1][0], medium_color, name_clothes)]

        with open(PATH_FOLDER_PHOTO + str(id_clothes[-1][0]) + '.jpg', 'tw', encoding='utf-8') as f:
            pass
        f = open(PATH_FOLDER_PHOTO + str(id_clothes[-1][0]) + '.jpg', "wb")
        f.write(img_for_db)

    def check_error_in_forms_add_clothes(self):
        if self.line_name_clothes.text() == "":
            self.change_status("Name is not filled", "red")
            return False
        try:
            if self.fname:
                pass
        except AttributeError:
            self.change_status("Photo is not filled", "red")
            return False
        self.parent().statusBar().showMessage("")
        return True

    def generate_look_today(self):
        """Главная функция генерации образа"""
        self.show_and_hide_elem_clothes()

        self.label_not_selected.hide()
        month = self.months[dt.datetime.now().strftime("%m")]
        weather_clothes = self.dict_clothes.get(month, False)
        if not(weather_clothes):
            self.status.setStyleSheet("color: red;")
            self.status.showMessage("No suitable clothes")
            return False
        self.outerwear_clothes = weather_clothes.get("Outwear", False)
        self.underwear_clothes = weather_clothes.get("Underwear", False)
        self.footwear_clothes = weather_clothes.get("Footwear", False)
        self.jackets_and_coat_clothes = weather_clothes.get("Jackets, coat", False)

        if self.check_existence_required_types_clothing():
            if self.footwear_clothes and self.jackets_and_coat_clothes:
                self.display_сlothes_in_widget(("outwear", choice(self.outerwear_clothes)),
                                                ("underwear", choice(self.underwear_clothes)),
                                                ("footwear", choice(self.footwear_clothes)),
                                                ("jackets", choice(self.jackets_and_coat_clothes)))
            elif self.footwear_clothes:
                self.display_сlothes_in_widget(("outwear", choice(self.outerwear_clothes)),
                                                ("underwear", choice(self.underwear_clothes)),
                                                ("footwear", choice(self.footwear_clothes)))
            elif self.jackets_and_coat_clothes:
                self.display_сlothes_in_widget(("outwear", choice(self.outerwear_clothes)),
                                                ("underwear", choice(self.underwear_clothes)),
                                                ("jackets", choice(self.jackets_and_coat_clothes)))
            else:
                self.display_сlothes_in_widget(("outwear", choice(self.outerwear_clothes)),
                                                ("underwear", choice(self.underwear_clothes)))

    def show_and_hide_elem_clothes(self):
        """Функция, показывающая карточки одежды при нажатии на кнопку для генерации"""
        self.label_not_selected.hide()
        self.img_outwear.show()
        self.img_underwear.show()
        self.img_footwear.show()
        self.img_jackets.show()
        self.label_10.show()
        self.label_11.show()
        self.label_12.show()
        self.label_13.show()

    def check_existence_required_types_clothing(self):
        if not(self.outerwear_clothes) or not(self.underwear_clothes):
            self.change_status("Not clothes for generate look", "red")
            return False
        elif not(self.footwear_clothes):
            self.change_status("Genered imperfect look", "yellow")
            return True
        return True

    def display_сlothes_in_widget(self, *clothes):
        """Функия, заполняющая карточки изображением и текстом"""
        for thing in clothes:
            self.now_pixmap_clothes = self.create_pixmap_clothes(thing[1][0])
            if thing[0] == "outwear":
                self.img_outwear.setPixmap(self.now_pixmap_clothes)
                self.label_name_outwear.setText(thing[1][2].title())
            if thing[0] == "underwear":
                self.img_underwear.setPixmap(self.now_pixmap_clothes)
                self.label_name_underwear.setText(thing[1][2].title())
            if thing[0] == "footwear":
                self.img_footwear.setPixmap(self.now_pixmap_clothes)
                self.label_name_footwear.setText(thing[1][2].title())
            if thing[0] == "jackets":
                self.img_jackets.setPixmap(self.now_pixmap_clothes)
                self.label_name_jackets.setText(thing[1][2].title())

    def create_pixmap_clothes(self, clothes_id: int):
        self.pixmap = QPixmap(PATH_FOLDER_PHOTO + str(clothes_id) + ".jpg")
        return self.pixmap.scaled(self.img_outwear.size().width() + 20, self.img_outwear.size().height() - 40)