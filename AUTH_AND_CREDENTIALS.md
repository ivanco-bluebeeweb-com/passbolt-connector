# Passbolt Connector — Auth & Credentials Standard

**Compliance:** AUTH_AND_CREDENTIALS_STANDARD.md (B1–B10)

## Схема аутентификации
- **Метод:** GPG Auth / User Private Key + Passphrase
- **Хранение:** Секреты сохраняются изолированно в хранилище секретов платформы Imperal.
- **Валидация:** При сохранении ключа выполняется тестовый запрос `GET /auth/verify.json`.
- **Отключение:** Удаление локальных ключей без воздействия на аккаунт вендора.
