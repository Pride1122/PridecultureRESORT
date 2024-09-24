# backend/app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Configure Database (SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prideculture_resort.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    arrival = db.Column(db.Date, nullable=False)
    departure = db.Column(db.Date, nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Booking {self.id} - {self.guests} guests>'


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Contact {self.id} - {self.email}>'


# Routes
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/booking', methods=['POST'])
def booking():
    arrival = request.form.get('arrival')
    departure = request.form.get('departure')
    guests = request.form.get('guests')

    if not arrival or not departure or not guests:
        flash('Please fill out all fields.', 'danger')
        return redirect(url_for('home'))

    try:
        new_booking = Booking(
            arrival=datetime.strptime(arrival, '%Y-%m-%d'),
            departure=datetime.strptime(departure, '%Y-%m-%d'),
            guests=int(guests)
        )
        db.session.add(new_booking)
        db.session.commit()
        flash('Your booking has been successfully made!', 'success')
        return redirect(url_for('thank_you'))
    except Exception as e:
        db.session.rollback()
        flash('There was an issue with your booking. Please try again.')
        print(e)

        return redirect(url_for('home'))


@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email or not message:
        flash('Please fill out all fields.', 'danger')
        return redirect(url_for('home'))

    try:
        new_contact = Contact(
            name=name,
            email=email,
            message=message
        )
        db.session.add(new_contact)
        db.session.commit()
        flash(
            'Thank you for reaching out! We will get back to you shortly.',
            'success')
        return redirect(url_for('thank_you'))
    except Exception as e:

        db.session.rollback()
        flash('There was an issue with your message. Please try again.')
        print(e)
        return redirect(url_for('home'))


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


if __name__ == '__main__':
    app.run(debug=True)
