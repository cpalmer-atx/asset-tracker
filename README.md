# Python RESTful asset tracker
## Created by: Chad Palmer

### About this repo:
This web application project (in development) serves to track and display assets to a central dashboard for team visibility.  Specifics of the project will be documented here as it evolves. 

### Native environment:
All code has been written and tested in Ubuntu 20.04 and macOS Catalina V 10.15.6.  Any similar Linux distro based on Ubuntu should have no issues with this project.

### Setting things up:

Using PIPENV virtual environment with the following dependencies:
1. `$ pipenv install Flask`
2. `$ pipenv install Flask-RESTful`
3. `$ pipenv install Flask-JWT`
4. `$ pipenv install Flask-SQLAlchemy`

Once virtual environment is initialized and set up with our dependancies, remember to launch the environment to ensure global packages aren't changed:

`$ pipenv shell`

### Having issues?
If using VSCode text editor (or launching the app from any editor for that matter), ensure that the correct Python interpreter is selected for your virtual environment or required packages installed during setup will not be found.