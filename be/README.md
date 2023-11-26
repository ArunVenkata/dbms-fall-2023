Development Environment
Development Tool: PyCharm 2020.1
Programming Language: Python 3.8.0
Web Framework: Django 3.0.6
Database: MySQL 5.7
Operating System: Windows 10
Project Implementation
1. Create a Project
File -> New Project -> Django


Wait for a moment, and the project directory structure will look like the following:



After project creation, confirm whether Django and mysqlclient interpreters are installed. To confirm, navigate to File -> Settings.



If not installed, run the following commands in the terminal to install:

bash
Copy code
pip install django
pip install mysqlclient
If you encounter a "Read timeout" error during installation, set a longer timeout as follows:

bash
Copy code
pip --default-timeout=180 install -U django
pip --default-timeout=180 install -U mysqlclient
Here, -U is a shorthand for --upgrade, which upgrades the installed packages to the latest versions.

2. Create an Application
Open the PyCharm terminal and run the following command to create the shop application:

bash
Copy code
python manage.py startapp shop
After creating the application, add 'shop' to the INSTALLED_APPS section in the settings.py file of the project.



3. Configure MySQL Database
Create a sms database in your local MySQL, and modify the database connection information in the project's settings.py from the default SQLite to MySQL.



python
Copy code
DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  'sms',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': 3306
     }
}
Test the connection by clicking on "Test Connection" in PyCharm. If successful, the connection details will be displayed, indicating a successful connection to the local MySQL.



4. Create Data Models (M)
In the models.py file under the shop application, add the Student model:



python

bash
Copy code
python manage.py makemigrations shop
python manage.py migrate shop
The generated table structure in the database will look like the following:

