# Blog API – Django REST Framework

A full-featured blog API built with Django REST Framework, JWT authentication, PostgreSQL, Docker, and deployed on AWS EC2. The project supports user registration/login, CRUD operations for blog posts with media uploads, permission controls, and more.

---

## Features

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

## Project Setup

### 1. Virtual Environment & Dependencies
```bash
python -m venv .venv
source .venv/Scripts/activate 
pip install -r requirements.txt
```

### 2. Django Project Structure

```bash
django-admin startproject blogapi
python manage.py startapp accounts   # For custom user
python manage.py startapp blog       # For blog logics
python manage.py runserver           # Starting the Django development server
```

## Models
### Custom User Model
- Extends Django's AbstractUser
- Uses email as primary identifier
- Ready for future customization

### Post Model
#### Fields
`title`: string; 
`content`: text; 
`image`: image field; 
`created_at`, `updated_at`: datetime fields; 
`author`: ForeignKey to user

Tests are written for all models.

## Database
- PostgreSQL
- Initially on Local machine with **pgAdmin 4**
- (Later on PostgreSQL when Dockerization)

Run migrations -
  `python manage.py migrate`

## API Overview

### Authentication


| Endpoint              | Method | Description         | Request                                              | Response                                         |
|-----------------------|--------|---------------------|------------------------------------------------------|--------------------------------------------------|
| `/api/register/`      | POST   | Register new user   | `{ email: string, username: string, password: string }` | `{ id: int, email: string, username: string }`     |
| `/api/token/`         | POST   | Get JWT token pair  | `{ email: string, password: string }`               | `{ access: string, refresh: string }`            |
| `/api/token/refresh/` | POST   | Refresh access token| `{ refresh: string }`                               | `{ access: string }`                             |


### Blog Posts

| Endpoint              | Method | Description              | Permission   | Request                                          | Response                                                                 |
|-----------------------|--------|--------------------------|--------------|--------------------------------------------------|--------------------------------------------------------------------------|
| `/api/posts/`         | GET    | List all posts (paginated) | Any        | Query: `?page=int`                               | `{ count, next, previous, results: [ { id, title, content, image, author, created_at } ] }` |
| `/api/posts/`         | POST   | Create new post          | Authenticated| `{ title: string, content: string, image: string }` | Full post object                                                        |
| `/api/posts/{id}/`    | GET    | Retrieve post            | Any          | –                                                | Full post object                                                        |
| `/api/posts/{id}/`    | PUT    | Update post              | Author only  | Full post body                                   | Updated post                                                             |
| `/api/posts/{id}/`    | PATCH  | Partial update           | Author only  | Partial post fields                              | Updated post                                                             |
| `/api/posts/{id}/`    | DELETE | Delete post              | Author only  | –                                                | `204 No Content`                                                         |


## Permissions:
- **Global**: `IsAuthenticatedOrReadOnly`

- **Object-level**: `IsAuthorOrReadOnly` (custom)


## API Documentation
Documenting the APIs with `drf-spectacular`.
Available at:
-  Swagger-UI: [`/api/docs/`](https://blogging-restful-api-project-with-drf.onrender.com/api/docs/)
-  Redoc-UI [`/api/redoc/`](https://blogging-restful-api-project-with-drf.onrender.com/api/redoc/)

## Static & Media Files with AWS S3
- Uploaded blog post images are stored in an S3 bucket.
- Configured with boto3 and IAM credentials.
- `collectstatic` uploads static files to S3.
- Public access enabled via S3 bucket policy.

## Environment Variables (.env)
All sensitive values are managed through `.env` for:
- Database configuration
- Django secret key
- AWS credentials
- Allowed hosts

## Dockerization
#### Docker & Compose Setup
- created `start.sh` for entrypoint commands for `migrate`, `createsuperuser`, `collectstatic` and starting `gunicorn`
- created Dockerfile
- Dockerfile built and pushed to DockerHub
  - `docker build -t blogapi .`
  - `docker tag blogapi sdelowar2/blogapi:latest`
  - `docker login`
  - `docker push sdelowar2/blogapi:latest`
- docker-compose.yml includes:
  - Django app
  - PostgreSQL image
- Run the images with:
  `docker-compose --env-file .env up -d`

## AWS EC2 Deployment
#### Steps:
1. Provision EC2 & open port 8000

2. Configure EC2 instance for deployment
    - Update packages
      - `sudo apt-get update`
      - `sudo apt-get upgrade -y`
    - Install Docker
      - `curl -fsSL https://get.docker.com -o get-docker.sh`
      - `sudo sh get-docker.sh`
      - `sudo usermod -aG docker ubuntu`
      - `newgrp docker`
    - Install Docker Compose
      - `sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
      - `sudo chmod +x /usr/local/bin/docker-compose`
    - Install AWS CLI
      - `curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"`
      - `sudo apt install -y unzip`
      - `unzip awscliv2.zip`
      - `sudo ./aws/install`
    - Configure using IAM credentials
      - `aws configure` (Giving the Acces Key and Secret Access Key of IAM user, Region)

3. Transfer project files (`.env` and 'docker-compose.yml`) to EC2:
     - `scp -i path/to/key.pem .env docker-compose.yml ubuntu@ec2-ip:/home/ubuntu/`
4. Run Docker Compose on EC2:
     - `docker-compose --env-file .env up -d`
  
## Test with Postman
All API endpoints were tested using **Postman** against the deployed EC2 URL. All features and permissions worked as expected.
Small Recorded Video on Testing the APIs on Postman:
[![Watch the video](https://img.shields.io/badge/Watch%20Video-Click%20Here-brightgreen)](https://drive.google.com/file/d/19gScsng5NIkq9iR8ifAZepZOfnZX6A8p/view?usp=sharing)
