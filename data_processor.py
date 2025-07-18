import csv
import random
import string
from datetime import datetime, date, timedelta
from app import db
from models import Machine, Operator, SensorData, Task, SafetyIncident, TrainingRecord, User

def initialize_sample_data():
    """Initialize the database with sample data if it's empty"""
    
    # Check if data already exists
    if Machine.query.first():
        print("Sample data already exists, skipping initialization.")
        return
    
    print("Initializing sample data...")
    
    # Create machines
    create_sample_machines()
    
    # Create operators
    create_sample_operators()
    
    # Create users with authentication
    create_sample_users()
    
    # Create sensor data
    create_sample_sensor_data()
    
    # Create tasks
    create_sample_tasks()
    
    # Create safety incidents
    create_sample_safety_incidents()
    
    # Create enhanced training records
    create_enhanced_training_data()
    
    db.session.commit()
    print("Sample data initialization completed.")

def create_sample_machines():
    """Create sample heavy equipment machines"""
    from models import Machine
    machines = [
        {'id': 'EXC001', 'model': 'CAT 320 Excavator', 'location': 'North Quarry'},
        {'id': 'EXC002', 'model': 'CAT 330 Excavator', 'location': 'South Quarry'},
        {'id': 'LDR001', 'model': 'CAT 950M Loader', 'location': 'Loading Bay A'},
        {'id': 'LDR002', 'model': 'CAT 966M Loader', 'location': 'Loading Bay B'},
    ]
    
    for machine_data in machines:
        machine = Machine(**machine_data)
        db.session.add(machine)
    
    print("Created sample machines")

def create_sample_operators():
    """Create sample equipment operators"""
    from models import Operator
    operators = [
        {'id': 'OP1001', 'name': 'John Smith', 'email': 'john.smith@company.com', 'certification_level': 'Advanced', 'machine_id': 'EXC001'},
        {'id': 'OP1002', 'name': 'Maria Garcia', 'email': 'maria.garcia@company.com', 'certification_level': 'Intermediate', 'machine_id': 'EXC002'},
        {'id': 'OP1003', 'name': 'David Johnson', 'email': 'david.johnson@company.com', 'certification_level': 'Basic', 'machine_id': 'LDR001'},
        {'id': 'OP1004', 'name': 'Sarah Wilson', 'email': 'sarah.wilson@company.com', 'certification_level': 'Advanced', 'machine_id': 'LDR002'},
    ]
    
    for operator_data in operators:
        operator = Operator(**operator_data)
        db.session.add(operator)
    
    print("Created sample operators")

def create_sample_users():
    """Create sample users for authentication"""
    from models import User
    users = [
        # Operators
        {'username': 'john.smith', 'email': 'john.smith@company.com', 'role': 'operator', 'operator_id': 'OP1001', 'password': 'operator123'},
        {'username': 'maria.garcia', 'email': 'maria.garcia@company.com', 'role': 'operator', 'operator_id': 'OP1002', 'password': 'operator123'},
        {'username': 'david.johnson', 'email': 'david.johnson@company.com', 'role': 'operator', 'operator_id': 'OP1003', 'password': 'operator123'},
        {'username': 'sarah.wilson', 'email': 'sarah.wilson@company.com', 'role': 'operator', 'operator_id': 'OP1004', 'password': 'operator123'},
        
        # Managers
        {'username': 'manager', 'email': 'manager@company.com', 'role': 'manager', 'operator_id': None, 'password': 'manager123'},
        {'username': 'supervisor', 'email': 'supervisor@company.com', 'role': 'manager', 'operator_id': None, 'password': 'manager123'},
        
        # Admin
        {'username': 'admin', 'email': 'admin@company.com', 'role': 'admin', 'operator_id': None, 'password': 'admin123'},
    ]
    
    for user_data in users:
        password = user_data.pop('password')
        user = User(**user_data)
        user.set_password(password)
        db.session.add(user)
    
    print("Created sample users")

