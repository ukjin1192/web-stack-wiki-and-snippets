#### `utilities.py`

~~~~
from PIL import Image as ImageObj
from PIL import ImageOps
import os
import StringIO
import urllib

def process_image(image_file):
  """"
  Process image file
  """"
  file_extension = image_file.content_type.split('/')[1]
  
  if file_extension is not in ['png', 'jpeg', 'bmp', 'gif']:
    return None
    
  width, height = get_image_dimensions(raw_file)
  
  size = (100, 70)
  thumbnail_image = ImageOps.fit(image_file, size, ImageObj.ANTIALIAS)
  
  return None
~~~~


#### `views.py`

~~~~
from utilities import process_image

for raw_file in request.FILES.getlist('file'):
  process_image(raw_file)
~~~~
