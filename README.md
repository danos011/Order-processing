# Мини-система обработки заказов с использованием брокера сообщений Apache Kafka

## Цель проекта

Разработать прототип системы микросервисов для обработки заказов в интернет-магазине с целью тестирования
функциональности брокера сообщений Apache Kafka в асинхронной архитектуре.

## Технологический стек

- Брокер сообщений: Apache Kafka (версия 3.x)
- Язык программирования: Python с библиотекой confluent-kafka
- Фреймворк API: FastAPI, uvicorn
- Логирование: стандартный Python logging и ELK
- Среда выполнения: Docker

## Описание микросервисов

1. **Order Service**  
   Принимает заказы через REST API и публикует сообщения в Kafka topic `orders`.

2. **Processing Service**  
   Подписывается на топик `orders`, обрабатывает заказы (проверка и подтверждение), публикует результат в
   топик `notifications`.

3. **Notification Service**  
   Подписывается на топик `notifications`, выводит результат обработки заказа в консоль или лог.

## Поток данных

- Пользователь отправляет заказ в формате JSON:

```
{ “order_id”: “12345”, “user_id”: “user789”, “item”: “laptop”, “quantity”: 2 }
```

- Order Service публикует заказ в топик `orders`
- Processing Service обрабатывает заказ и публикует результат (`order_id`, `status`) в топик `notifications`
- Notification Service выводит результат в лог


## Запуск контейнеров

- **Продакшен-окружение:**

1. **Билд контейнера:**

```
./entrypoint.sh --build
```

2. **Остановка контейнера:**

```
./entrypoint.sh --down
```

3. **Показать логи:**

```
./entrypoint.sh --down
```

---

## Работа с девовским окружением

1. **Настройка `.env` файлов для каждого сервиса:**

- **notification_service**
  ```
  KAFKA_BOOTSTRAP_SERVERS=localhost:9092
  KAFKA_GROUP_ID=notification-group
  KAFKA_AUTO_OFFSET_RESET=earliest
  ```

- **order_service**
  ```
  KAFKA_BOOTSTRAP_SERVERS=localhost:9092
  ```

- **processing_service**
  ```
  KAFKA_BOOTSTRAP_SERVERS=localhost:9092
  KAFKA_GROUP_ID=notification-group
  KAFKA_AUTO_OFFSET_RESET=earliest
  ```

Создайте файл `.env` в каждой директории соответствующего сервиса и вставьте содержимое в него.

2. **Создание виртуального окружения и установка зависимостей:**

- В корне проекта выполните:

  ```
  python3 -m venv venv
  source venv/bin/activate
  ```

- Установите зависимости для всех сервисов сразу (если requirements.txt общий):

  ```
  pip install -r requirements.txt
  ```

- Если в каждом сервисе свой requirements.txt, установите зависимости для каждого сервиса, находясь в корне venv:

  ```
  pip install -r notification_service/requirements.txt
  pip install -r order_service/requirements.txt
  pip install -r processing_service/requirements.txt
  ```

3. **Запуск сервисов в отдельных терминалах:**

- В каждом новом терминале активируйте venv:

  ```
  source venv/bin/activate
  ```

- Затем запустите каждый сервис:

    - **notification_service**
      ```
      cd notification_service
      python3 main.py
      ```

    - **order_service**
      ```
      cd order_service
      uvicorn main:app --reload --port 8001
      ```

    - **processing_service**
      ```
      cd processing_service
      python3 main.py
      ```

---

## Создание топиков в Kafka

Для работы всех сервисов предварительно создайте необходимые топики в Kafka. После запуска контейнеров с брокером
сообщений выполните следующие команды:

1. **Зайдите в контейнер с Kafka:**

```
docker exec -it kafka1 bash
```

2. **Создайте топики:**

- *orders*
  ```
  kafka-topics --create --topic orders --partitions 1 --replication-factor 1 --if-not-exists --bootstrap-server localhost:9092
  ```

- *notifications*
  ```
  kafka-topics --create --topic notifications --partitions 1 --replication-factor 1 --if-not-exists --bootstrap-server localhost:9092
  ```

- (Добавьте другие топики по аналогии, если нужно.)

3. **Проверьте, что топики созданы:**

```
kafka-topics –list –bootstrap-server localhost:9092
```

**Примечания:**

- Просмотр логов в Kibana: http://localhost:5601/
- Убедитесь, что все переменные окружения прописаны в `.env` для корректной работы сервисов.
- Для работы Kafka убедитесь, что брокер сообщений доступен по адресу, указанному в переменных.
- Запуск каждого сервиса требует отдельного терминала с активированным venv.
