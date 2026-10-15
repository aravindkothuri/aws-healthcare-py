from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import Doctor, Appointment

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # Seed initial doctor records if table is empty
    if Doctor.query.count() == 0:
        initial_doctors = [
            Doctor(name="Dr. Aravind Sharma", specialty="Cardiology", qualification="MD, DM (Cardiology)", experience="15 Years", availability="Mon - Fri: 9:00 AM - 2:00 PM", rating=4.9, image="https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&q=80&w=400"),
            Doctor(name="Dr. Priya Nair", specialty="Pediatrics", qualification="MD (Pediatrics), DCH", experience="10 Years", availability="Mon - Sat: 10:00 AM - 4:00 PM", rating=4.8, image="https://images.unsplash.com/photo-1594824813576-9c424a6e3448?auto=format&fit=crop&q=80&w=400"),
            Doctor(name="Dr. Rajesh Kumar", specialty="Orthopedics", qualification="MS (Ortho), M.Ch", experience="12 Years", availability="Tue - Sun: 11:00 AM - 6:00 PM", rating=4.7, image="https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&q=80&w=400"),
            Doctor(name="Dr. Sneha Reddy", specialty="General Medicine", qualification="MBBS, MRCP (UK)", experience="8 Years", availability="Mon - Fri: 8:00 AM - 1:00 PM", rating=4.9, image="https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&q=80&w=400")
        ]
        db.session.bulk_save_objects(initial_doctors)
        db.session.commit()

    return render_template('index.html')

@bp.route('/api/doctors', methods=['GET'])
def get_doctors():
    department = request.args.get('department')
    query = Doctor.query
    if department and department != 'All Departments':
        query = query.filter_by(specialty=department)
    doctors = query.all()
    return jsonify([d.to_dict() for d in doctors])

@bp.route('/api/appointments', methods=['GET', 'POST'])
def handle_appointments():
    if request.method == 'GET':
        appointments = Appointment.query.order_by(Appointment.created_at.desc()).all()
        return jsonify([a.to_dict() for a in appointments])
    
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        required_fields = ['patient_name', 'email', 'phone', 'doctor_id', 'department', 'appointment_date', 'appointment_time']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing field: {field}'}), 400

        new_apt = Appointment(
            patient_name=data['patient_name'],
            email=data['email'],
            phone=data['phone'],
            doctor_id=data['doctor_id'],
            department=data['department'],
            appointment_date=data['appointment_date'],
            appointment_time=data['appointment_time'],
            symptoms=data.get('symptoms', '')
        )
        db.session.add(new_apt)
        db.session.commit()
        return jsonify({'message': 'Appointment booked successfully!', 'appointment': new_apt.to_dict()}), 201

@bp.route('/api/appointments/<int:apt_id>', methods=['PUT', 'DELETE'])
def modify_appointment(apt_id):
    apt = Appointment.query.get_or_404(apt_id)
    if request.method == 'PUT':
        data = request.get_json()
        apt.status = data.get('status', apt.status)
        apt.appointment_date = data.get('appointment_date', apt.appointment_date)
        apt.appointment_time = data.get('appointment_time', apt.appointment_time)
        db.session.commit()
        return jsonify({'message': 'Appointment updated successfully', 'appointment': apt.to_dict()})
    
    elif request.method == 'DELETE':
        apt.status = 'Cancelled'
        db.session.commit()
        return jsonify({'message': 'Appointment cancelled successfully'})

@bp.route('/api/stats', methods=['GET'])
def get_stats():
    total_appts = Appointment.query.count()
    completed_appts = Appointment.query.filter_by(status='Completed').count()
    active_doctors = Doctor.query.count()
    return jsonify({
        'total_appointments': total_appts,
        'completed_appointments': completed_appts,
        'active_doctors': active_doctors,
        'patient_satisfaction': '99.4%'
    })