def create_sample_sensor_data():
    """Create sample sensor data for monitoring"""
    machines = ['EXC001', 'EXC002', 'LDR001', 'LDR002']
    operators = ['OP1001', 'OP1002', 'OP1003', 'OP1004']
    
    # Create data for the last 30 days
    start_date = datetime.utcnow() - timedelta(days=30)
    
    for day in range(30):
        current_date = start_date + timedelta(days=day)
        
        # Create 3-8 records per day per machine
        for machine_id, operator_id in zip(machines, operators):
            records_per_day = random.randint(3, 8)
            
            for _ in range(records_per_day):
                # Random time during working hours (6 AM to 6 PM)
                hour = random.randint(6, 18)
                minute = random.randint(0, 59)
                timestamp = current_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                sensor_data = SensorData(
                    timestamp=timestamp,
                    machine_id=machine_id,
                    operator_id=operator_id,
                    engine_hours=round(random.uniform(8.0, 12.0), 1),
                    fuel_used=round(random.uniform(3.5, 6.0), 2),
                    load_cycles=random.randint(5, 12),
                    idling_time=random.randint(15, 60),
                    seatbelt_status=random.choice(['Fastened', 'Fastened', 'Fastened', 'Unfastened']),  # 75% fastened
                    safety_alert_triggered=random.choice([False, False, False, False, True]),  # 20% alerts
                    proximity_alert=random.choice([False, False, False, True]),  # 25% proximity alerts
                    temperature=round(random.uniform(180.0, 220.0), 1),
                    hydraulic_pressure=round(random.uniform(2800.0, 3200.0), 1)
                )
                db.session.add(sensor_data)
    
    print("Created sample sensor data")

def create_sample_tasks():
    """Create sample work tasks"""
    task_templates = [
        ('Excavation - North Wall', 'Excavate north wall section for foundation prep', 180, 'High'),
        ('Material Loading', 'Load gravel into trucks for transport', 120, 'Medium'),
        ('Site Cleanup', 'Clear debris from work area', 90, 'Low'),
        ('Trenching Work', 'Dig trenches for utility lines', 240, 'High'),
        ('Stockpile Management', 'Organize material stockpiles', 60, 'Low'),
        ('Equipment Inspection', 'Daily equipment safety inspection', 30, 'High'),
        ('Grading Work', 'Level ground for new construction', 150, 'Medium'),
        ('Debris Removal', 'Remove construction debris', 75, 'Low'),
        ('Foundation Digging', 'Dig foundation for new building', 300, 'High'),
        ('Road Maintenance', 'Repair access road surfaces', 120, 'Medium'),
    ]
    
    machines = ['EXC001', 'EXC002', 'LDR001', 'LDR002']
    operators = ['OP1001', 'OP1002', 'OP1003', 'OP1004']
    manager_user = User.query.filter_by(role='manager').first()
    
    # Create tasks for the last 10 days and next 10 days
    start_date = date.today() - timedelta(days=10)
    
    for day in range(20):  # 10 past + 10 future days
        current_date = start_date + timedelta(days=day)
        
        # 1-3 tasks per day
        daily_tasks = random.randint(1, 3)
        
        for _ in range(daily_tasks):
            title, description, base_duration, priority = random.choice(task_templates)
            machine_id = random.choice(machines)
            operator_id = operators[machines.index(machine_id)]  # Assign to machine's operator
            
            # Add some randomness to duration
            estimated_duration = base_duration + random.randint(-30, 30)
            
            # Determine status based on date
            if current_date < date.today():
                status = random.choice(['Completed', 'Completed', 'Completed', 'In Progress'])
                actual_duration = estimated_duration + random.randint(-20, 40) if status == 'Completed' else None
                completed_at = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=random.randint(8, 16)) if status == 'Completed' else None
            elif current_date == date.today():
                status = random.choice(['Pending', 'In Progress', 'Completed'])
                actual_duration = None
                completed_at = None
            else:
                status = 'Pending'
                actual_duration = None
                completed_at = None
            
            task = Task(
                title=title,
                description=description,
                machine_id=machine_id,
                operator_id=operator_id,
                assigned_by=manager_user.id if manager_user else None,
                scheduled_date=current_date,
                estimated_duration=estimated_duration,
                actual_duration=actual_duration,
                status=status,
                priority=priority,
                completed_at=completed_at
            )
            db.session.add(task)
    
    print("Created sample tasks")

