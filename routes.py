from datetime import datetime, date, timedelta
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func, desc
from app import app, db
from models import Machine, Operator, SensorData, Task, SafetyIncident, TrainingRecord, User

@app.route('/')
def index():
    """Landing page with role selection"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).filter(
            User.role == role
        ).filter(
            User.is_active == True
        ).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect based on role
            if user.role == 'operator':
                return redirect(url_for('operator_dashboard'))
            elif user.role == 'manager':
                return redirect(url_for('manager_dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('manager_dashboard'))  # Admin uses manager view for now
        else:
            flash('Invalid username, password, or role selection.', 'error')
    
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Redirect to appropriate dashboard based on role"""
    if current_user.role == 'operator':
        return redirect(url_for('operator_dashboard'))
    else:
        return redirect(url_for('manager_dashboard'))

@app.route('/manager')
@login_required
def manager_dashboard():
    """Manager dashboard with overall statistics and operator filtering"""
    if current_user.role not in ['manager', 'admin']:
        flash('Access denied. Manager privileges required.', 'error')
        return redirect(url_for('operator_dashboard'))
    
    # Get filter parameters
    selected_operator = request.args.get('operator_filter')
    
    # Base queries
    machines_query = Machine.query
    operators_query = Operator.query
    tasks_query = Task.query
    alerts_query = SensorData.query.filter_by(safety_alert_triggered=True)
    incidents_query = SafetyIncident.query.filter_by(resolved=False)
    
    # Apply operator filter if selected
    if selected_operator:
        tasks_query = tasks_query.filter_by(operator_id=selected_operator)
        alerts_query = alerts_query.filter_by(operator_id=selected_operator)
        incidents_query = incidents_query.filter_by(operator_id=selected_operator)
    
    # Get statistics
    total_machines = machines_query.count()
    active_operators = operators_query.count()
    
    # Recent alerts
    recent_alerts = alerts_query.order_by(desc(SensorData.timestamp)).limit(5).all()
    
    # Today's tasks
    today_tasks = tasks_query.filter_by(scheduled_date=date.today()).all()
    
    # Recent incidents
    recent_incidents = incidents_query.order_by(desc(SafetyIncident.timestamp)).limit(5).all()
    
    # Calculate safety score
    total_records = SensorData.query.count()
    alert_records = SensorData.query.filter_by(safety_alert_triggered=True).count()
    safety_score = round(((total_records - alert_records) / max(total_records, 1)) * 100, 1) if total_records > 0 else 100
    
    # Get all operators for filter dropdown
    all_operators = Operator.query.all()
    
    return render_template('manager_dashboard.html',
                         total_machines=total_machines,
                         active_operators=active_operators,
                         recent_alerts=recent_alerts,
                         today_tasks=today_tasks,
                         recent_incidents=recent_incidents,
                         safety_score=safety_score,
                         all_operators=all_operators,
                         selected_operator=selected_operator)

@app.route('/operator')
@login_required 
def operator_dashboard():
    """Operator dashboard showing only their personal data"""
    if current_user.role != 'operator':
        flash('Access denied. Operator privileges required.', 'error')
        return redirect(url_for('manager_dashboard'))
    
    operator = current_user.operator
    if not operator:
        flash('No operator profile found. Please contact your manager.', 'error')
        return redirect(url_for('index'))
    
    # Get operator-specific data
    operator_tasks = Task.query.filter_by(operator_id=operator.id).order_by(Task.scheduled_date.desc()).limit(10).all()
    operator_alerts = SensorData.query.filter_by(
        operator_id=operator.id, 
        safety_alert_triggered=True
    ).order_by(desc(SensorData.timestamp)).limit(5).all()
    
    operator_training = TrainingRecord.query.filter_by(operator_id=operator.id).all()
    
    # Today's tasks
    today_tasks = Task.query.filter_by(
        operator_id=operator.id, 
        scheduled_date=date.today()
    ).all()
    
    # Training statistics
    total_training = len(operator_training)
    completed_training = len([t for t in operator_training if t.status == 'Completed'])
    pending_training = len([t for t in operator_training if t.status == 'Assigned'])
    overdue_training = len([t for t in operator_training if t.due_date and t.due_date < date.today() and t.status != 'Completed'])
    
    # Recent incidents involving this operator
    operator_incidents = SafetyIncident.query.filter_by(
        operator_id=operator.id,
        resolved=False
    ).order_by(desc(SafetyIncident.timestamp)).limit(3).all()
    
    return render_template('operator_dashboard.html',
                         operator=operator,
                         operator_tasks=operator_tasks,
                         operator_alerts=operator_alerts,
                         operator_training=operator_training,
                         today_tasks=today_tasks,
                         total_training=total_training,
                         completed_training=completed_training,
                         pending_training=pending_training,
                         overdue_training=overdue_training,
                         operator_incidents=operator_incidents,
                         date=date)



