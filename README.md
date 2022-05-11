# FirstBlog
Simple blog with basic functions on Django and Bootstrap.

### Features
- Post (add, edit, delete);
- Tags;
- Comments;
- User (log in, registration, email confirm, reset password, profile);
- Search;
- Feedback page;
- Admin panel;

## Getting Started
These instructions will get you a copy of the project up and running on your local machine.

### Data base
Create PostgreSQL base and user.

```
Username: firstuser
Password: 'your_password'
Name of base: firstblog
```
### Environment variables
Generate secret key: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
```
SECRET_KEY='1e2x3a4m5l6e7.....'  
```
Choose True or False for debug:
```
DJANGO_DEBUG='True'
```
Enter password of PostgreSQL user:
```
DATABASE_PASSWORD='your_password'
```
If `DEBUG=False` a gmail host is used as an email host, otherwise console EmailBackend is used.

Go to your @gmail.com and go to `Manage your google accaunt` > `Security` > `turn ON '2-step Verification'` >  `add 'App passwords'` > `select the application and device for which you need to create an application password. From the opening list, select 'Other'` > `Generate`
```
MAIN_EMAIL='user@gmail.com'
GMAIL_HOST_PASSWORD='password' 
```

### Installation

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver
```
## Requirements
- Python 3.10
- Django 4.0.2