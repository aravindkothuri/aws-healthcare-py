from datetime import datetime
from app import db

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.String(50), nullable=False)
    availability = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, default=5.0)
    image = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'specialty': self.specialty,
            'qualification': self.qualification,
            'experience': self.experience,
            'availability': self.availability,
            'rating': self.rating,
            'image': self.image
        }

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    appointment_date = db.Column(db.String(50), nullable=False)
    appointment_time = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Confirmed')
    symptoms = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctor = db.relationship('Doctor', backref=db.backref('appointments', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'patient_name': self.patient_name,
            'email': self.email,
            'phone': self.phone,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name if self.doctor else 'Unknown',
            'department': self.department,
            'appointment_date': self.appointment_date,
            'appointment_time': self.appointment_time,
            'status': self.status,
            'symptoms': self.symptoms,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }
