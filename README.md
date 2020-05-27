# Django REST API

This is a Rest API for addding students into courses

## Installation & Run

Option 1: docker-compose

```bash
docker-compose up
```

Option 2: Using python

```bash
pip install -r requirements.txt
```

```bash
python manage.py runserver
```

The API is working in http://localhost:8000

## Tests

This application has been tested for each endpoint reaching the goals of the test. 

To run the tests:
```bash
python manage.py test
```

## Notes

1) It is easily scalable using docker and docker-compose

2) In the code are comments explaining some design decisions

3) You can change the databse easily in mysite/settings.py