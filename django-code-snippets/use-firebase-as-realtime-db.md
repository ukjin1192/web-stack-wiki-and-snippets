#### Pre-settings at firebase

- Make new repository at <a href="https://www.firebase.com/" target="_blank">Firebase</a>
- Check `repository URL` and `API secret code`


#### Install firebase

~~~~
pip install firebase
~~~~


#### `settings.py`

~~~~
FIREBASE_USERNAME = '{USERNAME}'
FIREBASE_REPO_URL = '{REPOSITORY URL}'
FIREBASE_API_SECRET = '{API SECRET CODE}'
~~~~


#### `utilities.py`

~~~~
from firebase import firebase

FIREBASE_USERNAME = getattr(settings, 'FIREBASE_USERNAME')
FIREBASE_REPO_URL = getattr(settings, 'FIREBASE_REPO_URL')
FIREBASE_API_SECRET = getattr(settings, 'FIREBASE_API_SECRET')

authentication = firebase.FirebaseAuthentication(FIREBASE_API_SECRET, FIREBASE_USERNAME, True, True)
firebase_obj = firebase.FirebaseApplication(FIREBASE_REPO_URL, authentication)


def update_firebase_database(permalink, key, value):
  """
  Update Firebase DB
  """
  firebase_obj.put(permalink, key, value)

  return None
~~~~


#### `views.py`

~~~~
from utilities import update_firebase_database


update_firebase_database(
  '/fpp/',
  'bar',
  0
)
~~~~
