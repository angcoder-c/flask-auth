# How Blueprints are used in Flask❔
Hello netizen, you are probably reading this because you found a repository about flask on GitHub, let me explain what it is. This is a tutorial where I will show you how to make a simple application with blueprints in flask.

## Requirements
- Have python 3 installed.
- For this tutorial i assume you use Windows

## How to start❔
To start we must create a directory on our computer, this will be the one that will contain everything that concerns the project. After accessing this directory through the command line we must install `virtualenv` to work in an empty environment.

***Console***

```
C:\root\directory\project> python -m pip install virtualenv
```

Following this we must create and activate a new virtual environment in the directory of our project.

***Console***

```
C:\root\directory\project> python -m venv venv
C:\root\directory\project> venv\Scripts\activate
```

This will activate the virtual environment. `(venv) C:\root\directory\project>`.

What follows is to install flask in the virtual environment, it is done as follows:

```
(venv) C:\root\directory\project> pip install flask
```

If there was no problem, we are ready to start with the project structure.

## Initial structure of the application
The basic structure of a flask application would look like the following:

```
project
├─venv
└─main.py
```

Within `main.py` you can create an instance of Flask that in turn allows you to create your own urls for the application, as follows:

***main.py***

```
from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
    return 'Index'
```

To see the result we must use the following commands in the console: 

***Console***

```
set FLASK_APP=main.py
set FLASK_DEBUG=1
flask run
```

This will start the application and if we enter `http://127.0.0.1:5000`, we can see a page with the text `'Index'`.

## A Better structure
The above structure can be quite useful but not the most elegant. An alternative is to divide our urls is groups according to their usefulness, making use of blueprints, for example:

```
project
├─app
│ └─___init__.py
│ ├─public
│ │ └─__init__.py
├─venv
└─main.py
```

In the new structure, an **app** directory has been created that will contain everything related to the application, while **main.py** will only fulfill the task of executing it.

It's time to create our first blueprint.

## Blueprints 
Let's create the same view as before, but this time with the new structure. Within the **app** directory we create another one called **public**,in this we will define all the public views as the previous view.

***app/public/__init__.py***

```
from flask import Blueprint 
bp_public = Blueprint('public', __name__) # creando el primer bleprint

@bp_public.route('/') # index view
def index():
    return 'Index'
```

To give a little more order to the file structure, we can create a new file that contains the views within the ***public*** directory, in my case I will call it ***routes.py***.

```
project
├─app
│ └─___init__.py
│ ├─public
│ │ ├─__init__.py
│ │ └─routes-py
├─venv
└─main.py
```

***app/public/routes.py***

```
from . import bp_public # import blueprint

@bp_public.route('/') # index view
def index():
    return 'Index'
```

Doing this would leave our app/prublic/init file .py as follows:

***app/prublic/__init__.py***

```
from flask import Blueprint 
bp_public = Blueprint('public', __name__) # creating the first bleprint

from . import routes
```

