# 🌟 Kondrashov-M Official Website

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Gulp](https://img.shields.io/badge/Gulp-CF4647?logo=gulp&logoColor=white)](https://gulpjs.com/)

Добро пожаловать на официальный сайт Михаила Кондрашова! 🚀 Этот репозиторий содержит открытый исходный код моего персонального портфолио, где вы найдете проекты, резюме и контактную информацию.

## ✨ Особенности

- 🎨 Современный дизайн с темной темой
- 📱 Адаптивная верстка (Bootstrap 5)
- ⚡ Быстрая загрузка без JavaScript-зависимостей
- 🔧 Модульная структура с Gulp-сборкой
- 🎭 Анимации с AOS (Animate On Scroll)
- 🖼️ Галерея проектов с Isotope фильтрацией

## 🛠️ Технологии

- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Frameworks:** Bootstrap 5, Swiper, AOS
- **Build Tools:** Gulp, npm
- **Icons:** Custom SVG sprites
- **Fonts:** Google Fonts (Bebas Neue, Poppins)

## 🚀 Быстрый старт

### 📦 Установка зависимостей

```bash
npm install
```

### 🏗️ Сборка проекта

```bash
npx gulp build
```

Это создаст папку `dist/` с оптимизированными файлами для продакшена.

### 👨‍💻 Разработка

```bash
npx gulp watch
```

Автоматическая пересборка при изменении файлов в `src/`.

### 🌐 Запуск локального сервера

```bash
npx http-server dist/
```

Или используйте любой статический сервер.

## 📁 Структура проекта

```
├── src/                    # Исходные файлы для разработки
│   ├── index.html         # Главная страница с @@include
│   ├── header.html        # Шапка сайта
│   └── footer.html        # Подвал сайта
├── dist/                  # Собранные файлы (после gulp build)
├── css/                   # Стили
├── js/                    # Скрипты
├── images/                # Изображения
├── gulpfile.js            # Конфигурация Gulp
├── package.json           # Зависимости
└── README.md             # Этот файл
```

## 🎯 Скрипты

- `npm run build` - сборка проекта
- `npm run dev` - запуск в режиме разработки
- `npm run serve` - запуск локального сервера

## 📝 Как внести вклад

1. 🍴 Fork репозиторий
2. 🌿 Создайте feature-ветку: `git checkout -b feature/amazing-feature`
3. 💾 Commit изменения: `git commit -m 'Add amazing feature'`
4. 📤 Push в ветку: `git push origin feature/amazing-feature`
5. 🔄 Создайте Pull Request

## 📞 Контакты

- **Telegram:** [@mikondra](https://t.me/mikondra)
- **GitHub:** [kondrashov-m](https://github.com/kondrashov-m)
- **VK:** [kondrashov.mikhail](https://vk.com/kondrashov.mikhail)
- **Email:** [Ваш email]

## � Последние обновления (апрель 2026)

### ✨ Прелоадер
- ✅ Реализован оптимизированный прелоадер с вращающимся спиннером
- ✅ Встроенный JavaScript скрипт для гарантированного закрытия через 2 сек
- ✅ Фиксировано зависание прелоадера (использован встроенный скрипт вместо jQuery)
- ✅ Плавная анимация исчезновения (fade-out)

### 🏗️ Сборка и структура
- ✅ Внедрена Gulp-сборка с `gulp-file-include` для встраивания header/footer
- ✅ Автоматическое включение компонентов при сборке (`@@include()`)
- ✅ Разделение на `src/` для разработки и `dist/` для продакшена
- ✅ Watch-режим для автоматической пересборки

### 🐛 Исправления ошибок
- ✅ Исправлена проблема с анимацией кнопок (двойное закрытие скобок в script.js)
- ✅ Восстановлена функциональность фильтров портфолио (Isotope)
- ✅ Лечение проблем со Swiper слайдером отзывов
- ✅ Нормализация обработчиков jQuery событий

### 📚 Документация
- ✅ Создан современный README.md с badges и подробной информацией
- ✅ Добавлены инструкции по установке и использованию
- ✅ Описана структура проекта и доступные скрипты
- ✅ Добавлены контакты и информация об открытой лицензии

### 💻 Код и оптимизация
- ✅ Переход на чистый JavaScript для критических операций (прелоадер)
- ✅ Оптимизация порядка загрузки скриптов
- ✅ Улучшение производительности для лучшей UX

## �📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).

---

⭐ Если проект вам понравился, поставьте звезду! Ваша поддержка мотивирует на новые фичи.

*Создано с ❤️ Михаилом Кондрашовым*
