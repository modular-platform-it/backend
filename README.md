
# Описание
Проект разработан в акселераторе [it-preactic ](https://github.com/itpractice-team)

## О проекте
Система для возможности создания персонального бота. 
Проект состоит из трех частей. Для двух частей требования будут заданы, требования для третьей части можно будет выработать участникам проекта.
Предоставляет возможность создания, управления ботами. Настройки логики поведения бота. 

## Технологии
- **Python - 3.11**
- **Django - 3.2**
- **DRF - 3.12.4**
- **PostgreSQL - 13.10**
- **Docker - 4.19**

## Авторы
- [Nikki Nikonor](https://github.com/Paymir121)
- [Орленко Олеся](https://github.com/olees-orlenko)
- [Рябов Игорь](https://github.com/Geroy4ik)
- [Кузин Сергей](https://github.com/sihuannewrise)

## Основная логика
### Архитектура приложения
### Приложение для управления ботами (приложение управления).
Django приложение. 
Предназначено для возможности отображения, добавления, удаления, редактирования, управления ботами.
- возможность авторизации пользователя в системе
Авторизация с использование токена. Нет разграничения принадлежности бота. Любой авторизовавшийся пользователь может взаимодействовать со всеми ботами.
- возможность  отображения состояния ботов
- возможность добавления бота
- возможность изменения настроек бота
- возможность добавления действий бота:
- В приложении управления добавляется бот, создаются действия. В действиях указывается сообщение, файлы, вопросы, которые будут отображаться пользователю; API, которое нужно вызвать, следующее действие. Введенная пользователем информация будет передаваться в API, которое настроено в действии бота. Также можно указать API, информация из которого будет отображаться пользователю.
- Должна быть возможность добавления, редактирования, удаления, копирования, включения, выключения действий.
- Должна быть доступна возможность тестирования бота. Тестирование производится в окне браузера.
возможность управления ботом:
- Должна быть возможность запуска, остановки, удаления бота; проверки доступности API; проверки ключа бота..

#### Серверная часть.
Серверное приложение, которое обеспечивает запуск и работу ботов.
- бота, который будет создаваться с учетом настроек, которые содержатся в приложении управления.
- ввозможность запуска ботов, которые были созданы в приложении управления. 
- ввозможность выполнения команд управления из приложения управления

#### Приложение для  тестирования работоспособности веб приложения управления и серверной части.
Django приложение, которое принимает запросы от бота. 
Как предложение - реализовать веб приложение, которое позволяет совершать покупки и отслеживать состояние доставки товара. В приложении через админку Джанго добавляем список товаров, пользователь через бота просматривает добавленные товары, покупает товар, по вводу идентификатора отслеживает состояние доставки.
- возможность отдачи списка товаров (текстовая и графическая информация),
совершение покупки
- отслеживания состояния доставки товара.

### Возможности пользователя
Невторизированный пользователь имеет возможность:
- 
Авторизованный пользователь имеет возможность:
- 
Администратор имеет возможность:
- 



## Для запуска проекта вам понадобится:

### Клонирование репозитория:
Просите разрешение у владельца репозитория( можно со слезами на глазах)
Клонируете репозиторий:

```bash
    git clone git@github.com:modular-platform-it/backend.git
```

### Cоздать  виртуальное окружение:
```bash
    python -m venv venv
```
# активировать виртуальное окружение, Если у вас Linux/macOS
```bash
    source venv/bin/activate
```
# Активировать виртуальное окружение, Если у вас windows
```bash
    source venv/scripts/activate
```

### Установить зависимости из файла requirements.txt:
```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```


### Выполнить миграции:
```bash
    python manage.py makemigrations
    python manage.py migrate
```

### Запустить проект:
```bash
    python manage.py runserver
```

### Создать суперпользователя:
```bash
    python manage.py createsuperuser
```

## Запуск докер контейнеров на локальной машине:

### Билдим проект и запускаем:
```bash
    docker compose up --build
```

### Выполнить миграции:
```bash
    docker compose exec backend python manage.py migrate
```

### Выполнить создание суперпользователя:
```bash
    docker compose exec backend python manage.py createsuperuser
```

### Выполнить Собрать статику Django:
```bash
    sudo docker compose  exec backend python manage.py collectstatic
    sudo docker compose  exec backend cp -r /app/collected_static/. /app/static/
```

## Запуск докер контейнеров на удаленной машине:

### Выполнить обновление apt:
```bash
    sudo apt update
```

### Билдим проект и запускаем:
```bash
    cd bot_controler
    sudo docker compose -f docker-compose.production.yml pull
    sudo docker compose -f docker-compose.production.yml down
    sudo docker compose -f docker-compose.production.yml up -d
    sudo docker system prune -af
```

### Выполнить миграции:
```bash
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```

### Выполнить миграции:
```bash
    docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```

### Выполнить Собрать статику Django:
```bash
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
    sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /app/static/
```

### Настройки nginx:
```bash
    sudo nano /etc/nginx/sites-enabled/default
```

## Примеры запросов и ответов к API
