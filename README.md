#  CAPSTONE - Ideal Insurances Web APP - FINAL PROJECT CS50W

## DISTINCTIVENESS AND COMPLEXITY
- This is a web application focused on the health insurance industry. Specifically for health insurance agents.This web app allows the creation, update and deletion of contacts, allows you to convert a contact into a customer, updates customer information and also allows its deletion. It has an algorithm for calculating the annual profit depending on the number of clients, the contracted plan or plans, payment made by the plan or plans and the age of the client. 


## PROJECT STRUCTURE
Ideal Insurances Web APP is an app built in Django (including FOUR models: User, PlanSeguro, Contact, Customer). Next, a tree of the project structure is presented:

```
📦FINAL PROJECT 
    ┣ 📦BACK-END (Django)
    ┃    ┣ 📂capstone (App)
    ┃    ┃  ┣  📜models.py ()
    ┃    ┃  ┣  📜admin.py
    ┃    ┃  ┣  📜serializers.py
    ┃    ┃  ┣  📜admin.py
    ┃    ┃  ┣  📜urls.py
    ┃    ┃  ┣  📜....
    ┃    ┣ 📂project_final
    ┃    ┃  ┣  📜settings.py
    ┃    ┃  ┣  📜urls.py
    ┃    ┃  ┣  📜....

```
### Back end
For the Back end in this Web application, Django combined with Django Rest Framework (DRF) was used, achieving a powerful and robust RESTful API’s. Using django-rest-framework (DRF), class serializers are implemented that will automatically serialize fields in JSON and return to Python objects when needed. The Django REST Framework enables complex data, such as query sets and model instances, to be converted to native Python data types that can then be easily represented in JSON.

- In the back end, 4 models were implemented. Below is an extract of the code of a model.

```python
    class Customer(models.Model):
    contacto = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='info_contact')
    planes = models.ManyToManyField(PlanSeguro, blank=True, related_name='customers')
    timecustomer = models.DateTimeField(auto_now_add=True)
    payment = models.FloatField(max_length=10, blank= True, null=True)
    age = models.IntegerField(max_length=3, blank=True, null=True)

    def __str__(self):
        return f"contacto:{self.contacto.name} - payment:{self.payment}"
```
- To create a database from the designed models, you have to navigate to the main directory of the project and execute the command:
```sh
    python manage.py makemigrations capstone
```
Then run the following command to apply migrations to the database:
```sh
    python manage.py migrate
```
In the serializers file serializers.py (./capstone/serializers.py), six serializer classes are created for the different models. Serializers allow you to transform client instances and QuerySets to and from JSON. Below is an extract of the code of a serializer class:

```python
    class GetCustomerSerializer(serializers.ModelSerializer):
    contacto = serializers.CharField(source='contacto.name')
    planes = PlanSeguroSerializer(many=True, read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'contacto', 'planes', 'timecustomer', 'payment', 'age']
```
Eleven methods were implemented in the views.py. The methods handle operations like GET, POST, PUT, DELETE, on the root endpoints of our API. Below is an extract of the code of a method:

```python
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def customer(request, contact_id):
        if request.method == 'GET':
            try:
                contact = Contact.objects.get(id = contact_id)
                customer = Customer.objects.get(contacto = contact_id)
                plans = customer.planes.all()
                serializerplans = PlanSeguroSerializer(plans, context={'request': request}, many= True)
                information = []
                information.append({'name':contact.name, 'phone':contact.phone, 'email':contact.email})
                serializer = GetCustomerSerializer(customer, context={'request': request})
                return Response({'customer':serializer.data, 'information': information, 'plans':serializerplans.data})
            except Contact.DoesNotExist:
                return JsonResponse({"error": "Contact not exist."}, status=404)
            except Customer.DoesNotExist:
                return JsonResponse({"error": "Customer not exist."}, status=404)
```


## EXPLAINING THE PROJECT
This application for health insurance agents has the following functionalities:

