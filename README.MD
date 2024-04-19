# Custom Expiring Access Tokens with Django and Django Rest Framework

This repository contains a proof of concept implementation for generating custom expiring access tokens using Django and Django Rest Framework.

## Overview

In many web applications, it's crucial to manage user authentication and access securely. Traditional access tokens might not suffice for scenarios where you need tighter control over the lifespan of access tokens. This proof of concept demonstrates how to implement custom expiring access tokens using Django and Django Rest Framework.

## Features

- **Custom Expiring Tokens**: Instead of using traditional tokens, this implementation generates custom expiring tokens.
- **Token Expiry Management**: Tokens have a predetermined expiration time, enhancing security and reducing the risk of unauthorized access.
- **Django Rest Framework Integration**: The proof of concept leverages Django Rest Framework for API development, making it easy to implement token-based authentication.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
Special thanks to the Django and Django Rest Framework communities for their excellent documentation and resources.

## Testing this project

### Create a new environment for the project (all fixtures will be loaded post migrate)
```shell
python3.x -m venv venv
source ./venv/bin/activate
pip install --upgrade pip
pip install --upgrade setuptools
pip install --upgrade wheel
pip install -r requirements.txt
```

### Make migrations, migrate and create a new superuser:

```shell
./manage.py makemigrations
```
```shell
./manage.py migrate
```
```shell
./manage.py createsuperuser
```

### Run the application then login

```shell
./manage.py runserver
```

### Use cURL, Postman or python-requests to test the API
