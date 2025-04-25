# Flask App

This is a simple Flask app that serves as a starting point for building web applications using the Flask framework.
It includes a basic structure with a few example routes and templates.

## Installation

```bash
py -3 -m venv .venv
```

```bash
pip install Flask py2neo
```

## Usage

Activate the virtual environment and run the Flask app.

1. Launch venv

```bash
.venv\Scripts\activate
```

2. Launch the app

```bash
flask --app app run
```

2. (optional) launch the app in debug mode

```bash
flask --app app run --debug
```

3. Launch neo4j in docker

```bash
docker run --name neo4j -d -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j
```

Api url :

```bash
localhost:5000/api
```

# Example Postman tests

## Get all users

```bash
GET http://localhost:5000/users
```

## Create a new user

```bash
POST http://localhost:5000/users
```

body :

```bash
{
    "name": "Person",
    "email": "test@mail.com"
}
```

## Create a new post

```bash
POST http://localhost:5000/posts/by-user/{userId}
```

body :

```bash
{
    "title": "Post title",
    "content": "Post content"
}
```

## Create a new comment

```bash
POST http://localhost:5000/posts/{postId}/comments
```

body :

```bash
{
    "user_id": {userId},
    "content": "Comment content"
}
```
