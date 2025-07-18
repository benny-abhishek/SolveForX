# Smart Operator Management System

A comprehensive heavy equipment operator management system built with Flask, featuring real-time safety monitoring, task management, training tracking, and incident reporting for construction and mining operations.

## 🚀 Features

- **Real-time Safety Monitoring**: Monitor equipment safety metrics including seatbelt status, proximity alerts, and engine conditions
- **Operator Management**: Track operator certifications, assignments, and performance metrics
- **Task Management**: Create, assign, and track daily operational tasks with priority levels
- **Training Hub**: Manage operator training records, course assignments, and certification tracking
- **Incident Reporting**: Record and track safety incidents with severity classification
- **Role-based Access**: Separate dashboards for operators, managers, and administrators
- **Equipment Tracking**: Monitor machine status, location, and operational data
- **Reporting & Analytics**: Comprehensive reporting on safety metrics, task completion, and training progress

## 🏗️ Project Structure

```
SolveForX/
├── app.py                 # Flask application configuration and setup
├── main.py               # Application entry point
├── models.py             # SQLAlchemy database models
├── routes.py             # Flask route handlers and views
├── data_processor.py     # Sample data initialization and data processing
├── pyproject.toml        # Python dependencies and project configuration
├── uv.lock              # Dependency lock file
├── sample_data.csv      # Sample data for testing
├── cat-logo.jpeg        # Application logo
├── instance/            # Database files (SQLite)
│   └── smart_operator.db
├── static/              # Static assets
│   ├── css/
│   │   └── style.css    # Main stylesheet
│   └── js/
│       └── dashboard.js # Dashboard JavaScript functionality
└── templates/           # HTML templates
    ├── base.html        # Base template with navigation
    ├── index.html       # Landing page with login
    ├── dashboard.html   # General dashboard
    ├── manager_dashboard.html    # Manager-specific dashboard
    ├── operator_dashboard.html   # Operator-specific dashboard
    ├── tasks.html       # Task management interface
    ├── create_task.html # Task creation form
    ├── training.html    # Training management interface
    └── reports.html     # Reporting and analytics
```

## 🛠️ Technology Stack

### Backend
- **Flask 3.1.1** - Web framework
- **SQLAlchemy 3.1.1** - Database ORM
- **Flask-Login 0.6.3** - User authentication
- **SQLite/PostgreSQL** - Database (SQLite for development, PostgreSQL for production)
- **Gunicorn 23.0.0** - WSGI server for production

### Frontend
- **HTML5** with Jinja2 templating
- **CSS3** with modern responsive design
- **JavaScript** for interactive dashboard features
- **Bootstrap** (included in templates) for UI components

### Database Models
- **User** - Authentication and role management
- **Operator** - Equipment operator profiles
- **Machine** - Heavy equipment tracking
- **SensorData** - Real-time equipment monitoring data
- **Task** - Work task management
- **SafetyIncident** - Safety incident reporting
- **TrainingRecord** - Operator training and certification tracking

## 📋 Prerequisites

Before running this project, make sure you have the following installed:

- **Python 3.11 or higher**
- **pip** (Python package manager)
- **uv** (recommended for dependency management)

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone <repository-url>
cd SolveForX
```

### 2. Install Dependencies
Using uv (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables
Create a `.env` file in the project root:
```env
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///instance/smart_operator.db
SESSION_SECRET=your-secret-key-here
```

### 4. Initialize the Database
The application will automatically create the database and populate it with sample data on first run.

### 5. Run the Application
```bash
python main.py
```

The application will be available at `http://localhost:5001`

## 👥 User Roles & Access

### Operator
- View personal dashboard with assigned tasks
- Track training progress and certifications
- View safety alerts and incidents
- Update task status and completion

### Manager
- Overview of all operators and equipment
- Create and assign tasks
- Monitor safety metrics and incidents
- Access comprehensive reporting
- Manage training assignments



## 🔐 Default Login Credentials

The system comes with sample users for testing:

### Operators
- Username: `john.smith` / Password: `operator123`
- Username: `maria.garcia` / Password: `operator123`
- Username: `david.johnson` / Password: `operator123`
- Username: `sarah.wilson` / Password: `operator123`

### Managers
- Username: `manager` / Password: `manager123`
- Username: `supervisor` / Password: `manager123`

## 📊 Key Features Explained

### Safety Monitoring
- **Real-time Alerts**: Monitor seatbelt status, proximity warnings, and engine conditions
- **Incident Tracking**: Record and classify safety incidents by severity
- **Safety Score**: Calculate overall safety performance metrics

### Task Management
- **Priority Levels**: High, Medium, Low priority classification
- **Status Tracking**: Pending, In Progress, Completed states
- **Duration Tracking**: Estimated vs actual completion times
- **Assignment System**: Managers can assign tasks to specific operators

### Training Management
- **Course Types**: Safety, Technical, and Certification training
- **Progress Tracking**: Monitor completion status and scores
- **Due Date Management**: Track overdue and upcoming training requirements
- **Certification Levels**: Basic, Intermediate, Advanced operator levels

### Equipment Management
- **Machine Tracking**: Monitor equipment status and location
- **Sensor Data**: Real-time monitoring of engine hours, fuel usage, and operational metrics
- **Operator Assignment**: Link operators to specific equipment

## 🧪 Testing

### Run the Application
```bash
python main.py
```

### Access Different Dashboards
1. **Operator Dashboard**: Login as any operator user
2. **Manager Dashboard**: Login as manager or admin user
3. **Task Management**: Access via `/tasks` route
4. **Training Hub**: Access via `/training` route
5. **Reports**: Access via `/reports` route

## 🔧 Configuration

### Database Configuration
The application supports both SQLite (development) and PostgreSQL (production):

```python
# Development (SQLite)
DATABASE_URL=sqlite:///instance/smart_operator.db

# Production (PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/smart_operator
```

### Security Configuration
- Change the `SESSION_SECRET` environment variable in production
- Use HTTPS in production environments
- Configure proper database credentials

## 📈 Sample Data

The application includes comprehensive sample data:
- 4 heavy equipment machines (excavators and loaders)
- 4 operators with different certification levels
- 30 days of sensor data with realistic operational metrics
- Sample tasks, incidents, and training records
- Multiple user accounts for testing different roles

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the existing issues in the repository
2. Create a new issue with detailed information about your problem
3. Include system information, error messages, and steps to reproduce

## 🔄 Updates

Stay updated with the latest changes by:
- Watching the repository
- Checking the releases page
- Following the commit history

---

**Built with ❤️ for efficient heavy equipment operator management and safety monitoring**