### Register and Login
- It allows the registration of new users (entering the username, email and password information). For this web app a user is a health insurance agent.
- Once registered, the user or health insurance agent will enter the web app using their username and password.

For authentication to more of the code in models.py, views.py, urls.py, serializers.py, admin.py in the app called capstone on the back-end it is necessary to add the following configuration to settings.py

```python
    # Specifies localhost port 3000 where the React
    # server will be running is safe to receive requests from.
    CORS_ALLOWED_ORIGINS = [    
    'http://localhost:3000',
    'http://192.168.1.61:3000'
    ]

    # Django All Auth config. Add all of this.
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    AUTHENTICATION_BACKENDS = (    
        "django.contrib.auth.backends.ModelBackend",    
        "allauth.account.auth_backends.AuthenticationBackend",
    )
    SITE_ID = 1 
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_USERNAME_REQUIRED = True
    ACCOUNT_SESSION_REMEMBER = True
    ACCOUNT_AUTHENTICATION_METHOD = 'username'
    ACCOUNT_UNIQUE_EMAIL = True
    # Rest Framework config. Add all of this.
    REST_FRAMEWORK = {    
    'DATETIME_FORMAT': '%d %b %Y, %I:%M %p', 
    'DEFAULT_AUTHENTICATION_CLASSES': [        
        'rest_framework.authentication.TokenAuthentication',
    ],
    }
```
For user registration and login the following packages were used:
 - django-rest-auth
 - django-allauth
 - django-cors-headers
 - django-rest-framework


##  INSTALLED PACKAGES - EXECUTING THIS PROJECT
### Virtual environment
The project will be setup using pipenv.:
```sh
pipenv install --python 3.9.2
```
```sh
pipenv shell
```
### Server side (back-end)
Install all server dependencies like Django, django-rest-framework, django-rest-auth, django-allauth, django-cors-headers.

Framework:
- django: The Django framework is the backbone of the this project final.

Packages for building an API:
- django-rest-framework: To serialize data and turn our Django application into a RESTful API.

Packages for authentication:
- django-rest-auth: Endpoints needed for user authentication.
- django-allauth: Needed for user registration.
- django-cors-headers: To specify domains where requests can be made from.

Package for calculating the cumulative sum of a matrix:
- pandas: Cumulative sum of a column in Pandas can be calculated with the use of a function cumsum().

```sh
pipenv install django djangorestframework django-rest-auth django-allauth django-cors-headers pandas
```
- Create the Django project:
```sh
django-admin startproject project_final .
```
Note the period at the end of the command. This will create the project in the current directory instead of making a whole new one.

- Terminate the development server in terminal and run the following command to create the app:
```sh
python manage.py startapp capstone
```
Instalar para poder usar variables de entorno, ahí es donde guardaremos la información en relación con la conexión a la base de datos:
```sh
pipenv install django-environ
```

Install the following packages to upload to Heroku:
OJO Todos los paquetes se deben instlar en pipenv, sino no funciona en Heroku. Si aprece un error import fcntl en el log de Heroku, instalar en ubuntu (El uso del subsistema de Windows para Linux (WSL) en Windows 10) gunicorn. 
- gunicorn. La librería más importante de todas, me refiero a gunicorn. gunicorn es un servidor HTTP para Unix, sin él, será prácticamente imposible realizar el despliegue.
```sh
pipenv install gunicorn
```
- psycopg2. El gestor de base de datos PostgreSQL.
```sh
pipenv install psycopg2
```
- dj-database-url. Para realizar la conexión entre el proyecto y el gestor de base de datos usaremos la librería dj-database-url, esto principalmente, ya que Heroku nos proveerá de una base de datos que no se encuentra en el mismo servidor.
```sh
pipenv install dj-database-url
```
- python-decouple. Para que podamos iniciar el servidor haremos uso de ciertas variables de entorno.
```sh
pipenv install python-decouple
```
Instalamos WhiteNoise. Django no soporta servir archivos estáticos en producción, así que nos apoyaremos de WhiteNoise.
```sh
pipenv install whitenoise
```