def create_sample_safety_incidents():
    """Create sample safety incidents"""
    incident_types = [
        ('Seatbelt Violation', 'Low'),
        ('Excessive Idling', 'Medium'),
        ('Equipment Malfunction', 'High'),
        ('Proximity Alert', 'Medium'),
        ('Unauthorized Operation', 'High'),
    ]
    
    machines = ['EXC001', 'EXC002', 'LDR001', 'LDR002']
    operators = ['OP1001', 'OP1002', 'OP1003', 'OP1004']
    
    # Create incidents for the last 15 days
    start_date = datetime.utcnow() - timedelta(days=15)
    
    for day in range(15):
        current_date = start_date + timedelta(days=day)
        
        # 0-2 incidents per day (most days have 0-1)
        daily_incidents = random.choices([0, 1, 2], weights=[60, 35, 5])[0]
        
        for _ in range(daily_incidents):
            incident_type, severity = random.choice(incident_types)
            machine_id = random.choice(machines)
            operator_id = operators[machines.index(machine_id)]
            
            # Random time during working hours
            hour = random.randint(6, 18)
            minute = random.randint(0, 59)
            timestamp = current_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            descriptions = {
                'Seatbelt Violation': 'Operator detected without seatbelt fastened during operation',
                'Excessive Idling': f'Machine left idling for {random.randint(45, 90)} minutes',
                'Equipment Malfunction': 'Hydraulic system showing abnormal pressure readings',
                'Proximity Alert': 'Machine operated too close to personnel/obstacles',
                'Unauthorized Operation': 'Machine operated outside designated area',
            }
            
            incident = SafetyIncident(
                machine_id=machine_id,
                operator_id=operator_id,
                incident_type=incident_type,
                severity=severity,
                description=descriptions[incident_type],
                timestamp=timestamp,
                resolved=random.choice([True, True, False])  # 67% resolved
            )
            db.session.add(incident)
    
    print("Created sample safety incidents")

