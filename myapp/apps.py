from django.apps import AppConfig

class MyAppConfig(AppConfig):  # Use correct app name
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'  # Replace with your actual app name

    def ready(self):
        import myapp.signals  # Import signals when the app is ready
