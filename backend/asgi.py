import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

try:
    from django.core.asgi import get_asgi_application
    application = get_asgi_application()
except ImportError:
    raise ImportError(
        "Could not import Django. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable? Did you "
        "forget to activate a virtual environment?"
    )