@app.route('/tasks')
@login_required
def task_management():
    """Task management dashboard"""
    query = Task.query
    
    # Filter by operator if user is an operator
    if current_user.role == 'operator':
        operator = current_user.operator
        if operator:
            query = query.filter_by(operator_id=operator.id)
    
    # Get all tasks ordered by priority (High, Medium, Low) and date
    from sqlalchemy import case
    priority_order = case(
        (Task.priority == 'High', 1),
        (Task.priority == 'Medium', 2),
        (Task.priority == 'Low', 3),
        else_=4
    )
    tasks = query.order_by(priority_order, Task.scheduled_date.desc()).all()
    
    # Calculate task statistics
    stats_query = Task.query
    if current_user.role == 'operator':
        operator = current_user.operator
        if operator:
            stats_query = stats_query.filter_by(operator_id=operator.id)
    
    total_tasks = stats_query.count()
    completed_tasks = stats_query.filter_by(status='Completed').count()
    pending_tasks = stats_query.filter_by(status='Pending').count()
    in_progress_tasks = stats_query.filter_by(status='In Progress').count()
    
    return render_template('tasks.html',
                         tasks=tasks,
                         total_tasks=total_tasks,
                         completed_tasks=completed_tasks,
                         pending_tasks=pending_tasks,
                         in_progress_tasks=in_progress_tasks)

@app.route('/task/update/<int:task_id>', methods=['POST'])
@login_required
def update_task_status(task_id):
    """Update task status"""
    task = Task.query.get_or_404(task_id)
    
    # Check if user can update this task
    if current_user.role == 'operator':
        operator = current_user.operator
        if not operator or task.operator_id != operator.id:
            flash('You can only update your own tasks.', 'error')
            return redirect(url_for('task_management'))
    
    new_status = request.form.get('status')
    if new_status in ['Pending', 'In Progress', 'Completed']:
        task.status = new_status
        if new_status == 'Completed':
            task.completed_at = datetime.utcnow()
        db.session.commit()
        flash(f'Task status updated to {new_status}', 'success')
    
    return redirect(url_for('task_management'))