Create requirements.txt file:
```sh
pip freeze > requirements.txt
```

Tip: Una forma en la cual puedes instalar todas las dependencias de un proyecto sin tener que instalar librería por librería, será ejecutando la siguiente sentencia (El archivo requirements.txt ya deberá existir).

```sh
pip install -r requirements.txt
```

### Settings - To work with Heroku
Para que funcione con Heroku:
- En el archivo settings.py
```python
import environ
import os
from decouple import config

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config('SECRET_KEY', default=env('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = config('DJANGO_DEBUG', default=env('DJANGO_DEBUG'), cast=bool)

ALLOWED_HOSTS = ['*']


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    .......
]

CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

# PROJECT_ROOT and STATIC_ROOT to up to HEROKU. Para que funcione el CSS
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

if config('DJANGO_PRODUCTION', default=False, cast=bool):
    from .settings_production import *
```
- En el archivo settings_production.py:
```python
import dj_database_url
from decouple import config

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}
```
- OJO: se debe crear el archivo Procfile:
```sh
echo "web: gunicorn project_final.wsgi" > Procfile
```
En el archivo Procfile también colocar lo siguiente para que las migraciones sean automáticas:
```sh
release: python manage.py makemigrations 
release: python manage.py migrate
```
- Crear un archivo runtime.txt (no es tan necesario ya que Heroku actualmente implementa la última versión de python)

```sh
echo "python-3.9.2" > runtime.txt
```
- Crear el archivo .gitignore. Ahí colocar los arhivos a ignorar.

- Si aparece el error at=error code=H14 desc="No web processes running", ejecutar:
```sh
heroku ps:scale web=1
```
Este error aparece cuando no está instalado en el entorno virtual gunicorn.

### Heroku
- Instalar Heroku
```sh
brew install heroku/brew/heroku
```
- Get the Heroku Command Line Interface. Es lo mismo del comando de instalación de arriba.
```sh
curl https://cli-assets.heroku.com/install.sh | sh
```
- Create a new Git repository for this project.
```sh
git init
```
- Login to Heroku CLI.
```sh
heroku login
```
- Crear nuestra aplicación.
```sh
heroku create <nombre de tu aplicación heroku>
```
- Ligamos el repositorio a nuestra app en heroku.
```sh
heroku git:remote -a <nombre de tu aplicación heroku>
```
- Crear nuestra base de datos en Heroku. Se puede hacer también a través de la página web de Heroku.
```sh
heroku addons:create heroku-postgresql:hobby-dev
```
- En settings de la app en heroku configurar lo siguiente
```sh
DATABASE_URL    Se estableció con la BD
DJANGO_DEBUG    FALSE
DJANGO_PRODUCTION   True
SECRET_KEY      Tupassword
```
- Add your project’s files to Git
```sh
git add .
```
- Commit the files to Git.
```sh
git commit -am "Initialize Django project"
```
- Push the files to the Heroku repository
```sh
git push heroku master
```
- Para chequear si hay errores
```sh
heroku logs --tail
```
- Para crear el super usuario y hacer migraciones. Hacerlo en el terminal de Ubuntu
```sh
heroku run bash
```
```sh
python manage.py migrate
python manage.py createsuperuser
```

### Executing this project
Then, start the server (local)
```sh
python manage.py runserver
```

## About CS50 Web
CS50 Web dive more deeply into the design and implementation of web apps with Python, JavaScript, and SQL using frameworks like Django, React, and Bootstrap. Topics include database design, scalability, security, and user experience. Taught by Brian Yu, a Senior Preceptor at Harvard Division of Continuing Education, you can learn tools, languages, skills and principles to design and deploy applications on the internet.

[CS50 Web](https://cs50.harvard.edu/web/2020/)