# Cat Companion Backend Setup

This Django application uses PostgreSQL as its database. Follow the instructions below to set up the development environment.

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## Database Setup

### Windows Setup

1. **Install PostgreSQL**
   - Download PostgreSQL from https://www.postgresql.org/download/windows/
   - During installation, remember the password you set for the `postgres` user
   - Make sure to add PostgreSQL to your PATH during installation

2. **Create Database**
   ```cmd
   # Open Command Prompt as Administrator and run:
   createdb -U postgres caterpillar
   ```

3. **Install Python Dependencies**
   ```cmd
   cd backend\catcompanion
   pip install -r requirements.txt
   ```

4. **Configure Database Settings**
   - Copy `catcompanion/settings_example.py` to `catcompanion/settings_local.py`
   - Update the database configuration in `settings_local.py`:
   ```python
   DATABASES = {
       "default": {
           "ENGINE": "django.db.backends.postgresql",
           "NAME": "caterpillar",
           "USER": "postgres",
           "PASSWORD": "your_postgres_password",
           "HOST": "localhost",
           "PORT": "5432",
       }
   }
   ```

5. **Run Migrations**
   ```cmd
   python manage.py migrate
   ```

### macOS/Linux Setup

1. **Install PostgreSQL**
   ```bash
   # macOS (using Homebrew)
   brew install postgresql
   brew services start postgresql
   
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   
   # Start PostgreSQL service
   sudo systemctl start postgresql
   ```

2. **Create Database**
   ```bash
   createdb caterpillar
   ```

3. **Install Python Dependencies**
   ```bash
   cd backend/catcompanion
   pip install -r requirements.txt
   ```

4. **Configure Database Settings**
   - The default settings should work with your system username
   - If needed, create `catcompanion/settings_local.py` and override database settings

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

## Running the Development Server

After setup is complete, you can start the development server:

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Environment Variables (Optional)

For production or sensitive configurations, consider using environment variables:

```python
import os
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)

# In settings.py or settings_local.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_env_variable("DB_NAME"),
        "USER": get_env_variable("DB_USER"),
        "PASSWORD": get_env_variable("DB_PASSWORD"),
        "HOST": get_env_variable("DB_HOST"),
        "PORT": get_env_variable("DB_PORT"),
    }
}
```

## Troubleshooting

### Common Issues

1. **"role does not exist" error**
   - Update the `USER` field in your database configuration to match your PostgreSQL username
   - On Windows, this is usually `postgres`
   - On macOS/Linux, this is usually your system username

2. **Connection refused**
   - Make sure PostgreSQL service is running
   - Check if the port 5432 is available and not blocked by firewall

3. **Authentication failed**
   - Verify your PostgreSQL password
   - Check your `pg_hba.conf` file for authentication methods

### Useful Commands

```bash
# Check PostgreSQL service status
# Windows
sc query postgresql-x64-14

# macOS
brew services list | grep postgresql

# Linux
sudo systemctl status postgresql

# Connect to database directly
psql -d caterpillar -U your_username

# List all databases
psql -l

# List tables in current database
psql -d caterpillar -c "\dt"
```

## Contributing

When making database changes:
1. Create and apply migrations: `python manage.py makemigrations`
2. Run migrations: `python manage.py migrate`
3. Test your changes thoroughly
4. Commit both your model changes and migration files 