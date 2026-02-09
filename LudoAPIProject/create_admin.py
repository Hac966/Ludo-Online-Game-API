import os
import django

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LudoAPIProject.settings')
django.setup()

from django.contrib.auth.models import User

# Replace these with what you want
username = 'fezile'
email = 'admin@example.com'
password = 'mazibuko'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created successfully!")
else:
    print(f"Superuser '{username}' already exists.")