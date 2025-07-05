# 📚 DRF Library Project

> A modern backend solution for managing library operations using Django REST Framework.

## 🚀 Overview

The DRF Library Project is an API-driven backend application that digitizes and automates the operations of a traditional library. It replaces outdated manual tracking of books, borrowings, users, and payments with a fully functional web-based system, designed for performance, scalability, and ease of use.

This project was developed as a technical assessment simulation and focuses on clean architecture, authentication, API design, and test coverage.

---

## Features

- JWT Authentication for secure access
- ull CRUD for Books with inventory management
- User registration and profile management
- Borrowing system with return tracking and fee handling
- Swagger/OpenAPI documentation for easy API exploration
- 60%+ test coverage with coverage reporting
- Scalable for up to 50k borrowings/year

---

## Tech Stack

- **Python 3.11+**
- **Django 4.x**
- **Django REST Framework**
- **SimpleJWT** (for JWT-based auth)
- **drf-spectacular** (for API docs)
- **SQLite / PostgreSQL**
- **pytest / coverage** (for tests)

---

## Documentation

Interactive Swagger docs available at:
http://localhost:8000/api/schema/swagger-ui/



## Project Structure

drf_library_project/  
 ┣ books/    
 ┣ users/  
 ┣ borrowings/  
 ┣ Great_Library/  
 ┣ manage.py  
 ┣ .env  
 ┣ equirements.txt  

---

## Installation

```bash
git clone https://github.com/weuis/DRF_Library_Project.git
cd DRF_Library_Project
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate 
```

---

## Star this repo

If you found this project helpful or inspiring, drop a ⭐️ to support it!

