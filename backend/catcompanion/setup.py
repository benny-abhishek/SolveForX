#!/usr/bin/env python3
"""
Quick setup script for Cat Companion backend.
This script helps automate the database setup process.
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n📋 {description}")
    print(f"Running: {command}")
    
    try:
        if platform.system() == "Windows":
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command.split(), check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}")
        print(f"Command output: {e.stdout}")
        print(f"Error output: {e.stderr}")
        return False

def check_postgresql():
    """Check if PostgreSQL is installed and running."""
    print("\n🔍 Checking PostgreSQL installation...")
    
    try:
        subprocess.run(["psql", "--version"], check=True, capture_output=True)
        print("✅ PostgreSQL is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PostgreSQL is not installed or not in PATH")
        return False

def create_database():
    """Create the caterpillar database."""
    print("\n🗄️ Creating database...")
    
    # Try different usernames based on platform
    system = platform.system()
    if system == "Windows":
        username = "postgres"
    else:
        username = os.getenv("USER", "postgres")
    
    command = f"createdb -U {username} caterpillar"
    success = run_command(command, "Database creation")
    
    if not success:
        print("\n💡 Database creation failed. This might be because:")
        print("   - The database already exists (which is fine)")
        print("   - Wrong username - check your PostgreSQL setup")
        print("   - PostgreSQL service is not running")
    
    return success

def install_dependencies():
    """Install Python dependencies."""
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def run_migrations():
    """Run Django migrations."""
    return run_command("python manage.py migrate", "Running migrations")

def create_superuser():
    """Prompt to create a superuser."""
    print("\n👤 Would you like to create a superuser account? (y/n): ", end="")
    response = input().lower().strip()
    
    if response in ['y', 'yes']:
        return run_command("python manage.py createsuperuser", "Creating superuser")
    return True

def main():
    """Main setup function."""
    print("🐱 Cat Companion Backend Setup")
    print("=" * 40)
    
    # Check prerequisites
    if not check_postgresql():
        print("\n🛠️ Please install PostgreSQL first:")
        if platform.system() == "Windows":
            print("   Download from: https://www.postgresql.org/download/windows/")
        elif platform.system() == "Darwin":  # macOS
            print("   Run: brew install postgresql")
        else:  # Linux
            print("   Run: sudo apt-get install postgresql postgresql-contrib")
        sys.exit(1)
    
    # Setup steps
    steps = [
        ("📦 Installing dependencies", install_dependencies),
        ("🗄️ Creating database", create_database),
        ("🔄 Running migrations", run_migrations),
        ("👤 Creating superuser", create_superuser),
    ]
    
    for description, func in steps:
        print(f"\n{description}")
        if not func():
            print(f"\n❌ Setup failed at: {description}")
            print("Please check the error messages above and try again.")
            sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Copy catcompanion/settings_example.py to catcompanion/settings_local.py")
    print("2. Update the database configuration in settings_local.py if needed")
    print("3. Run 'python manage.py runserver' to start the development server")

if __name__ == "__main__":
    main() 