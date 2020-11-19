from view import *
import hashlib
from create_caсhe_user import create_cache


class AutorizationWindow(QMainWindow):
    """Класс авторизации, отдельное окно."""
    def __init__(self):
        super().__init__()
        uic.loadUi('autorization.ui', self)

        self.btn_signin.clicked.connect(self.change_widget_in)
        self.btn_signup.clicked.connect(self.change_widget_up)
        self.btn_signin_2.clicked.connect(self.change_widget_in)
        self.btn_signup_2.clicked.connect(self.change_widget_up)

        self.connect_to_db = sqlite3.connect('wardrobe.sqlite')

        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.registration)

    def change_widget_in(self):
        self.stackedWidget.setCurrentIndex(0)

    def change_widget_up(self):
        self.stackedWidget.setCurrentIndex(1)

    def login(self):
        text_login = self.line_login.text()
        password = self.line_password.text()
        text_password = hashlib.md5(password.encode("utf-8"))
        cur = self.connect_to_db.cursor()
        data = cur.execute("SELECT id, password from users WHERE login = ?", (text_login,)).fetchall()
        if self.check_on_correct_data_autorization(data, text_password):
            cur = self.connect_to_db.cursor()
            cache = cur.execute("SELECT id, photo from clothes WHERE userid = ?", (data[0][0],)).fetchall()
            create_cache([(elem[0], elem[1]) for elem in cache])

            with open("user_id.txt", "tw", encoding="utf-8") as f:
                pass
            with open("user_id.txt", "w") as f:
                f.write(str(data[0][0]))

            self.second_form = MainCapWidget(data[0][0])
            self.second_form.show()
            self.close()

    def check_on_correct_data_autorization(self, data: list, text_password):
        if not(data):
            self.statusBar().showMessage("No such user")
            return False
        elif data[0][1] != text_password.hexdigest():
            self.statusBar().showMessage("Wrong password")
            return False
        return True

    def registration(self):
        text_login = self.line_login_registration.text()
        text_password = self.line_password_registration.text()
        text_name = self.line_name.text()
        if self.check_on_correct_data_registration(text_login, text_password, text_name):
            text_password = hashlib.md5(text_password.encode("utf-8"))
            cur = self.connect_to_db.cursor()
            cur.execute("INSERT INTO users(login, password, name) VALUES(?, ?, ?)", (text_login,
                                                                                     text_password.hexdigest(),
                                                                                     text_name),)
            self.connect_to_db.commit()

            cur = self.connect_to_db.cursor()
            data = cur.execute("SELECT id from users WHERE login = ?", (text_login,)).fetchall()

            with open("user_id.txt", "tw", encoding="utf-8") as f:
                pass
            with open("user_id.txt", "w") as f:
                f.write(str(data[0][0]))

            self.second_form = MainCapWidget(data[0][0])
            self.second_form.show()
            self.close()

    def check_on_correct_data_registration(self, login, password, name):
        if not(name and password and name):
            self.statusBar().showMessage("Not all fields are filled")
            return False
        cur = self.connect_to_db.cursor()
        if cur.execute("SELECT id from users WHERE login = ?", (login,)).fetchall():
            self.statusBar().showMessage("User already exists")
            return False
        return True


if __name__ == '__main__':
    if not(os.path.exists("user_id.txt")):
        app = QApplication(sys.argv)
        ex = AutorizationWindow()
        ex.show()
        sys.exit(app.exec())
    else:
        app = QApplication(sys.argv)
        with open("user_id.txt", encoding="utf-8") as f:
            user_id = f.readline()
        ex = MainCapWidget(int(user_id))
        ex.show()
        sys.exit(app.exec())