## SPA_web_app

Django-приложение с REST API, PostgreSQL, Redis и Celery. Сервисы запускаются через Docker Compose.
CI/CD реализован через GitHub Actions с автоматическим деплоем на Hetzner.

## Технологии

- Python 3.12, Django 5.2
- Django REST Framework
- PostgreSQL 18
- Redis 8
- Celery и Celery Beat
- Nginx
- Docker и Docker Compose
- Poetry
- GitHub Actions

## Доступ к приложению

- Django Admin: `http://localhost/admin/`
- Swagger API: `http://localhost/api/docs/`
- OpenAPI Schema: `http://localhost/api/schema/`

## CI/CD — GitHub Actions

Workflow **Django CI/CD** запускается при:

- `push` в ветку `homework/docker-compose`;
- `pull_request` в ветку `develop`.

### Этапы CI/CD

1. **Run tests and linting** — установка зависимостей, проверка Black и Flake8, запуск Django-тестов с PostgreSQL и Redis.
2. **Validate Docker build** — проверка конфигурации Docker Compose и сборка Docker-образов.
3. **Deploy to Hetzner** — автоматическое развёртывание приложения на сервере через SSH.

Деплой выполняется после успешного прохождения тестов и сборки при отправке изменений в `homework/docker-compose`.

### GitHub Secrets

Для SSH-подключения используются:

- `SERVER_SSH_KEY`
- `SERVER_HOST`
- `SERVER_PORT`
- `SERVER_USER`

На сервере должен быть установлен Docker, настроен Docker Compose и подготовлен production-файл `.env`.

## Результат

Проект поддерживает запуск всех сервисов одной командой, автоматическое тестирование,
проверку Docker-сборки и автоматическое развёртывание на Hetzner.
