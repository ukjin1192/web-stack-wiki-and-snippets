#### `settings.py`

~~~~
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '{ADMIN GMAIL ACCOUNT}'
EMAIL_HOST_PASSWORD = '{PASSWORD}'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
~~~~


#### `utilities.py`

~~~~
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template


def send_mail_with_template(subject, template_name, user_from, *user_to, **dict_var):
  """
  Send mail with template
  """
  plaintext = get_template('email/email.txt')
  htmly = get_template(template_name)
  d = Context(dict_var)

  text_content = plaintext.render(d)
  html_content = htmly.render(d)

  msg = EmailMultiAlternatives(
    subject,
    text_content,
    user_from,
    user_to
  )
  msg.attach_alternative(html_content, 'text/html')
  msg.send()

  return None
~~~~


#### `views.py`

~~~~
from utilities import send_mail_with_template


send_mail_with_template(
  'MAIL TITLE',
  'email_content.html',
  '{ADMIN GMAIL ACCOUNT}',
  'user_to_1@domain.com', 'user_to_2@domain.com', ...,
  name='Tim', year=2015
)
~~~~

#### `templates/email.txt`

~~~~
ANY TEXT HERE
~~~~


#### `templates/email_content.html`

~~~~
<div>
  Hello, {{ name }}! 
  You've got mail for year {{ year }}!
</div>
~~~~
