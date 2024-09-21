import os
from uuid import uuid4

from PIL import Image as Img

from core import constants as const
from sarafan.settings import BASE_DIR


def get_uuid_image_name():
    return f'{uuid4()}.jpg'


def save_image_in_current_size(image, size, image_directory):
    """Сохранить изображение в заданном размере."""
    image = Img.open(image)
    image_resized = image.resize(size, Img.LANCZOS)
    path_to_file = (f'media/products/{image_directory}/images/')
    image_path = (f'media/products/{image_directory}/'
                  f'images/{get_uuid_image_name()}')
    os.makedirs(path_to_file, exist_ok=True)
    image_resized.save(os.path.join(BASE_DIR, image_path))
    image.close()
    return image_path[const.PATH_WITHOUT_MEDIA_PREFIX:]
