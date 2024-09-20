import os
from uuid import uuid4

from PIL import Image as Img

from sarafan.settings import BASE_DIR


def get_uuid_image_name():
    return f'{uuid4()}.jpg'


def save_image_in_current_size(image, size, image_directory):
    PATH_WITHOUT_MEDIA_PREFIX = 5
    image = Img.open(image)
    image_resized = image.resize(size, Img.LANCZOS)
    image_path = (f'media/products/{image_directory}/'
                  f'images/{get_uuid_image_name()}')
    image_resized.save(os.path.join(BASE_DIR, image_path))
    image.close()
    return image_path[PATH_WITHOUT_MEDIA_PREFIX:]
