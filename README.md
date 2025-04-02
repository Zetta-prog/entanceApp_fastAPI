# 🔐 Auth FastAPI App  

Простое веб-приложение с системой регистрации и аутентификации, написанное на **FastAPI** с использованием **SQLAlchemy** для работы с базой данных и **JWT** для безопасного хранения сессий.  

Фронтенд адаптивный и работает на любых устройствах.  

## 🛠 Технологии  
- **Backend**: FastAPI  
- **Database**: SQLite (через SQLAlchemy)  
- **Authentication**: JWT 
- **Frontend**: HTML, CSS, JS(адаптивный дизайн)  

## ⚙️ Настройка проекта  

### 1. Создание виртуального окружения  
```bash
python -m venv venv
```  

### 2. Активация виртуального окружения  
**Windows:**  
```bash
venv\Scripts\activate
```  
**Linux/MacOS:**  
```bash
source venv/bin/activate
```  

### 3. Установка зависимостей  
```bash
pip install -r requirements.txt
```  

### 4. Создание файла `.env`  
В корне проекта создайте файл `.env` и добавьте путь к базе данных:  
```env
DB_PATH=sqlite:///app/database/users.db
```  

### 5. Запуск приложения  
Перейдите в папку `app` и запустите `main.py`:  
```bash
cd app
python main.py
```  

После запуска сервер будет доступен по адресу:  
👉 [http://127.0.0.1:4444](http://127.0.0.1:4444)  