def create_enhanced_training_data():
    """Create enhanced training records with estimated time calculations"""
    
    # Enhanced course catalog with realistic data
    courses = [
        # Safety Courses
        ('Heavy Equipment Safety Fundamentals', 'Safety', 45, 'Basic safety protocols for heavy equipment operation'),
        ('Advanced Safety Procedures', 'Safety', 60, 'Advanced safety techniques and emergency response'),
        ('Workplace Safety Certification', 'Certification', 90, 'Comprehensive workplace safety certification program'),
        ('Emergency Response Training', 'Safety', 30, 'Emergency response procedures and protocols'),
        ('OSHA Compliance Training', 'Safety', 75, 'OSHA regulations and compliance requirements'),
        
        # Technical Courses
        ('CAT 320 Excavator Operations', 'Technical', 120, 'Complete operation training for CAT 320 excavators'),
        ('CAT 950M Loader Certification', 'Technical', 100, 'Professional certification for CAT 950M loaders'),
        ('Advanced Equipment Maintenance', 'Technical', 80, 'Advanced maintenance and troubleshooting techniques'),
        ('Hydraulic Systems Training', 'Technical', 60, 'Understanding and maintaining hydraulic systems'),
        ('Engine Diagnostics', 'Technical', 90, 'Engine troubleshooting and diagnostic procedures'),
        ('Fuel Efficiency Best Practices', 'Technical', 40, 'Techniques for optimizing fuel consumption'),
        
        # Certification Courses
        ('Equipment Operator Certification Level I', 'Certification', 150, 'Basic equipment operator certification'),
        ('Equipment Operator Certification Level II', 'Certification', 180, 'Intermediate equipment operator certification'),
        ('Equipment Operator Certification Level III', 'Certification', 240, 'Advanced equipment operator certification'),
        ('Site Supervisor Certification', 'Certification', 200, 'Supervisory skills and site management'),
    ]
    
    operators = ['OP1001', 'OP1002', 'OP1003', 'OP1004']
    operator_levels = {'OP1001': 'Advanced', 'OP1002': 'Intermediate', 'OP1003': 'Basic', 'OP1004': 'Advanced'}
    
    for operator_id in operators:
        operator_level = operator_levels[operator_id]
        
        # Number of courses based on certification level
        if operator_level == 'Advanced':
            num_courses = random.randint(8, 12)
        elif operator_level == 'Intermediate':
            num_courses = random.randint(5, 8)
        else:
            num_courses = random.randint(3, 6)
        
        # Select courses for this operator
        assigned_courses = random.sample(courses, min(num_courses, len(courses)))
        
        for course_name, course_type, base_duration, description in assigned_courses:
            # Calculate estimated time using algorithm based on:
            # - Base course duration
            # - Operator experience level
            # - Course complexity
            # - Random factor for individual variation
            
            estimated_time = calculate_training_time(base_duration, operator_level, course_type)
            
            # Determine course status and dates
            status_weights = {
                'Advanced': [30, 15, 55],    # [Assigned, In Progress, Completed]
                'Intermediate': [40, 20, 40],
                'Basic': [50, 25, 25]
            }
            
            status = random.choices(
                ['Assigned', 'In Progress', 'Completed'],
                weights=status_weights[operator_level]
            )[0]
            
            # Generate dates
            if status == 'Completed':
                completion_date = date.today() - timedelta(days=random.randint(1, 90))
                due_date = completion_date + timedelta(days=random.randint(7, 30))
                score = random.randint(75, 100)
            elif status == 'In Progress':
                completion_date = None
                due_date = date.today() + timedelta(days=random.randint(7, 60))
                score = None
            else:  # Assigned
                completion_date = None
                due_date = date.today() + timedelta(days=random.randint(10, 90))
                score = None
            
            training = TrainingRecord(
                operator_id=operator_id,
                course_name=course_name,
                course_type=course_type,
                completion_date=completion_date,
                score=score,
                status=status,
                due_date=due_date,
                estimated_time=estimated_time
            )
            
            db.session.add(training)
    
    print("Created enhanced training data with ML-based time estimates")

def calculate_training_time(base_duration, operator_level, course_type):
    """
    Calculate estimated training time using algorithm based on:
    - Base course duration (historical average)
    - Operator experience level (learning speed factor)  
    - Course complexity (technical vs safety vs certification)
    - Individual variation factor
    
    This simulates what an XGBoost model might predict based on historical data
    """
    
    # Base duration in minutes
    estimated_time = base_duration
    
    # Operator experience factor (how quickly they learn)
    experience_factors = {
        'Advanced': 0.85,    # 15% faster than average
        'Intermediate': 1.0,  # Average learning speed
        'Basic': 1.25        # 25% slower than average
    }
    
    estimated_time *= experience_factors.get(operator_level, 1.0)
    
    # Course complexity factor
    complexity_factors = {
        'Safety': 0.9,        # Generally easier to understand
        'Technical': 1.2,     # More complex, hands-on practice needed
        'Certification': 1.4  # Most comprehensive and thorough
    }
    
    estimated_time *= complexity_factors.get(course_type, 1.0)
    
    # Individual variation (simulates personal learning differences)
    variation_factor = random.uniform(0.8, 1.3)
    estimated_time *= variation_factor
    
    # Round to nearest 5 minutes
    estimated_time = round(estimated_time / 5) * 5
    
    return int(estimated_time)