@app.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    """Create new task (managers only)"""
    if current_user.role not in ['manager', 'admin']:
        flash('Access denied. Manager privileges required.', 'error')
        return redirect(url_for('task_management'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        machine_id = request.form.get('machine_id')
        operator_id = request.form.get('operator_id')
        scheduled_date = datetime.strptime(request.form.get('scheduled_date'), '%Y-%m-%d').date()
        estimated_duration = int(request.form.get('estimated_duration', 60))
        priority = request.form.get('priority', 'Medium')
        
        task = Task(
            title=title,
            description=description,
            machine_id=machine_id,
            operator_id=operator_id,
            assigned_by=current_user.id,
            scheduled_date=scheduled_date,
            estimated_duration=estimated_duration,
            priority=priority
        )
        
        db.session.add(task)
        db.session.commit()
        
        flash(f'Task "{title}" assigned to {operator_id} successfully!', 'success')
        return redirect(url_for('task_management'))
    
    # Get operators and machines for form
    operators = Operator.query.all()
    machines = Machine.query.all()
    
    return render_template('create_task.html', operators=operators, machines=machines, date=date)

@app.route('/training')
@login_required
def training_hub():
    """Operator training hub"""
    if current_user.role == 'operator':
        # Show only operator's training
        operator = current_user.operator
        if not operator:
            flash('No operator profile found.', 'error')
            return redirect(url_for('index'))
        
        operator_training = TrainingRecord.query.filter_by(operator_id=operator.id).all()
        
        # Calculate operator-specific training statistics
        total_courses = len(operator_training)
        completed_courses = len([t for t in operator_training if t.status == 'Completed'])
        overdue_courses = len([t for t in operator_training if t.due_date and t.due_date < date.today() and t.status != 'Completed'])
        
        # Get upcoming training due in next 7 days
        next_week = date.today() + timedelta(days=7)
        upcoming_training = [t for t in operator_training if t.due_date and date.today() <= t.due_date <= next_week and t.status != 'Completed']
        
        return render_template('training.html',
                             operator=operator,
                             training_records=operator_training,
                             total_courses=total_courses,
                             completed_courses=completed_courses,
                             overdue_courses=overdue_courses,
                             upcoming_training=upcoming_training,
                             operators=[operator],  # Single operator list for template compatibility
                             date=date,
                             timedelta=timedelta)
    else:
        # Manager view - show all operators with training
        operators = Operator.query.all()
        
        # Get training statistics
        total_courses = TrainingRecord.query.count()
        completed_courses = TrainingRecord.query.filter_by(status='Completed').count()
        overdue_courses = TrainingRecord.query.filter(
            TrainingRecord.due_date < date.today(),
            TrainingRecord.status != 'Completed'
        ).count()
        
        # Get upcoming training due in next 7 days
        next_week = date.today() + timedelta(days=7)
        upcoming_training = TrainingRecord.query.filter(
            TrainingRecord.due_date.between(date.today(), next_week),
            TrainingRecord.status != 'Completed'
        ).order_by(TrainingRecord.due_date).all()
        
        return render_template('training.html',
                             operators=operators,
                             total_courses=total_courses,
                             completed_courses=completed_courses,
                             overdue_courses=overdue_courses,
                             upcoming_training=upcoming_training,
                             date=date,
                             timedelta=timedelta)

@app.route('/reports')
@login_required
def reports():
    """Reports and analytics dashboard"""
    # Machine performance data for charts
    machines = Machine.query.all()
    performance_data = []
    
    for machine in machines:
        # Get average metrics for the last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        avg_data = db.session.query(
            func.avg(SensorData.fuel_used).label('avg_fuel'),
            func.avg(SensorData.idling_time).label('avg_idling'),
            func.avg(SensorData.load_cycles).label('avg_cycles'),
            func.count(SensorData.id).label('total_records')
        ).filter(
            SensorData.machine_id == machine.id,
            SensorData.timestamp >= thirty_days_ago
        ).first()
        
        if avg_data and avg_data.total_records > 0:
            performance_data.append({
                'machine_id': machine.id,
                'avg_fuel': round(avg_data.avg_fuel or 0, 2),
                'avg_idling': round(avg_data.avg_idling or 0, 1),
                'avg_cycles': round(avg_data.avg_cycles or 0, 1)
            })
    
    # Safety incidents by type
    incident_stats = db.session.query(
        SafetyIncident.incident_type,
        func.count(SafetyIncident.id).label('count')
    ).group_by(SafetyIncident.incident_type).all()
    
    return render_template('reports.html',
                         performance_data=performance_data,
                         incident_stats=incident_stats)



@app.route('/create_incident', methods=['POST'])
@login_required
def create_incident():
    """Create a new safety incident report"""
    machine_id = request.form.get('machine_id')
    operator_id = request.form.get('operator_id')
    incident_type = request.form.get('incident_type')
    severity = request.form.get('severity')
    description = request.form.get('description')
    
    # Create new incident
    incident = SafetyIncident(
        machine_id=machine_id,
        operator_id=operator_id,
        incident_type=incident_type,
        severity=severity,
        description=description,
        timestamp=datetime.utcnow(),
        resolved=False
    )
    
    db.session.add(incident)
    db.session.commit()
    
    flash(f'Safety incident reported successfully. Incident ID: {incident.id}', 'success')
    
    # Redirect back to appropriate dashboard based on user role
    if current_user.role == 'operator':
        return redirect(url_for('operator_dashboard'))
    else:
        return redirect(url_for('manager_dashboard'))

@app.route('/api/sensor-data/<machine_id>')
@login_required
def get_sensor_data(machine_id):
    """API endpoint for real-time sensor data"""
    latest_data = SensorData.query.filter_by(machine_id=machine_id)\
        .order_by(desc(SensorData.timestamp)).first()
    
    if latest_data:
        return jsonify({
            'timestamp': latest_data.timestamp.isoformat(),
            'fuel_used': latest_data.fuel_used,
            'engine_hours': latest_data.engine_hours,
            'load_cycles': latest_data.load_cycles,
            'idling_time': latest_data.idling_time,
            'seatbelt_status': latest_data.seatbelt_status,
            'safety_alert': latest_data.safety_alert_triggered
        })
    
    return jsonify({'error': 'No data found'}), 404
