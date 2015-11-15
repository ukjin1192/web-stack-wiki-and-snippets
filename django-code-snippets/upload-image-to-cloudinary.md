#### Pre-settings at cloudinary

- Enroll new application
- Check API key and API secret code at <a href="http://cloudinary.com/" target="_blank">Cloudinary</a>


#### Install cloudinary

~~~~
pip install cloudinary
~~~~


#### `settings.py`

~~~~~
CLOUDINARY_API_KEY = '576224373763765'
CLOUDINARY_API_SECRET = 'aiVax8O_I2SfPe7ufT-Uy9GI7r4'
~~~~~


#### `utilities.py`

~~~~
import cloudinary
import cloudinary.uploader

CLOUDINARY_API_KEY = getattr(settings, 'CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = getattr(settings, 'CLOUDINARY_API_SECRET')

cloudinary.config( 
    cloud_name = '{YOUR APP NAME}', 
    api_key = CLOUDINARY_API_KEY, 
    api_secret = CLOUDINARY_API_SECRET 
)


def upload_image_to_cloudinary(image_obj):
  """
  Updload image to Cloudinary and return media url
  """
  # Check file type is image
  if image_obj.content_type.split('/')[0] != 'image':
    return ''

  file_size = image_obj._size
  width, height = get_image_dimensions(image_obj)

  cloudinary_obj = cloudinary.uploader.upload(image_obj, width=width, height=height)

  return cloudinary_obj['secure_url']
~~~~


#### `views.py`

~~~~
from utilities import upload_image_to_cloudinary


if 'image' in request.FILES:
  image_url = upload_image_to_cloudinary(request.FILES['image'])
~~~~
