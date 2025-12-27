# Переводы (Translations)

Файлы переводов созданы для трех языков:
- **hy** (Armenian / Հայերեն)
- **ru** (Russian / Русский)
- **en** (English / Английский)

## Компиляция переводов

### Способ 1: Использование polib (рекомендуется, работает без gettext)

Установите polib:
```bash
pip install polib
```

Затем выполните:
```bash
python compile_with_polib.py
```

### Способ 2: Использование gettext (стандартный способ)

Для компиляции .po файлов в .mo файлы выполните:

```bash
python manage.py compilemessages
```

Если у вас не установлен gettext, установите его:

**Windows:**
- Скачайте gettext с https://mlocati.github.io/articles/gettext-iconv-windows.html
- Или используйте: `choco install gettext`

**Linux:**
```bash
sudo apt-get install gettext
```

**macOS:**
```bash
brew install gettext
```

После установки gettext выполните `python manage.py compilemessages` для компиляции переводов.

## Структура файлов

```
locale/
├── hy/
│   └── LC_MESSAGES/
│       └── django.po
├── ru/
│   └── LC_MESSAGES/
│       └── django.po
└── en/
    └── LC_MESSAGES/
        └── django.po
```

После компиляции появятся файлы `django.mo` в каждой директории LC_MESSAGES.

