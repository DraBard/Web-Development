## Distinctiveness and Complexity
This project is different from other projects, because it is an educational platform.
It serves as a platform for students to study Python. Apart from usually repetetive
funcionalities like creating a user the rest of the functionalities are rather distinctive
from other projects. The users are divided into Student, Tutor and Headmaster. Each of 
them have different permissions for the functionalities of the web app. The Exercises
are different coding tasks that challenge the student. The compilator of Python
is achieved by connecting to compilator of python on docker. This is the main functionality
of the web app which serves as the distinguisher and special functionality. Additionally,
Students have limited access to the web app functionalities. The manipulation of groups,
assignment and removal of students is shaded from them both on the HTML rendering and on
the backend as well.

## Files structure
- Codegym
    - views.py contains the backend functions to handle the logic and responses and request - render the page HTML.
    - urls.py contains the urls to manage the requests. It servers as a bridge between the front-end HTML
                        and the backend views.py.
    - models.py contains the database structure embedded in Django classes. Thanks to it the database can be generated
                        with its special structure and functionalities that Django additionally allows.
    - templates:
        * exercise.html - renders the particular exercise, with access to python console.
        * exercises.html - list of exercises that the student can access and try to solve.
        * groups.html - contains the groups that students are assigned to. Tutors and Headmasters can arrange the groups.
        * index.html - main page.
        * layout.html - layout for rendering in django.
        * login.html - log in view. Allows the user to log in to the web app.
        * register.html - registration view. Allows user to register to the web app.
        * user.html - access to user profile.
- dockerfile - file with instructions to build docker image.
- manage.py - Django generated file that manages the commends that one can use on the framework
- README.md - this file with instructions and description of project.
- requirements.py - file with list of packages for Python
- sql_script.py - automatically generates artificial database records for testing the page.

## How to run
* create environment: 
    * ```pip install -r requirements.txt``` - installs the required Python packages
                                                for this web app to function properly
* create database:
    * ```python manage.py makemigrations ``` - creates blueprint for database
    * ```python manage.py migrate ``` - actually generates the sql database structure
* run web server:
    * ```python manage.py runserver``` - activates the localhost that server as the local web server.
                                            As it is not deployed yet, it is only for local use.
* run docker container that compiles python code:
    * run your docker app - The docker application has to be active on the local computer
                            so that the docker can function properly
    * build the image ```docker build -t codegym .``` - builds the docker image that serves as a blueprint 
                                                        for the generation of containers. This web page is
                                                        configured for one contrainer so far.
    * run the contrain ```docker run -p 5000:5000 codegym``` - runs a container that is now an active environment
                                                            that can handle request and compile python code.

