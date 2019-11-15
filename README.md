
## My Note API
The APIs allow users to create an account and save notes online.

## Requirements
- Python 3.7
- pipenv

`Setup guide`: [Link](https://djangoforbeginners.com/initial-setup/)

## App Installation

1. Clone repo:

        $ git clone https://github.com/omedale/django-note.git

2. Change directory to `django-note` 

        $ cd django-note

3. Setup environment

        $ pipenv shell

4. Install application dependencies:

        $ pip install -r requirements.txt
      
5. Database Setup

        $ python manage.py makemigrations notes
        $ python manage.py migrate

6. Create admin user

        $ python manage.py createsuperuser

7. start the server:

          $ python manage.py runserver

visit: `http://127.0.0.1:8000/admin` on your browser and login with the admin user you created above

## Endpoints

> `POST` /api/users/
- Sign up
- Params
```
 username: String
 email: String
 password: String
```

> `POST` /api/users/login/
- Login
- Params
```
 email: String
 password: String
```

> `POST` /api/notes/
- Create Note
- Header
```
Authorization: Bearer <token>
```
- Params
```
 title: String
 body: String
```

> `GET` /api/notes/:id
- Get Note
- Header
```
Authorization: Bearer <token>
```

> `PUT` /api/notes/:id
- Update Note
- Header
```
Authorization: Bearer <token>
```

> `DELETE` /api/notes/:id
- Delete Note
- Header
```
Authorization: Bearer <token>
```