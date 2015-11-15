#### `cron.py`

~~~~
from celery import task

@task()
def sample_async_task(*args, **kwargs):
  return None
~~~~


#### `views.py`

~~~~
from cron import sample_async_task

# Run task asynchronously with celery after 1 second
sample_async_task.apply_async(
  args=[
    'foo_1', 
    'foo_2',
  ], 
  kwargs={
    'foo_3': 'bar',
    'foo_4': 'bar',
  },
  countdown=1
)
~~~~
