# Passbolt Connector — Connector Discovery

**Official Documentation:** https://passbolt.com  
**Base URL:** https://<passbolt-domain>/api  
**Auth Model:** GPG Auth / User Private Key + Passphrase  

## Основные сущности вендора
- ресурсы/секреты (/resources), папки (/folders), пользователи (/users), группы прав (/groups), журналы аудита

## Лимиты и особенности API
- Соблюдение Rate Limits вендора, обработка HTTP 429 с экспоненциальным backoff.
- Валидация входных данных по Pydantic-схемам вендора до отправки запроса.
- Тестовая точка проверки подключения: `GET /auth/verify.json`.
