# 📝 Blog API – Django REST Framework

A full-featured blog API built with Django REST Framework, JWT authentication, PostgreSQL, Docker, and deployed on AWS EC2. The project supports user registration/login, CRUD operations for blog posts with media uploads, permission controls, and more.

---

## 🚀 Features

- User registration & JWT authentication (`djangorestframework-simplejwt`)
- Custom user model
- Full CRUD API for blog posts
- Custom permissions (Author-only edit/delete)
- Pagination for posts
- API documentation with Swagger & ReDoc (`drf-spectacular`)
- Media file uploads to AWS S3
- Dockerized app with PostgreSQL
- Deployment on AWS EC2
- Environment variable support via `.env`

---

## 🔧 Project Setup

### 1. Virtual Environment & Dependencies
```bash
python -m venv .venv
source .venv/Scripts/activate 
pip install -r requirements.txt
```

## 🛠️ Django Project Structure

```bash
django-admin startproject blogapi
python manage.py startapp accounts   # For custom user
python manage.py startapp blog       # For blog logic
```

## Models
### Custom User
A custom user model using email as the primary identifier for authentication instead of username. This allows flexibility for future extensions (e.g., adding profiles).

### Post Model
`title`: string

`content`: text

`image`: image field

`created_at`, `updated_at`: datetime fields

`author`: ForeignKey to user

Tests are written for all models.

## API Overview
### Authentication
#### Register

#### **Register**
- **POST** `/api/register/`  
  **Request**:  
  ```json
  {
    "email": "string",
    "username": "string",
    "password": "string"
  }
POST /api/register/
Request: { email: string, username: string, password: string }
Response: { id: int, email: string, username: string }

Login (Token Pair)
POST /api/token/
Request: { email: string, password: string }
Response: { access: string, refresh: string }

Token Refresh
POST /api/token/refresh/
Request: { refresh: string }
Response: { access: string }

📝 Blog Posts
List All Posts
GET /api/posts/
Query: ?page=int
Response: { count, next, previous, results: [ { id, title, content, image, author, created_at } ] }

Create Post (Authenticated)
POST /api/posts/
Request: { title: string, content: string, image: string }
Response: Full post object

Retrieve Post
GET /api/posts/{id}/
Response: Full post object

Update Post (Author Only)
PUT /api/posts/{id}/
Request: Full post body
Response: Updated post

Partial Update Post (Author Only)
PATCH /api/posts/{id}/
Request: Partial post fields
Response: Updated post

Delete Post (Author Only)
DELETE /api/posts/{id}/
Response: 204 No Content


