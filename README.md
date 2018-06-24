# Django Getting Stated


You have to start somewhere right?

https://docs.djangoproject.com/en/2.0/intro/


## [Writing your first Django app, part 1](https://docs.djangoproject.com/en/2.0/intro/tutorial01/)

* Check version - `$ python -m django --version`
* Creating a Project - `$ django-admin startproject mysite`
* run development server - `$ python manage.py runserver`

Creating the Polls app

The `include()` function allows referencing other URLconfs. Whenever Django encounters include(), it chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing.

The `path()` function is passed four arguments, two required: `route` and `view`, and two optional: `kwargs`, and `name`. At this point, it’s worth reviewing what these arguments are for:
* `route` - a string that contains a URL pattern.
* `view` - When Django finds a matching pattern, it calls the specified view function with an `HttpRequest` object as the first argument and any “captured” values from the route as keyword arguments.
* `kwargs` - Arbitrary keyword arguments can be passed in a dictionary to the target view.
* `name` -  Naming your URL lets you refer to it unambiguously from elsewhere in Django, especially from within templates. This powerful feature allows you to make global changes to the URL patterns of your project while only touching a single file.
