def get_userid(db, login):
    """Получение id пользователя"""
    cur = db.cursor()
    userid = cur.execute("SELECT id from users WHERE login = ?", (login,)).fetchall()
    return userid[0][0]

def get_dict_clothes(db, userid: int):
    """Получение словаря для ипспользования в выводе генерации одежды и для инвертаря"""
    cur = db.cursor()
    dict_clothes = {}
    clothes = cur.execute("SELECT id, weather, type, mediumcolor, name from clothes WHERE userid = ?",
                          (userid,)).fetchall()
    return clothes