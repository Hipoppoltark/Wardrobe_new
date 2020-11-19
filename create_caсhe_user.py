import os
from config import *


def create_cache(photo: list):
    """Создание кэша при авторизации или регистрации"""
    os.mkdir("photo_clothes")
    for id_photo, photo in photo:
        with open(PATH_FOLDER_PHOTO + str(id_photo) + '.jpg', 'tw', encoding='utf-8') as f:
            pass
        with open(PATH_FOLDER_PHOTO + str(id_photo) + '.jpg', "wb") as f:
            f.write(photo)