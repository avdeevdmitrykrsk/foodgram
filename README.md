# О проекте:
## У вас есть любимое блюдо? Блюдо, которое вы готовы вкушать всю жизнь...Блюдо, поедая которое вы хотите завопить -"Это лучшая еда во всем мире!". Есть? Тогда поделитесь рецептом с нами на [Фудграме](http://foodgram.myftp.org)!
## [Фудграм](http://foodgram.myftp.org) это сайт, на котором вы можете поделиться с нами рецептами самых изысканных блюд, которые кочевали из поколения в поколение и вот, настал момент, когда о нем должны узнать все! 
## Как же это сделать? Сейчас объясню на пальцах:
### Палец номер 1:
### **Клонировать репозиторий и перейти в него в командной строке:**
```python
git clone git@github.com:avdeevdmitrykrsk/foodgram.git
```
```python
cd foodgram
```
### Находясь в папке foodgram выполнить команду:
```python
docker compose up
```
### После этого Docker развернет контейнеры локально.


## Стек:
```python
  Django==3.2.16
```
```python
  djangorestframework==3.12.4
```
```python
  djoser==2.1.0
```
```python
  gunicorn==20.1.0
```
```python
  Pillow==9.0.0
```

## Перед началом, загрузите тестовые ингредиенты и тэги из CSV в БД.
```python
python manage.py load_ingredients
```
```python
python manage.py load_tags
```

## Порядок действий при регистрации:
### Для регистрации необходимо отправить POST, все поля обязательны к заполнению:
```python
https://foodgram.myftp.org/api/users/
```
```python
{
    "email": "example@yandex.ru",
    "username": "example.example",
    "first_name": "example",
    "last_name": "example",
    "password": "Qwerty123"
}
```

### Далее, необходимо отправить POST запрос для получения токена, все поля обязательны к заполнению:
```python
https://foodgram.myftp.org/api/auth/token/login/
```
```python
{
    "email": "example@yandex.ru",
    "password": "Qwerty123"
}
```

### Пользователи имеют возможность редактировать свой профиль, отправив PATCH, все поля обязательны к заполнению:
```python
https://foodgram.myftp.org/api/users/me/
```
```python
{
    "email": "new@yandex.ru",
    "username": "new.example",
    "first_name": "new",
    "last_name": "new",
    "password": "Qwerty123"
}
```

## Добавить аватар к профилю.
```python
https://foodgram.myftp.org/api/users/me/avatar/
```
```python
{
    "avatar": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAACAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
}
```

## Подписаться на пользователя.
```python
https://foodgram.myftp.org/api/users/<id>/subscribe/
```

## Добавление нового Рецепта:
### Post запрос. Все поля обязательны:
```python
https://foodgram.myftp.org/api/recipes/
```
```python
{
    "ingredients": [{"id": 1, "amount": 10}, {"id": 2, "amount": 20}],
    "tags": [1, 2],
    "name": "test_recipes1",
    "text": "sadfgsdfh",
    "cooking_time": 1,
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABiX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
}
```

## Добавить рецепт в избранное.
```python
https://foodgram.myftp.org/api/recipes/<id>/favorited/
```


## Добавить рецепт в корзину для покупок.
```python
https://foodgram.myftp.org/api/recipes/<id>/shopping_cart/
```

## Скачать список покупок.
```python
https://foodgram.myftp.org/api/recipes/download_shopping_cart/
```

### GitHub [avdeevdmitrykrsk](https://github.com/avdeevdmitrykrsk)
