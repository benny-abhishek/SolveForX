# CatCompanion

A comprehensive monitoring and management system with a React frontend and Django backend, featuring real-time safety monitoring, daily task management, and critical alert systems.

## 🚀 Features

- **Real-time Safety Monitoring**: Monitor system safety metrics and alerts
- **Daily Task Management**: Track and manage daily operational tasks
- **Critical Alert System**: Real-time notifications for critical system events
- **Dashboard Overview**: Comprehensive system overview and analytics
- **Modern UI**: Clean, responsive interface built with React and TypeScript
- **GraphQL API**: Efficient data fetching and mutations
- **Django Backend**: Robust backend with Django REST framework

## 🏗️ Project Structure

```
SolveForX/
├── backend/                 # Django backend application
│   └── catcompanion/       # Main Django project
│       ├── cat_operator/   # Cat operator management app
│       ├── machine_logs/   # Machine logging and monitoring
│       ├── manage.py       # Django management script
│       └── requirements.txt # Python dependencies
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── graphql/        # GraphQL queries and mutations
│   │   └── types/          # TypeScript type definitions
│   ├── package.json        # Node.js dependencies
│   └── tsconfig.json       # TypeScript configuration
└── README.md              # This file
```

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript
- **GraphQL** for API communication
- **CSS Modules** for styling
- **Modern ES6+** JavaScript

### Backend
- **Django 4.x** with Python
- **Django REST Framework** for API endpoints
- **GraphQL** support
- **PostgreSQL** (recommended database)

## 📋 Prerequisites

Before running this project, make sure you have the following installed:

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **pip** (Python package manager)
- **npm** or **yarn** (Node.js package manager)

## 🚀 Getting Started

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend/catcompanion
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

The Django backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

The React frontend will be available at `http://localhost:3000`

## 📁 Key Components

### Frontend Components

- **Dashboard**: Main application interface with tab navigation
- **OverviewTab**: System overview and key metrics
- **SafetyMonitorTab**: Real-time safety monitoring interface
- **DailyTasksTab**: Daily task management and tracking
- **CriticalAlert**: Critical alert display and management
- **Header**: Application header with navigation
- **TabNavigation**: Tab-based navigation system

### Backend Apps

- **cat_operator**: Cat operator management and operations
- **machine_logs**: Machine logging, monitoring, and analytics

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/solveforx
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Django Settings

Copy `settings_example.py` to `settings.py` and configure according to your environment.

## 🧪 Testing

### Backend Tests
```bash
cd backend/catcompanion
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 API Documentation

The project uses GraphQL for API communication. You can explore the GraphQL schema at:
- **GraphQL Playground**: `http://localhost:8000/graphql/` (when backend is running)

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

**Built with ❤️ for efficient system monitoring and management**