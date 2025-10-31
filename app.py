from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, g
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to something random!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Availability(db.Model):
    __tablename__ = 'availability'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    day = db.Column(db.String(10), nullable=False)
    no_availability = db.Column(db.Boolean, default=False)
    duration = db.Column(db.Integer, default=0)

    user = db.relationship('User', back_populates='availabilities')

User.availabilities = db.relationship(
    'Availability',
    order_by=Availability.id,
    back_populates='user',
    cascade='all, delete-orphan'
)

class SubjectWeight(db.Model):
    __tablename__ = 'subject_weight'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    weight = db.Column(db.Integer, nullable=False, default=3)

    user = db.relationship('User', back_populates='subject_weights')

User.subject_weights = db.relationship(
    'SubjectWeight',
    order_by=SubjectWeight.id,
    back_populates='user',
    cascade='all, delete-orphan'
)
# ----------------------------------------------------------#
# Defaults
# Days
default_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

# Subjects
default_subjects = [
    "ALGORITHMS & DATA STRUCTURES",
    "MATHEMATICS FOR DATA MANAGEMENT AND ANALYSIS",
    "PROBABILITY & STATISTICS FOR DATA MANAGEMENT AND ANALYSIS",
    "PROGRAMMING FOR DATA MANAGEMENT & ANALYSIS",
    "TECHNOLOGY WITH IMPACT",
    "TIME SERIES ANALYSIS"
]


# ----------------------------------------------------------#

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user=g.user)

@app.route('/addtestuser')
def addtestuser():
    u = User(username="testuser", password="testpass")
    db.session.add(u)
    db.session.commit()
    return "Test user added!"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first(): # check if ist existing
            flash('Username already exists. Please choose another.')
            return render_template('register.html')

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

    # Availability based on user
        for code in default_days:
            db.session.add(Availability(
                user_id=new_user.id,
                day=code,
                no_availability=False,
                duration=120 # default availability (2 h = 120 min)
            ))
        db.session.commit()

    # Subject based on user
        for subj in default_subjects:
            db.session.add(SubjectWeight(
                user_id=new_user.id,
                subject=subj,
                weight=3
            ))
        db.session.commit()

        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html', user=g.user)

@app.route('/weight')
def weight():
    rows = SubjectWeight.query.filter_by(user_id=g.user.id).all()
    existing = {r.subject for r in rows}

    for subj in default_subjects:
        if subj not in existing:
            db.session.add(SubjectWeight(
                user_id=g.user.id,
                subject=subj,
                weight=3
            ))
    if len(existing) < len(default_subjects):
        db.session.commit()
        rows = SubjectWeight.query.filter_by(user_id=g.user.id).all()

    weights = {r.subject: r for r in rows}
    ordered = [weights[s] for s in default_subjects]

    return render_template('weight.html', user=g.user, subject_weights=ordered)

@app.route('/save_weights', methods=['POST'])
def save_weights():
    if not g.user:
        return jsonify(error="Not logged in"), 403

    data = request.get_json() or {}

    SubjectWeight.query.filter_by(user_id=g.user.id).delete()

    for subj, wt in data.items():
        db.session.add(SubjectWeight(
            user_id=g.user.id,
            subject=subj,
            weight=wt
        ))
    db.session.commit()
    return jsonify(message="Weights saved!")

@app.before_request
def load_current_user():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

@app.route('/schedule')
def schedule():
    rows = Availability.query.filter_by(user_id=g.user.id).all()
    existing = {r.day for r in rows}

    for code in ['mon','tue','wed','thu','fri','sat','sun']:
        if code not in existing:
            db.session.add(Availability(
                user_id=g.user.id,
                day=code,
                no_availability=False,
                duration=480
            ))
    if len(existing) < 7:
        db.session.commit()
        rows = Availability.query.filter_by(user_id=g.user.id).all()

    availabilities = {r.day: r for r in rows}

    return render_template( # see availability per person
        'schedule.html',
        user=g.user,
        availabilities=availabilities
    )

# Route to save availability
@app.route('/save_availability', methods=['POST'])
def save_availability():
    # print("Save route called")  # Debug: Check if route is hit
    data = request.get_json() or {}
   #  print(f"Received data: {data}")  # Debug: See what data was sent
    user_id = session.get('user_id')
    if not user_id:
        print("No user_id in session")  # Debug: Login issue
        return jsonify(error="Not logged in"), 403

    # Clear existing for this user
    Availability.query.filter_by(user_id=user_id).delete()
    # print(f"Cleared existing for user {user_id}")  # Debug

    # Insert new data
    for day, info in data.items():
        #print(f"Saving {day}: {info}")  # Debug: Per-day data
        avail = Availability(
            user_id=user_id,
            day=day,
            no_availability=info.get('no_availability', False),
            duration=info.get('duration', 0)
        )
        db.session.add(avail)

    try:
        db.session.commit()
        #print("Commit successful")  # Debug
        return jsonify(message="Availability saved!")
    except Exception as e:
        #print(f"Commit failed: {e}")  # Debug: DB error
        db.session.rollback()
        return jsonify(error="Save failed"), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)