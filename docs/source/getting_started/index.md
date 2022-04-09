# Getting Started

Django Chunky Upload is designed to be super easy to setup.

## Installation

```sh
pip install django-chunky-upload
```

## Basic Setup

Inside your Django settings update your installed apps to include chunky_upload.

```python
installed_apps = [
    ...,
    chunky_upload
]
```

Update your urls.py file to include the chunky_upload app's urls.

```python
urlpatterns = [
    ...,
    include("chunky_upload.urls")
]
```

## Optional Configuration

As part of the chunky_upload app we provide a custom signal that allow you to receive notification when an upload has been completed. You can utilize this hook in the rest of your application to perform actions upon completion of the upload.

```python
# receiver.py
# An example function of what to do when an upload is complete
from chunky_upload.signals import chunky_upload_complete
from chunky_upload.models import ChunkedUpload
from django.dispatch import receiver

@receiver(chunky_upload_complete, sender=ChunkedUpload, dispatch_uid="handling_upload_complete")
def my_callback(sender, upload_id, completed_on):
    print(f"My upload {upload_id} was completed on {completed_on}.")

# app.py
from chunky_upload.signals import chunky_upload_complete
from django.apps import AppConfig

class MyApp(AppConfig):
    def ready(self):
        from . import receivers
        chunky_upload_complete.connect(receivers.my_callback)
```
