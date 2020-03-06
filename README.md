# customer-support-chatbot

Реализация чат-ботов поддержки клиентов с использованием сервиса Dialogflow на Google Cloud Platform.

У большинства компаний, которые взаимодействуют с людьми (покупатели, пользователи и пр.), есть служба поддержки. Сотрудникам службы поддержки приходится постоянно отвечать на однотипные вопросы пользователей. Это отнимает время, которое можно потратить на решение сложных и нетривиальных проблем.  

Данную проблему можно решить с помощью бота-помощника. Он будет закрывать все типичные вопросы, а вот что-то посложнее – перенаправлять на операторов. По предварительной оценке, это на 70% сократит время ожидания ответа и на 90% повысит довольство жизнью сотрудников службы поддержки.  

Специфика в том, что все люди разные и никогда не знаешь, как им придёт в голову сформулировать вопрос, предсказать варианты заранее невозможно. Поэтому бот будет подключен к сервису [Dialogflow](https://dialogflow.cloud.google.com/).  

Dialogflow — это сервис, позволяющий создавать чат-ботов для разных платформ и языков на разных устройствах. Принимая запрос в виде текста на естественном языке или некого события, Dialogflow согласовывает запрос с наиболее подходящим шаблоном. При этом он основывается на информации, содержащейся в шаблоне (примеры, сущности, контекст, параметры) и машинном обучении. Dialogflow  формирует ответный запрос и возвращает данные в виде объекта ответа JSON.

### Демо чат-бот для Telegram [https://t.me/serv_supp_bot](https://t.me/serv_supp_bot)  
Пример результата для Telegram:    

![Telegram animation](https://dvmn.org/media/filer_public/7a/08/7a087983-bddd-40a3-b927-a43fb0d2f906/demo_tg_bot.gif)

### Демо чат-бот для Вконтакте [https://vk.com/im?sel=-192417010](https://vk.com/im?sel=-192417010)

Пример результата для ВКонтакте:  

![VKontakte animation](https://dvmn.org/media/filer_public/1e/f6/1ef61183-56ad-4094-b3d0-21800bdb8b09/demo_vk_bot.gif)

## Создание агента в DialogFlow

"Агент" — это что-то вроде "бота" в Telegram, только в DialogFlow.  

Для начала нужно создать аккаунт в Google Cloud Platform: [https://console.cloud.google.com/](https://console.cloud.google.com/).  

После создания аккаунта в Google Cloud Platform создаем проект:
![Google Cloud Platform project](https://raw.githubusercontent.com/igorzakhar/customer-support-chatbot/master/media/Google_Cloud_Platform.png)

После создания проекта в создаем проект в сервисе DialogFlow: [https://cloud.google.com/dialogflow/docs/quick/setup](https://cloud.google.com/dialogflow/docs/quick/setup).  

Далее нужно создать агента через консоль DialogFlow: [https://cloud.google.com/dialogflow/docs/quick/build-agent](https://cloud.google.com/dialogflow/docs/quick/build-agent). При создании агента выбираем язык, на котором будем общаться с пользователями. Так же при создании агента понадобится идентификатор проекта Google Cloud Platform.  

![DialogFlow create agent](https://raw.githubusercontent.com/igorzakhar/customer-support-chatbot/master/media/Dialogflow.png)

## "Обучение" бота

Для обучения бота создайте новый __Intent__ и добавьте несколько тренировочных фраз в секции __Training phrases__. Чтобы бот что-то ответил, ему нужно добавить текст ответа в секции __Response__. Затем можно попробовать пообщаться с ботом в меню слева-сверху (см. скриншот).  

![DialogFlow Intent](https://raw.githubusercontent.com/igorzakhar/customer-support-chatbot/master/media/Dialogflow_Intent.png)

Чтобы бот хорошо натренировался, фразы должны быть разными. Добавьте 5-6 вариантов приветствия разными словами. 

Так же можно "обучить" бота с помощью скрипта ```create_dialogflow_intent.py```. Для этого нужно указать путь до файла с тренировочными фразами и ответами. Пример запуска:
```bash
$ python create_dialogflow_intent.py intents/questions.json  
```

Файл должен быть следующего содержания:
```
{
    "Удаление аккаунта": {
        "questions": [
            "Хочу удалить аккаунт",
            "Удалить аккаунт",
            "Как удалить аккаунт",
            "Как удалить данные обо мне",
            "Удалить мои статьи",
            "Как снести свой аккаунт"
        ],
        "answer": "Если вы хотите удалить аккаунт, это можно сделать в вашем профиле в разделе «Настройки». Пролистайте этот раздел до зоны, выделенной красным."
    },
    "Название": {
        "questions": [
            "Фраза",
            "Ещё одна фраза",
            "Какая-то фраза",
            "...",
        ],
        "answer": "Текст ответа."
    },
...
...
}

```
Пример файла с тренировочными фразами и ответами можно найти в каталоге ```intents``` этого репозитория: [intents/questions.json](https://github.com/igorzakhar/customer-support-chatbot/blob/master/intents/questions.json). 

## Запуск бота на сервере

Для размещения бота можно использовать платформу [Heroku](https://www.heroku.com/). Бесплатный вариант включает 550 бесплатных часов в месяц.

#### Регистрируем учетную запись и создаем приложение(app) на платформе [Heroku](https://www.heroku.com/):


Получится страница, как на скриншоте ниже:
![Heroku app](https://raw.githubusercontent.com/igorzakhar/customer-support-chatbot/master/media/heroku_app.png)

#### Привязываем репозиторий с кодом на Github к приложению на платформе Heroku

Далее нужно разместить репозиторий с кодом бота на своём аккаунте GitHub. Репозиторий должен содержать файл ```requirements.txt``` в котором прописаны зависимости. **Файл ```.env``` публиковать нельзя.**

Затем нужно привязать свой аккаунт GitHub к аккаунту Heroku. Это можно сделать на вкладке **Deploy** в разделе панели инструментов платформы Heroku. В разделе **Deployment method**  выберите **GitHub**, потом найдите свой репозиторий с помощью поиска и подключите его к Heroku.

![Heroku github connect](https://raw.githubusercontent.com/igorzakhar/customer-support-chatbot/master/media/heroku_github_connect.png)

#### Добавляем переменные окружения 

В панели инструментов платформы Heroku переходим на вкладку **Settings** и в разделе **Config Vars** добавляем переменные окружения которые использует бот.  

При использовании библиотеки [Dialogflow](https://github.com/googleapis/dialogflow-python-client-v2) потребуется установить переменную окружения __```GOOGLE_APPLICATION_CREDENTIALS```__. В переменной окружения __```GOOGLE_APPLICATION_CREDENTIALS```__ указывается путь к файлу JSON, который содержит ключ вашего сервисного аккаунта в Google Cloud. Для создания файла JSON с ключами воспользуйтесь следующей инструкцией [https://cloud.google.com/docs/authentication/getting-started#creating_a_service_account](https://cloud.google.com/docs/authentication/getting-started#creating_a_service_account).  

Объявите переменные среды из панели инструментов Heroku следующим образом: в значение переменной __```GOOGLE_CREDENTIALS```__ вставляем содержимое файла JSON c ключами  сервисного аккаунта в Google Cloud.  Для переменной среды __```GOOGLE_APPLICATION_CREDENTIALS```__ указываем имя файла ```google-credentials.json```.  

Когда переменные объявлены, добавьте buildpack через панель инструменов Heroku в разделе **Settings**:
![Heroku settings buildpack](https://raw.githubusercontent.com/igorzakhar/customer-support-chatbot/master/media/heroku_buildpacks.png)

или из командной строки (нужен предустановленный клиент [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)):
```bash
$ heroku buildpacks:add https://github.com/gerywahyunugraha/heroku-google-application-credentials-buildpack
```

Данный buildpack автоматически сгенерирует файл```google-credentials.json``` и заполнит его содержимым содержимого учетных данных Google.


>*Buildpacks - это скрипты, которые запускаются при развертывании вашего приложения. Они используются для установки зависимостей для вашего приложения и настройки среды.*

Добавте остальные переменные окружения. Список всех переменных окружения которые нужны для работы приложения.

- __```TELEGRAM_API_TOKEN```__ - токет чат-бота в Telegram;
- __```DIALOGFLOW_PROJECT_ID```__ - идентификатор проекта в Dialogflow;
- __```VK_TOKEN```__ - токен группы ВКонтакте;
- __```LOGGER_TOKEN```__ - токен бота Telegram для мониторинга работы чат-ботов которому отправляются логи;
- __```LOGGER_CHAT_ID```__ - ID чата в который отправляются логи приложений;
- __```GOOGLE_APPLICATION_CREDENTIALS```__ - указывается путь к файлу JSON, который содержит ключ вашего сервисного аккаунта в Google Cloud;
- __```GOOGLE_CREDENTIALS```__ - содержимое файла JSON c ключами  сервисного аккаунта в Google Cloud.

![Heroku env vars](https://raw.githubusercontent.com/igorzakhar/customer-support-chatbot/master/media/heroku_env_vars.png)

#### Развёртывание бота на сервере Heroku

Репозиторий с кодом должен содержать файл ```Procfile``` со следующим содержимым:  
```
vk-bot: python3 vk_chatbot.py
tg-bot: python3 tg_chatbot.py
```

На вкладке **Resources** панели инструментов платформы Heroku переключаем "тумблер" в положение "ON" как показано на скриншоте:  
![Heroku resourses](https://raw.githubusercontent.com/igorzakhar/customer-support-chatbot/master/media/heroku_resources.png)

Далее переходим на вкладку **Deploy** и в разделе **Manual deploy** нажимаем кнопку **Deploy Branch**, если всё прошло нормально то загорятся зелёные галочки справа, как на скриншоте.:
![Heroku deploy](https://raw.githubusercontent.com/igorzakhar/customer-support-chatbot/master/media/heroku_deploy.png)

#### Логи Heroku

Обычно, если код не работает, ошибка выводится в консоль. Но код запускал Heroku, и он просто так её не покажет. Вывод программы можно посмотреть через специальное приложение [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), которое придётся поставить на свой компьютер. Посмотреть логи можно командой: 

```bash
$ heroku logs --tail --app your_app_name
```

![Heroku logs](https://raw.githubusercontent.com/igorzakhar/customer-support-chatbot/master/media/heroku_logs.png)

Если вы не можете сразу увидеть источник ошибки, попробуйте перезапустить приложение из другого окна терминала.

```bash
$ heroku restart
```

# Цели проекта

Код написан в образовательных целях.