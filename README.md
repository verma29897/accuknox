# accuknox
 Create an API for social networking application using Django Rest Framework with below functionalities.
# Social Networking API

This is a social networking API built using Django Rest Framework (DRF). It provides user authentication, friend request management, and search functionality.

## Features

- **User Authentication**: 
  - Signup with email and password.
  - Login with email and password.
  - Token-based authentication.

- **User Search**:
  - Search for users by email or username.
  - Pagination for search results.

- **Friend Requests**:
  - Send, accept, and reject friend requests.
  - List all friends.
  - List pending friend requests.
  - Limit on sending more than 3 friend requests within a minute.

## Project Structure

## plaintext
social_network/
    ├── accounts/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations/
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── views.py
    ├── social_network/
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    ├── manage.py


git clone https://github.com/yourusername/social-networking-api.git
cd social-networking-api
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver


## Test User Signup

Method: POST
URL: http://127.0.0.1:8000/api/signup/
Body: Choose raw and JSON format.
JSON Payload:
{
  "email": "testuser@example.com",
  "password": "password123"
}
Response
{
  "id": 1,
  "username": "testuser@example.com",
  "email": "testuser@example.com"
}


## Test User Login

Method: POST
URL: http://127.0.0.1:8000/api/login/
Body: Choose raw and JSON format.
JSON Payload:

{
  "email": "testuser@example.com",
  "password": "password123"
}
Response 
{
  "token": "your-auth-token"
}

## Send Friend Request: 
POST /api/friend-request/

Request:
Headers: Authorization: Token your-auth-token
Body:
{
  "to_user": 1
}

Response:

{
  "id": 1,
  "from_user": 1,
  "to_user": 2,
  "is_accepted": false,
  "timestamp": "2024-08-12T12:34:56.789Z"
}

## Accept/Reject Friend Request:
PUT /api/friend-request/<id>/response/


Headers: Authorization: Token your-auth-token
Body:

{
  "action": "accept"  // or "reject"
}
Response:

{
  "status": "Friend request accepted"
}
## List Friends:
GET /api/friends/

Request:
Headers: Authorization: Token your-auth-token
Response:
[
{
"id
    "username": "frienduser",
    "email": "friend@example.com"
  }
]

## List Pending Friend Requests: 
GET /api/friend-requests/pending/

Request:
Headers: Authorization: Token your-auth-token
Response:

[
  {
    "id": 1,
    "from_user": 3,
    "to_user": 1,
    "is_accepted": false,
    "timestamp": "2024-08-12T12:34:56.789Z"
  }
]
