# Copy this file to settings_local.py and update the values for your environment

# Database configuration for local development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "caterpillar",
        "USER": "your_database_username",  # Windows: usually 'postgres', macOS/Linux: your system username
        "PASSWORD": "your_database_password",  # Windows: password set during installation, macOS/Linux: often empty
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Optional: Override other settings for local development
# DEBUG = True
# ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Example for Windows:
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "caterpillar",
#         "USER": "postgres",
#         "PASSWORD": "your_postgres_password",
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# }

# Example for macOS/Linux:
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "caterpillar",
#         "USER": "your_username",  # Replace with your system username
#         "PASSWORD": "",  # Often empty for local development
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# } 