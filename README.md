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

## [Writing your first Django app, part 2](https://docs.djangoproject.com/en/2.0/intro/tutorial02/)

 mysite/settings.p contains `INSTALLED_APPS` settings. That holds the names of all Django applications that are activated in this Django instance.

The migrate command looks at the INSTALLED_APPS setting and creates any necessary database tables according to the database settings in your mysite/settings.py file and the database migrations shipped with the app.

`$python manage.py migrate`

```
$ sqlite3
SQLite version 3.22.0 2018-01-22 18:45:57
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> .open db.sqlite3
Error: unknown command or invalid arguments:  "opedb.sqlite3". Enter ".help" for help
sqlite> .open db.sqlite3
sqlite> .schema
```

Now we’ll define your models – essentially, your database layout, with additional metadata. A model is the single, definitive source of truth about your data. It contains the essential fields and behaviors of the data you’re storing. Django follows the **DRY Principle**. The goal is to define your data model in one place and automatically derive things from it.

`$ python manage.py makemigrations polls` - By running **makemigrations**, you’re telling Django that you’ve made some changes to your models (in this case, you’ve made new ones) and that you’d like the changes to be stored as a migration. Migrations are how Django stores changes to your models (and thus your database schema) - they’re just files on disk. You can read the migration for your new model if you like; it’s the file polls/migrations/0001_initial.py.

`python manage.py sqlmigrate polls 0001` - The sqlmigrate command takes migration names and returns their SQL

`python manage.py migrate` - The migrate command takes all the migrations that haven’t been applied (Django tracks which ones are applied using a special table in your database called django_migrations) and runs them against your database - essentially, synchronizing the changes you made to your models with the schema in the database.


three-step guide to making model changes:
1. Change your models (in `models.py`).
2. Run `python manage.py makemigrations` to create migrations for those changes
3. Run `python manage.py migrate` to apply those changes to the database.

The reason that there are separate commands to make and apply migrations is because you’ll commit migrations to your version control system and ship them with your app;

### Playing with the API

 Invoke the Django Python shell - `$ python manage.py shell`

 We’re using this instead of simply typing “python”, because manage.py sets the DJANGO_SETTINGS_MODULE environment variable, which gives Django the Python import path to your mysite/settings.py file.

The API automatically follows relationships as far as you need. **Use double underscores to separate relationships.** This works as many levels deep as you want; there's no limit. Find all Choices for any question whose pub_date is in this year (reusing the 'current_year' variable we created above).

