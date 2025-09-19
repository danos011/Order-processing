# Реализация системы обработки заказов с использованием брокера сообщений

---

## Запуск контейнеров

- **Продакшен-окружение:**

```
docker compose -f docker-compose-prod.yml up -d –build
```

- **Дев-окружение:**

```
docker compose -f docker-compose-dev.yml up -d –build
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

**Примечания:**
- Убедитесь, что все переменные окружения прописаны в `.env` для корректной работы сервисов.
- Для работы Kafka убедитесь, что брокер сообщений доступен по адресу, указанному в переменных.
- Запуск каждого сервиса требует отдельного терминала с активированным venv.
