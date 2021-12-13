# What is Flask auth?

It is a flask application that allows you to log and record user sessions in a SQLite database. This project was created to serve as an example of the handling of flask and its extensions for the creation, administration and handling of templates, forms and validation of their fields, databases and their migrations and login.

![functioning](https://github.com/Angel-Gabriel-Chavez/flask-auth/blob/main/app/static/images/res/functioning.gif)

# Installation Guide
## Pre-requirements
In this project I will use `SQLite` as a database administrator and it is recommended to use `virtualenv` to avoid conflicts with other projects.

## How to start?
Clone the repository.
```
$ git clone https://github.com/Angel-Gabriel-Chavez/flask-auth.git
```
Create the virtual environment, and activate it.
```
> cd flask-auth
C:\project\root> python -m venv venv
C:\project\root> venv\Scripts\activate
```

## Install dependencies
```
(venv) C:\project\root> pip install -r requirements.txt
```

## Run 
```
(venv) C:\project\root> python main.py
```
Visit `https://127.0.0.1:5000` to see the project in operation
# License
- MIT