The migration files for each app live in a “migrations” directory inside of that app, and are designed to be committed to, and distributed as part of, its codebase. You should be making them once on your development machine and then running the same migrations on your colleagues’ machines, your staging machines, and eventually your production machines ([stackoverflow.com](https://stackoverflow.com/questions/28035119/should-i-be-adding-the-django-migration-files-in-the-gitignore-file)).


### Introducing the Django Admin

First we’ll need to create a user who can login to the admin site. Run the following command: `python manage.py createsuperuser`

## Writing your first Django app, part 3

A view is a “type” of Web page in your Django application that generally serves a specific function and has a specific template. Django will choose a view by examining the URL that’s requested (to be precise, the part of the URL after the domain name).Django uses what are known as ‘URLconfs’. A URLconf maps URL patterns to views.

```
views.py

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```

```
urls.py

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
```

When somebody requests a page from your website – say, “/polls/34/”, Django will load the mysite.urls Python module because it’s pointed to by the ROOT_URLCONF setting. It finds the variable named urlpatterns and traverses the patterns in order. After finding the match at 'polls/', it strips off the matching text ("polls/") and sends the remaining text – "34/" – to the ‘polls.urls’ URLconf for further processing. There it matches '<int:question_id>/', resulting in a call to the detail() view like so:
`detail(request=<HttpRequest object>, question_id=34)`

the `question_id=34` part comes from ``<int:question_id>``. **Using angle brackets “captures” part of the URL and sends it as a keyword argument to the view function.** The :question_id> part of the string defines the name that will be used to identify the matched pattern, and the <int: part is a converter that determines what patterns should match this part of the URL path.

Each view is responsible for doing one of two things: returning an HttpResponse object containing the content for the requested page, or raising an exception such as Http404. The rest is up to you. All Django wants is that HttpResponse. Or an exception.

Your project’s **TEMPLATES** setting describes how Django will load and render templates. The default settings file configures a DjangoTemplates backend whose APP_DIRS option is set to True. By convention DjangoTemplates looks for a “templates” subdirectory in each of the INSTALLED_APPS.

**Template namespacing** - Now we might be able to get away with putting our templates directly in polls/templates (rather than creating another polls subdirectory), but it would actually be a bad idea. Django will choose the first template it finds whose name matches, and if you had a template with the same name in a different application, Django would be unable to distinguish between them. We need to be able to point Django at the right one, and the easiest way to ensure this is by namespacing them. That is, by putting those templates inside another directory named for the application itself.

`render()` - It’s a very common idiom to load a template, fill a context and return an HttpResponse object with the result of the rendered template. Django provides a shortcut.The render() function takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument. It returns an HttpResponse object of the given template rendered with the given context.

### Raising a 404 error

`from django.http import Http404`

A shortcut: `get_object_or_404()` - It’s a very common idiom to use get() and raise Http404 if the object doesn’t exist. Django provides a shortcut.  get_object_or_404() function takes a Django model as its first argument and an arbitrary number of keyword arguments, which it passes to the get() function of the model’s manager. It raises Http404 if the object doesn’t exist.

### Use the template system

The template system uses dot-lookup syntax to access variable attributes.  In the example of `{{ question.question_text }}`, first Django does a dictionary lookup on the object question. Failing that, it tries an attribute lookup – which works, in this case. If attribute lookup had failed, it would’ve tried a list-index lookup.

`<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>` - The way this works is by looking up the URL definition as specified in the polls.urls module.

How does one make it so that Django knows which app view to create for a url when using the {% url %} template tag? The answer is to add namespaces to your URLconf. In the polls/urls.py file.`app_name = 'polls'`

## Writing your first Django app, part 4


### Write a simple form

We set the form’s action to `{% url 'polls:vote' question.id %}`, and we set `method="post"`. Using `method="post"` (as opposed to `method="get"`) is very important, because the act of submitting this form will alter data server-side. **Whenever you create a form that alters data server-side, use `method="post"`. This tip isn’t specific to Django; it’s just good Web development practice.**

Since we’re creating a POST form (which can have the effect of modifying data), we need to worry about Cross Site Request Forgeries. Thankfully, you don’t have to worry too hard, because Django comes with a very easy-to-use system for protecting against it. In short, all POST forms that are targeted at internal URLs should use the {% csrf_token %} template tag.

`request.POST` is a dictionary-like object that lets you access submitted data by key name. In this case, `request.POST['choice']` returns the ID of the selected choice, as a string. `request.POST` values are always strings. Note that Django also provides `request.GET` for accessing `GET` data in the same way – but we’re explicitly using `request.POST` in our code, to ensure that data is only altered via a `POST` call.

You should always return an `HttpResponseRedirect` after successfully dealing with `POST` data. This tip isn’t specific to Django; it’s just good Web development practice.

### Use generic views: Less code is better

These views represent a common case of basic Web development: getting data from the database according to a parameter passed in the URL, loading a template and returning the rendered template. Because this is so common, Django provides a shortcut, called the “generic views” system. Generic views abstract common patterns to the point where you don’t even need to write Python code to write an app.

`ListView` and `DetailView`. Respectively, those two views abstract the concepts of “display a list of objects” and “display a detail page for a particular type of object.” The `DetailView` generic view expects the primary key value captured from the URL to be called "pk", so we’ve changed question_id to pk for the generic views.

## Writing your first Django app, part 5

### Introducing automated testing

What’s different in automated tests is that the testing work is done for you by the system. You create a set of tests once, and then as you make changes to your app, you can check that your code still works as you originally intended, without having to perform time consuming manual testing.

* Tests will save you time
* Tests don’t just identify problems, they prevent them
* Tests make your code more attractive: “Code without tests is broken by design.” Jacob Kaplan-Moss
* Tests help teams work together

### Writing our first test

A conventional place for an application’s tests is in the application’s `tests.py` file; the testing system will automatically find tests in any file whose name begins with test.

* `python manage.py test polls` looked for tests in the polls application
* it found a subclass of the `django.test.TestCase` class
* it created a special database for the purpose of testing
* it looked for test methods - ones whose names begin with test
* in `test_was_published_recently_with_future_question` it created a `Question` instance whose `pub_date` field is 30 days in the  future
* … and using the `assertIs()` method, it discovered that its `was_published_recently()` returns `True`, though we wanted it to return `False`

### The Django test client

Django provides a test Client to simulate a user interacting with the code at the view level. We can use it in `tests.py` or even in the shell.

```
>>> from django.test.utils import setup_test_environment
>>> setup_test_environment()
```

`setup_test_environment()` installs a template renderer which will allow us to examine some additional attributes on responses such as `response.context` that otherwise wouldn’t be available. **Note that this method does not setup a test database, so the following will be run against the existing database.**


Sometimes tests will need to be updated. Suppose that we amend our views so that only Questions with Choices are published. In that case, many of our existing tests will fail - telling us exactly which tests need to be amended to bring them up to date, so to that extent tests help look after themselves.

## Writing your first Django app, part 6
Aside from the HTML generated by the server, web applications generally need to serve additional files — such as images, JavaScript, or CSS — necessary to render the complete web page. In Django, we refer to these files as “static files”. For small projects, this isn’t a big deal, because you can just keep the static files somewhere your web server can find it. However, in bigger projects – especially those comprised of multiple apps – dealing with the multiple sets of static files provided by each application starts to get tricky.That’s what `django.contrib.staticfiles` is for: it collects static files from each of your applications (and any other places you specify) into a single location that can easily be served in production.

Django’s `STATICFILES_FINDERS` setting contains a list of finders that know how to discover static files from various sources. One of the defaults is `AppDirectoriesFinder` which looks for a “static” subdirectory in each of the `INSTALLED_APPS`, like the one in polls we just created.Because of how the AppDirectoriesFinder staticfile finder works, you can refer to this static file in Django simply as `polls/style.css`, similar to how you reference the path for templates. **Just like templates, we might be able to get away with putting our static files directly in polls/static (rather than creating another polls subdirectory), but it would actually be a bad idea. Django will choose the first static file it finds whose name matches, and if you had a static file with the same name in a different application, Django would be unable to distinguish between them.**

The `{% static %}` template tag generates the absolute URL of static files.

Of course the `{% static %}` template tag is not available for use in static files like your stylesheet which aren’t generated by Django. You should always use **relative paths** to link your static files between each other, because then you can change `STATIC_URL` (used by the *static* template tag to generate its URLs) without having to modify a bunch of paths in your static files as well.
