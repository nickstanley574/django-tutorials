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
