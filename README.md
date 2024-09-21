# sarafan

Sarafan

### Описание:

Проект Sarafan -- это магазин, в котором пользователи могут искать необходимые продукты, проходить авторизацию и добавлять товары в корзину. В корзине вычисляется общее количество товаров и общая стоимость заказа. Покупатели могут устанавливать нужное количество каждого продукта. Администраторы могут добавлять (изменять, удалять) новые категории, подкатегории и продукты.

### Стек технологий:

* Python
* Django
* Django REST framework
* SQLite

### Как развернуть проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:NikitaPreis/sarafan.git
```

```
cd sarafan
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source venv/scripts/activate
```

Обновить pip и установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Список доступных эндпоинтов:

1) **Регистрация**
* http://127.0.0.1:8000/api/users/
2) **Авторизация**
* http://127.0.0.1:8000/auth/token/login/
3) **Просмотр категорий и подкатегорий**
* http://127.0.0.1:8000/api/categories/{category_id}
4) **Просмотр продуктов**
* http://127.0.0.1:8000/api/products/{product_id}
5) **Просмотр корзины покупателя**
* http://127.0.0.1:8000/api/products/get_shopping_cart/
6) **Добавить товар в корзину, изменить количество товара в корзине, удалить товар из корзины**
* http://127.0.0.1:8000/api/products/{product_id}/shopping_cart/
7) **Очистить корзину**
* http://127.0.0.1:8000/api/products/empty_shopping_cart/

### Примеры запросов и ответов

**Content type**:
```
application/json

```
**request samples №1:**
```
http://127.0.0.1:8000/api/users/
```

**payload №1:**

```
{
    "first_name": "Вадим",
    "last_name": "Вадимов",
    "username": "vadim_vadimov",
    "email": "some.mail@mail.ru",
    "password": "Qwerty123"
}
```

**response samples №1:**
```
{
    "id": 1
    "first_name": "Вадим",
    "last_name": "Вадимов",
    "username": "vadim_vadimov",
    "email": "some.mail@yandex.ru"
}
```



**request samples №2:**
```
http://127.0.0.1:8000/auth/token/login/
```

**payload №2:**

```
{
    "email": "some.mail@mail.ru",
    "password": "Qwerty123"
}
```

**response samples №2:**
```
{
    "auth_token": "f9994cbd33fa75d9cd781e202afab984d0eb3337"
}
```

**request samples №3:**

```
http://127.0.0.1:8000/api/categories/
```

**response samples №3:**
```
{
"count": 2,
"next": null,
"previous": null,
"results": [
    {
    "id": 1,
        "name": "Молочные продукты",
        "slug": "dairy-products",
        "image": "http://127.0.0.1:8000/media/categories/images/test_image_3.jpg",
        "subcategories": [
            {
                "id": 2,
                "name": "Молоко",
                "slug": "milk",
                "image": "http://127.0.0.1:8000/media/categories/images/test_image_2.jpeg"
            },
            {
                "id": 1,
                "name": "Мороженное",
                "slug": "ice-cream",
                "image": null
            }
        ]
    },
    {
        "id": 3,
        "name": "Мясо, птица, рыба",
        "slug": "meat-poultry-fish-products",
        "image": null,
        "subcategories": []
    }
  ]
}
```

**request samples №4:**

```
http://127.0.0.1:8000/api/products/
```


**response samples №4:**

```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "name": "Молоко «Простоквашино»",
            "slug": "milk-prostokvashino",
            "category": {
                "id": 1,
                "name": "Молочные продукты",
                "slug": "dairy-products",
                "image": "http://127.0.0.1:8000/media/categories/images/test_image_3.jpg"
            },
            "subcategory": {
                "id": 2,
                "name": "Молоко",
                "slug": "milk",
                "image": "http://127.0.0.1:8000/media/categories/images/test_image_2.jpeg"
            },
            "price": 90,
            "images": [
                {
                    "image_detail": "http://127.0.0.1:8000/media/products/detail/images/daa8ae9d-02c7-4003-9a53-f06b10ab2dd7.jpg",
                    "image_list": "http://127.0.0.1:8000/media/products/list/images/925b539a-9bdc-42ee-87b4-4aae3900dc3a.jpg",
                    "image_thumbnail": "http://127.0.0.1:8000/media/products/thumbnails/images/f075cc1c-6562-4f81-97dd-38da3455ea60.jpg"
                }
            ]
        },
        {
            "id": 1,
            "name": "Молоко «Фермерское»",
            "slug": "milk-farm",
            "category": {
                "id": 1,
                "name": "Молочные продукты",
                "slug": "dairy-products",
                "image": "http://127.0.0.1:8000/media/categories/images/test_image_3.jpg"
            },
            "subcategory": {
                "id": 2,
                "name": "Молоко",
                "slug": "milk",
                "image": "http://127.0.0.1:8000/media/categories/images/test_image_2.jpeg"
            },
            "price": 100,
            "images": []
        }
    ]
}

### Авторы:
* Никита, https://github.com/NikitaPreis
