# Начало работы

Для подгрузки всех библиотек необходимо прописать команду `npm install` находять в корневой папаке `ui-checkhomework`

После чего можно выполнить команду `npm start` для запуска приложения

## Структура приложения

```
ui_checkhomework/
├── node_modules/
├── public/
│   ├── favicon.ico
│   ├── index.html
│   └── robots.txt
├── src/
│   ├── elements/
│   │   ├── cardCheckInfo/
│   │   │   └── CardCheckInfo.jsx
│   │   └── cardImage/
│   │       └── CardImage.jsx
│   ├── pages/
│   │   ├── checkSolutionPage/
│   │   │   └── CheckSolutionPage.jsx
│   │   ├── correctAndRecognizedSolutionPage/
│   │   │   └── CorrectAndRecognizedSolutionPa...
│   │   └── mainPage/
│   │       └── MainPage.jsx
│   ├── App.css
│   ├── App.js
│   ├── index.css
│   └── index.js
├── .gitignore
├── package-lock.json
└── package.json
```

`ui_checkhomework` - корневая папка

`node_modules` - папка с библиотеками

 - `.gitignore` - внутри прописываются файлы, которые не следует заливать на гит

 - `package.json`/`package-lock.json` - хранят зависимости

`public` - хранит базовую html страницу, иконку и шрифт

`src` - основная директория разработки

 - `index.css`/`App.css` - файлы стилей

 - `index.js` - базовая страница для связи html и react

 - `App.js` - роутер, позволяющий удобно перемещаться между страницами

`src/pages` - директория с элементами-старницами

 - `CardCheckInfo` - карточка с данными по проверке

 - `CardImage` - карточка с изображением внутри, с возможностью масштабировать изображение

`src/elements` - директория с элемнетами, которые будут отображаться внутри элемнетов-страниц

 - `CheckSolutionPage` - Страница проверки с изображением и карточкой с данными

 - `CorrectAndRecognizedSolutionPage` - Страница с двуми изображениями: верным решением и распознанным

 - `MainPage` - Главная страница, когда-нибудь на ней что-нибудь будет

