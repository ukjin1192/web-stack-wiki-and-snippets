#### Basic settings

~~~~
$ apt-get install gettext
$ vi {PROJECT PATH}/{PROJECT NAME}/settings.py

  ...
  LANGUAGE_CODE = 'ko'
  ugettext = lambda s: s
  LANGUAGES = (
    ('ko', ugettext('Korean')),
    ('en', ugettext('English')),
  )
  LOCALE_PATHS = (
    ROOT_DIR + '/locale/',     # /var/www/mysite.com/locale
  )
  USE_I18N = True
  USE_L10N = True
  ...
  MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
  )
  # TEMPLATE_CONTEXT_PROCESSORS have django.core.context_processors.i18n as default
~~~~

#### Internationalization in template code

~~~~
$ vi {PROJECT PATH}/{PROJECT NAME}/templates/test.html

  {% load i18n %}
  ...
  {% trans "Hello" %}
  ...
  
$ cd {PROJECT PATH}
$ django-admin.py makemessages -l {LOCALE NAME}
~~~~


#### Internationalization in javascript code

~~~~
$ vi {PROJECT PATH}/{PROJECT NAME}/urls.py

  from django.views.i18n import javascript_catalog

  js_info_dict = {
    'packages': ('your.app.package',),
  }

  urlpatterns = [
    url(r'^jsi18n/$', javascript_catalog, js_info_dict),
  ]

$ vi {PROJECT PATH}/{PROJECT NAME}/templates/test.html

  <script type="text/javascript" src="{% url 'django.views.i18n.javascript_catalog' %}">
    document.write(gettext('Hello'));
  </script>

$ cd {PROJECT PATH}
$ django-admin.py makemessages -d djangojs -l {LOCALE NAME}
~~~~


#### Localization

~~~~
$ vi {PROJECT PATH}/locale/{LOCALE NAME}/LC_MESSAGES/django.po

  msgid "Hello"
  msgstr "안녕"

$ cd {PROJECT PATH}
$ django-admin.py compilemessages
~~~~
