from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # operator, manager, admin
    operator_id = db.Column(db.String(10), db.ForeignKey('operator.id'), nullable=True)  # Only for operators
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship to operator
    operator = db.relationship('Operator', back_populates='user_account', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Machine(db.Model):
    id = db.Column(db.String(10), primary_key=True)  # e.g., EXC001
    model = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100))
    status = db.Column(db.String(20), default='Active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    operators = db.relationship('Operator', backref='assigned_machine', lazy=True)
    sensor_data = db.relationship('SensorData', backref='machine', lazy=True)
    tasks = db.relationship('Task', backref='machine', lazy=True)
    incidents = db.relationship('SafetyIncident', backref='machine', lazy=True)

class Operator(db.Model):
    id = db.Column(db.String(10), primary_key=True)  # e.g., OP1001
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    certification_level = db.Column(db.String(20), default='Basic')
    machine_id = db.Column(db.String(10), db.ForeignKey('machine.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_account = db.relationship('User', back_populates='operator', lazy=True)
    sensor_data = db.relationship('SensorData', backref='operator', lazy=True)
    tasks = db.relationship('Task', backref='operator', lazy=True)
    incidents = db.relationship('SafetyIncident', backref='operator', lazy=True)
    training_records = db.relationship('TrainingRecord', backref='operator', lazy=True)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    machine_id = db.Column(db.String(10), db.ForeignKey('machine.id'), nullable=False)
    operator_id = db.Column(db.String(10), db.ForeignKey('operator.id'), nullable=False)
    engine_hours = db.Column(db.Float, nullable=False)
    fuel_used = db.Column(db.Float, nullable=False)  # Liters
    load_cycles = db.Column(db.Integer, nullable=False)
    idling_time = db.Column(db.Integer, nullable=False)  # Minutes
    seatbelt_status = db.Column(db.String(20), nullable=False)  # Fastened/Unfastened
    safety_alert_triggered = db.Column(db.Boolean, default=False)
    proximity_alert = db.Column(db.Boolean, default=False)
    temperature = db.Column(db.Float)  # Engine temperature
    hydraulic_pressure = db.Column(db.Float)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    machine_id = db.Column(db.String(10), db.ForeignKey('machine.id'), nullable=False)
    operator_id = db.Column(db.String(10), db.ForeignKey('operator.id'), nullable=False)
    assigned_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Manager who assigned
    scheduled_date = db.Column(db.Date, nullable=False)
    estimated_duration = db.Column(db.Integer)  # Minutes
    actual_duration = db.Column(db.Integer)  # Minutes
    status = db.Column(db.String(20), default='Pending')  # Pending, In Progress, Completed
    priority = db.Column(db.String(10), default='Medium')  # Low, Medium, High
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationship to the assigning manager
    assigner = db.relationship('User', backref='assigned_tasks', lazy=True)

class SafetyIncident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.String(10), db.ForeignKey('machine.id'), nullable=False)
    operator_id = db.Column(db.String(10), db.ForeignKey('operator.id'), nullable=False)
    incident_type = db.Column(db.String(50), nullable=False)  # Seatbelt, Proximity, Idling, etc.
    severity = db.Column(db.String(10), nullable=False)  # Low, Medium, High
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    resolved = db.Column(db.Boolean, default=False)
    resolution_notes = db.Column(db.Text)

class TrainingRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operator_id = db.Column(db.String(10), db.ForeignKey('operator.id'), nullable=False)
    course_name = db.Column(db.String(200), nullable=False)
    course_type = db.Column(db.String(50), nullable=False)  # Safety, Technical, Certification
    completion_date = db.Column(db.Date)
    score = db.Column(db.Integer)  # Percentage
    status = db.Column(db.String(20), default='Assigned')  # Assigned, In Progress, Completed
    due_date = db.Column(db.Date)
    estimated_time = db.Column(db.Integer)  # Estimated completion time in minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
