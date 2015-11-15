#### Pre-settings at facebook developers page

- <a href="https://developers.facebook.com/">Facebook Developers</a> > `My Apps` > `Settings` > `Advanced`
- Put `Deauthorize Callback URL` (e.g. `https://mysite.com/facebook/deauthorize/`)


#### `urls.py`

~~~~
urlpatterns += patterns(
  url(
    regex=r'^facebook/deauthorize/$',
    view='deautorize_facebook_logged_in_user'
  ),
)
~~~~


#### `utilities.py`

~~~~
import base64
import hashlib
import hmac
import json

FACEBOOK_SECRET_CODE = getattr(settings, 'FACEBOOK_SECRET_CODE')


def base64_url_decode(raw_url):
  """
  Decode URL by base64
  """
  padding_factor = (4 - len(raw_url) % 4) % 4
  raw_url += "="*padding_factor

  return base64.b64decode(unicode(raw_url).translate(dict(zip(map(ord, u'-_'), u'+/'))))
  
  
def parse_facebook_signed_request(signed_request):
    """
    Parse facebook signed request and recognize user ID
    """
    temp = signed_request.split('.', 2)
    encoded_sig = temp[0]
    payload = temp[1]

    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))

    # Unknown algorithm
    if data.get('algorithm').upper() != 'HMAC-SHA256':
        return None
    else:
        expected_sig = hmac.new(FACEBOOK_SECRET_CODE, msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        return None
    else:
        return data
~~~~


#### `views.py`

~~~~
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from utilities import parse_facebook_signed_request

@csrf_exempt
@require_http_methods(['POST'])
def deauthorize_facebook_logged_in_user(request):
  """
  Deauthorize facebook logged in user
  """
  if not 'signed_request' in request.POST:
    return JsonResponse({
      'state': 'fail',
      'code': 1,
      'message': 'Signed request parameter is required.'
    })
    
  data = parse_facebook_signed_request(request.POST['signed_request'])
  
  if data is None:
    return JsonResponse({
      'state': 'fail',
      'code': 2,
      'message': 'Invalid signed request.'
    })
  
  facebook_user_id = data['user_id']
  
  return JsonResponse({
    'state': 'success',
    'code': 1,
    'message': 'Succeed to get deauthorized facebook user ID.'
  })
~~~~
