# Тестирование переключения языков

## Проверка настроек

1. Убедитесь, что сервер Django запущен:
   ```bash
   python manage.py runserver
   ```

2. Откройте браузер и перейдите на сайт

3. Попробуйте нажать кнопки переключения языков (Հայ / Рус / Eng)

## Если языки не переключаются:

### Вариант 1: Установить gettext и скомпилировать переводы

**Windows:**
1. Скачайте gettext: https://mlocati.github.io/articles/gettext-iconv-windows.html
2. Распакуйте и добавьте в PATH
3. Выполните: `python manage.py compilemessages`

**Linux:**
```bash
sudo apt-get install gettext
python manage.py compilemessages
```

**macOS:**
```bash
brew install gettext
python manage.py compilemessages
```

### Вариант 2: Использовать альтернативный метод

Если gettext недоступен, Django может работать с .po файлами напрямую в режиме разработки (медленнее, но работает).

### Проверка:

1. Откройте консоль браузера (F12)
2. Проверьте, отправляется ли POST запрос при нажатии на кнопку языка
3. Проверьте cookies - должен быть установлен `django_language`
4. Проверьте Network tab - должен быть запрос к `/i18n/setlang/`

## Отладка

Если проблемы продолжаются, проверьте:

1. **Middleware порядок**: `LocaleMiddleware` должен быть после `SessionMiddleware`
2. **URL правильный**: `/i18n/setlang/` должен быть доступен
3. **CSRF токен**: форма должна содержать `{% csrf_token %}`
4. **Переводы**: файлы `.po` должны быть в `voske_dzerq/locale/[lang]/LC_MESSAGES/`

## Быстрое решение

Если ничего не помогает, попробуйте:

1. Очистить cookies браузера
2. Перезапустить сервер Django
3. Проверить, что `USE_I18N = True` в settings.py
4. Убедиться, что `LocaleMiddleware` в MIDDLEWARE

