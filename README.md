# groceries project
Сайт на http://62.84.122.48/

Автор - Илья Рыкованов

Разворачивание
В папке infra 
docker-compose up --build
после python manage.py makemigrations
python manage.py migrate
в контейнерах infra-backend и infra-web

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