> Within the file `__init__.py` we must define a function that will contain the flask instance, register the blueprints, and where a configuration secret key necessary for flask is defined.
[Flask documentation](https://flask.palletsprojects.com/en/2.0.x/tutorial/templates/)

***app/__init__.py***

```
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SUPER_SECRET'

    from .public import bp_public # import blueprint
    app.register_blueprint(bp_public)
    
    return app
```

> This reduces `main.py` to two lines of code, where the function `create_app` is imported and the necessary instance is created.

***main.py***

```
from app import create_app
app = create_app()
```

> The execution is done in the same way as before, we use the commands and if we access the same path we should not see any changes.

The new structure will help you a lot to have your views more organized.

## Templates
So far we have only returned text in our view, but in a real application we probably need a more complex html structure. Although we can continue to return text with html tags inside, this would be very confusing, luckily flask allows the use of templates through the Jinja2 library.

> Templates are files that contain static data as well as placeholders for dynamic data. 

Within the ***app*** directory we must create a new file directory called ***templates*** that will contain all the html files that we will show in the application.

```
project
├─app
│ └─___init__.py
│ ├─public
│ │ ├─__init__.py
│ │ └─routes-py
│ ├─templates
│ │ └─index.html
├─venv
└─main.py
```

Once this is done, we must tell the application in which directory the templates are listed.

***app/__init__.py***

```
def create_app():
    app = Flask(__name__,  template_folder='templates') # templates
    app.config['SECRET_KEY'] = 'SUPER_SECRET'
    ...
```

And of course, we have to write something in ***index.html***, for now, it will be simple.

***app/templates/index.html***

```
<h1>Index</h1>
<p>
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.Pellentesque interdum rutrum sodales.Nullam mattis fermentum libero, non volutpat.
</p>
```

We're ready, let's render our first template.

***app/public/routes.py***

```
from . import bp_public
from flask import render_template # render function

@bp_public.route('/')
def index():
    return render_template('index.html') # Template rendering
```

Now dear Netizen, you can already see your template in `http://127.0.0.1:5000`.

## Inheriting templates
Imagine that we have a navigation menu and a footer, it would be tedious to have to write the corresponding code in each of the views you create -imagine that you create a thousand - and even more, imagine wanting to make a change, you should change all the templates. That is why like the files of any programming language jinja2 allows us to inherit from another template.

Let's create another file in the ***templates*** folder called ***base.html***..

```
project
├─app
│ └─___init__.py
│ ├─public
│ │ ├─__init__.py
│ │ └─routes-py
│ ├─templates
│ │ ├─base.html
│ │ └─index.html
├─venv
├─main.py
└─requirements.txt
```

Within the new file, we will create a navigation menu and a footer that will be present in all the public views of the application.

***app/templates/base.html***

```
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>App | {% block title %}{% endblock %}</title>
    </head>
    <body>
        <header>
            <nav>
                <ul>
                    <li><a href="">Home</a></li>
                    <li><a href="">About us</a></li>
                    <li><a href="">Contact</a></li>
                </ul>
            </nav>
        </header>
        <div class="content">
            {% block content %}{% endblock %}
        </div>
        <footer>
            Footer
        </footer>
    </body>
</html>
```

All you have to understand about this html file is that there is a list of links (they do not lead anywhere) that simulates a navigation menu and in the footer there is only one text. The interesting thing is not that, but what is inside that rare structure of keys and percentages:

- `{% block title %}{% endblock %}`
- `{% block content %}{% endblock %}`

This is jinja2 way of introducing new content into a template, by blocks.

If you reload the page you will not see anything different, we must extend ***base.html*** to ***index.html***, and then introduce content in the blocks.

***app/templates/index.html***

```
{% extends 'base.html' %}
{% block title %}
    Index
{% endblock %}
{% block content %}
    <h1>Index</h1>
    <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.Pellentesque interdum rutrum sodales.Nullam mattis fermentum libero, non volutpat.
    </p>
{% endblock %}
```

As you can see, doing it is quite simple and will save you a lot of problems.

## Dynamic content
Well, up to this point you already understood how to render templates in a good application structure with flask, now let's play with urls.

Let's create a view that add two numbers passed by parameter through the url.

Flask has accepted many entries by url, numbers, strings, which are some examples of this. The way to do it is as follows:

- `/<int:n1>`

The parameter will be passed to the function defined for that url.

***app/public/routes.py***

```
...
@bp_public.route('/n1=<int:n1>,n2=<int:n2>')
def suma(n1=1, n2=1):
    res = n1 + n2
    return render_template()
```

At this point we have two problems, we have not written a template for this view and... how could I show the result?

The first problem is easy to solve, you just have to write the template and include it in the ***templates*** directory.

```
project
├─app
│ └─___init__.py
│ ├─public
│ │ ├─__init__.py
│ │ └─routes-py
│ ├─templates
│ │ ├─base.html
│ │ ├─index.html
│ │ └─suma.html
├─venv
└─main.py
```

***app/templates/index.html***

```
{% extends 'base.html' %}
{% block title %}
    Suma
{% endblock %}
{% block content %}
    <h1>El resultado es:<br></h1>
{% endblock %}
```

And now, the second problem. Jinja2 thought about it before us and that's why when rendering a template we can give it context, information from the python code that we can use in the template, it is done like this:

***app/public/routes.py***

```
...
    return render_template(suma.html, res=res) # renderizado con contexto
```

And so it is added in the template:
-  `<h1>El resultado es:<br>{{ res }}</h1>`

Let's do a test, go to the url `http://127.0.0.1:5000/n1=2,n2=2` and you will see the result

It's almost complete, now let's add color.

## Static files
Normally in a web application, you need to add styles, images, etc. That's why it's helpful to have all these files in one directory; The one for linking these types of files in flask is similar to working with templates.

- We must create a directory called ***static*** and within it, a file called ***styles.css***.

```
project
├─app
│ └─___init__.py
│ ├─public
│ │ ├─__init__.py
│ │ └─routes-py
│ ├─templates
│ │ ├─base.html
│ │ ├─index.html
│ │ └─suma.html
│ ├─static
│ │ └─styles.css
├─venv
└─main.py
```

- Let's write is the content of ***styles.css***.

```
body {
    margin: 0;
    background: linear-gradient(145deg, rgba(255,197,116,1) 0%, rgba(214,255,123,1) 100%);
    background-attachment: fixed;
    font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    height: 100vh;
}
.content {
    display: block;
    margin: auto;
    text-align: center;
}

footer{
    position: fixed;
    bottom: 0;
}
```

- We tell the application what the static files directory is called.

```
def create_app():
    app = Flask(__name__,  template_folder='templates', static_folder='static') # static files
    ...
```

- We link the ***styles.css*** file to ***base.html***.

***app/templates/base.html***

```
...
  <head>
    <meta charset="utf-8">
    <title>App | {% block title %}{% endblock %}</title>
     <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
  </head>
...
```

### Congratulations!, you can start making your applications with Flask blueprint