from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, g
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ============ Database Models ============
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    points = db.Column(db.Integer, default=0)


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
    allocation = db.Column(db.Integer, nullable=False, default=0)
    user = db.relationship('User', back_populates='subject_weights')


User.subject_weights = db.relationship(
    'SubjectWeight',
    order_by=SubjectWeight.id,
    back_populates='user',
    cascade='all, delete-orphan'
)


class StudySession(db.Model):
    __tablename__ = 'study_session'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    points_earned = db.Column(db.Integer, nullable=False)
    date_logged = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    user = db.relationship('User', back_populates='study_sessions')


User.study_sessions = db.relationship(
    'StudySession',
    order_by=StudySession.date_logged.desc(),
    back_populates='user',
    cascade='all, delete-orphan'
)

# ============ Defaults ============
default_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

default_subjects = [
    "ALGORITHMS & DATA STRUCTURES",
    "MATHEMATICS FOR DATA MANAGEMENT AND ANALYSIS",
    "PROBABILITY & STATISTICS FOR DATA MANAGEMENT AND ANALYSIS",
    "PROGRAMMING FOR DATA MANAGEMENT & ANALYSIS",
    "TECHNOLOGY WITH IMPACT",
    "TIME SERIES ANALYSIS"
]


# ============ Helper Functions ============
def calculate_allocations(user_id):
    """Calculate and update allocations for all subjects based on weights and availability"""
    availabilities = Availability.query.filter_by(user_id=user_id).all()
    total_duration = sum(
        avail.duration for avail in availabilities
        if not avail.no_availability
    )

    subject_weights = SubjectWeight.query.filter_by(user_id=user_id).all()
    total_weight = sum(sw.weight for sw in subject_weights)

    if total_weight > 0:
        for sw in subject_weights:
            sw.allocation = round((sw.weight / total_weight) * total_duration)
        db.session.commit()


def build_leaderboard_tree():
    """
    Build BST from all users and return tree data
    Demonstrates: OOP, BST construction, Tree traversal
    """
    bst = LeaderboardBST()
    users = User.query.all()

    # Insert each user into BST
    for user in users:
        bst.insert(user.id, user.username, user.points)

    # Get sorted list using traversal
    sorted_users = bst.get_sorted_descending()

    # Add ranks
    for rank, user in enumerate(sorted_users, start=1):
        user['rank'] = rank

    return {
        'sorted_users': sorted_users,
        'tree_structure': bst.get_tree_for_display(),
        'tree_height': bst.get_tree_height(),
        'node_count': bst.count_nodes(),
        'insertion_steps': bst.insertion_steps
    }


# ============ Routes ============
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
    if not g.user:
        return redirect(url_for('login'))

    # Get user's subjects with allocations
    subject_weights = SubjectWeight.query.filter_by(user_id=g.user.id).all()

    # Calculate hours logged per subject
    subjects_overview = []
    completed_count = 0
    in_progress_count = 0

    for sw in subject_weights:
        # Get total minutes logged for this subject
        logged_sessions = StudySession.query.filter_by(
            user_id=g.user.id,
            subject=sw.subject
        ).all()

        total_logged_minutes = sum(session.duration_minutes for session in logged_sessions)
        total_logged_hours = total_logged_minutes / 60

        # Convert minutes -> hours
        assigned_hours = round(sw.allocation / 60, 1)

        # status
        if assigned_hours == 0:
            status = 'Not Assigned'
            status_class = 'not-started'
        elif total_logged_hours >= assigned_hours:
            status = 'Done'
            status_class = 'done'
            completed_count += 1
        elif total_logged_hours > 0:
            status = 'In Progress'
            status_class = 'in-progress'
            in_progress_count += 1
        else:
            status = 'Not Started'
            status_class = 'not-started'

        subjects_overview.append({
            'subject': sw.subject,
            'assigned_hours': assigned_hours,
            'logged_hours': round(total_logged_hours, 1),
            'status': status,
            'status_class': status_class
        })

    #  total study sessions
    total_sessions = StudySession.query.filter_by(user_id=g.user.id).count()

    #  total study hours
    all_sessions = StudySession.query.filter_by(user_id=g.user.id).all()
    total_minutes = sum(session.duration_minutes for session in all_sessions)
    hours = int(total_minutes // 60)
    minutes = int(total_minutes % 60)
    seconds = int((total_minutes % 1) * 60)
    total_hours_formatted = f"{hours}:{minutes:02d}:{seconds:02d}"

    #  total assigned hours
    total_assigned_hours = sum(sw.allocation for sw in subject_weights) / 60

    # Build stats dictionary
    stats = {
        'total_sessions': total_sessions,
        'completed_subjects': completed_count,
        'in_progress_subjects': in_progress_count,
        'total_hours': total_hours_formatted,
        'total_assigned_hours': round(total_assigned_hours, 1),
        'total_subjects': len(subject_weights)
    }

    return render_template(
        'dashboard.html',
        user=g.user,
        subjects_overview=subjects_overview,
        stats=stats
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another.')
            return render_template('register.html')

        initial_points = 0
        new_user = User(username=username, password=password, points=initial_points)
        db.session.add(new_user)
        db.session.commit()

        for code in default_days:
            db.session.add(Availability(
                user_id=new_user.id,
                day=code,
                no_availability=False,
                duration=120
            ))
        db.session.commit()

        for subj in default_subjects:
            db.session.add(SubjectWeight(
                user_id=new_user.id,
                subject=subj,
                weight=3,
                allocation=0
            ))
        db.session.commit()

        calculate_allocations(new_user.id)
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/leaderboard')
def leaderboard():
    """
    Leaderboard using BST and Traversal Algorithm
    Demonstrates: OOP, Tree Data Structure, Reverse In-Order Traversal
    """
    if not g.user:
        return redirect(url_for('login'))

    leaderboard_data = build_leaderboard_tree()

    return render_template(
        'leaderboard.html',
        user=g.user,
        leaderboard=leaderboard_data['sorted_users'],
        tree_structure=leaderboard_data['tree_structure'],
        tree_height=leaderboard_data['tree_height'],
        node_count=leaderboard_data['node_count'],
        insertion_steps=leaderboard_data['insertion_steps']
    )


@app.route('/add_points', methods=['POST'])
def add_points():
    if not g.user:
        return jsonify(error="Not logged in"), 403

    data = request.get_json()
    points = data.get('points', 10)

    g.user.points += points
    db.session.commit()

    return jsonify(message=f"Added {points} points!", new_total=g.user.points)


@app.route('/weight')
def weight():
    if not g.user:
        return redirect(url_for('login'))

    rows = SubjectWeight.query.filter_by(user_id=g.user.id).all()
    existing = {r.subject for r in rows}

    for subj in default_subjects:
        if subj not in existing:
            db.session.add(SubjectWeight(
                user_id=g.user.id,
                subject=subj,
                weight=3,
                allocation=0
            ))
    if len(existing) < len(default_subjects):
        db.session.commit()
        rows = SubjectWeight.query.filter_by(user_id=g.user.id).all()

    calculate_allocations(g.user.id)
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
            weight=wt,
            allocation=0
        ))
    db.session.commit()
    calculate_allocations(g.user.id)

    return jsonify(message="Weights saved!")


@app.before_request
def load_current_user():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@app.route('/schedule')
def schedule():
    if not g.user:
        return redirect(url_for('login'))

    rows = Availability.query.filter_by(user_id=g.user.id).all()
    existing = {r.day for r in rows}

    for code in default_days:
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
    return render_template('schedule.html', user=g.user, availabilities=availabilities)


@app.route('/save_availability', methods=['POST'])
def save_availability():
    data = request.get_json() or {}
    user_id = session.get('user_id')
    if not user_id:
        return jsonify(error="Not logged in"), 403

    Availability.query.filter_by(user_id=user_id).delete()

    for day, info in data.items():
        avail = Availability(
            user_id=user_id,
            day=day,
            no_availability=info.get('no_availability', False),
            duration=info.get('duration', 0)
        )
        db.session.add(avail)

    try:
        db.session.commit()
        calculate_allocations(user_id)
        return jsonify(message="Availability saved!")
    except Exception as e:
        db.session.rollback()
        return jsonify(error="Save failed"), 500


@app.route('/study_log')
def study_log():
    if not g.user:
        return redirect(url_for('login'))

    # Get user's subjects
    subjects = SubjectWeight.query.filter_by(user_id=g.user.id).all()
    subject_list = [sw.subject for sw in subjects]

    if not subject_list:
        subject_list = default_subjects

    # Get recent study sessions
    recent_sessions = StudySession.query.filter_by(user_id=g.user.id).order_by(
        StudySession.date_logged.desc()
    ).limit(10).all()

    #  total study time and points
    all_sessions = StudySession.query.filter_by(user_id=g.user.id).all()
    total_minutes = sum(s.duration_minutes for s in all_sessions)
    total_hours = total_minutes / 60

    return render_template(
        'study_log.html',
        user=g.user,
        subjects=subject_list,
        recent_sessions=recent_sessions,
        total_hours=round(total_hours, 1),
        total_sessions=len(all_sessions)
    )


@app.route('/log_study_session', methods=['POST'])
def log_study_session():
    if not g.user:
        return jsonify(error="Not logged in"), 403

    data = request.get_json()
    subject = data.get('subject')
    duration = data.get('duration')  # in minutes

    if not subject or not duration:
        return jsonify(error="Subject and duration required"), 400

    try:
        duration = int(duration)
        if duration <= 0:
            return jsonify(error="Duration must be positive"), 400
    except ValueError:
        return jsonify(error="Invalid duration"), 400

    # Calculate points: 1 point per minute of study
    points_earned = duration

    #  study session record
    session_record = StudySession(
        user_id=g.user.id,
        subject=subject,
        duration_minutes=duration,
        points_earned=points_earned
    )
    db.session.add(session_record)

    # Add points
    g.user.points += points_earned

    try:
        db.session.commit()
        return jsonify(
            message=f"Study session logged! You earned {points_earned} points!",
            points_earned=points_earned,
            new_total_points=g.user.points
        )
    except Exception as e:
        db.session.rollback()
        return jsonify(error="Failed to log session"), 500


@app.route('/delete_study_session/<int:session_id>', methods=['POST'])
def delete_study_session(session_id):
    if not g.user:
        return jsonify(error="Not logged in"), 403

    session_record = StudySession.query.get(session_id)

    if not session_record:
        return jsonify(error="Session not found"), 404

    if session_record.user_id != g.user.id:
        return jsonify(error="Unauthorized"), 403

    # Remove points
    g.user.points -= session_record.points_earned
    if g.user.points < 0:
        g.user.points = 0

    db.session.delete(session_record)

    try:
        db.session.commit()
        return jsonify(message="Session deleted", new_total_points=g.user.points)
    except Exception as e:
        db.session.rollback()
        return jsonify(error="Failed to delete session"), 500


# ============ OOP: Tree Node Class ============
class TreeNode:
    """
    Node in Binary Search Tree for leaderboard
    Demonstrates: OOP principles, encapsulation, object attributes
    """

    def __init__(self, user_id, username, points):
        self.user_id = user_id
        self.username = username
        self.points = points
        self.left = None  # Left child (lower points)
        self.right = None  # Right child (higher points)

    def __repr__(self):
        return f"TreeNode({self.username}, {self.points}pts)"


# ============ OOP: Binary Search Tree Class ============
class LeaderboardBST:
    """
    Binary Search Tree for managing study leaderboard
    Demonstrates: Tree data structure, recursive algorithms, OOP design
    """

    def __init__(self):
        self.root = None
        self.insertion_steps = []

    def insert(self, user_id, username, points):
        """
        Insert a user into the BST based on points
        Time Complexity: O(log n) average, O(n) worst case
        """
        if self.root is None:
            self.root = TreeNode(user_id, username, points)
            self.insertion_steps.append(f"Created root node: {username} ({points} pts)")
        else:
            self._insert_recursive(self.root, user_id, username, points)

    def _insert_recursive(self, node, user_id, username, points):
        """
        Helper method for recursive insertion
        Demonstrates: Recursion, BST insertion algorithm
        """
        if points < node.points:
            # Go left (lower points)
            if node.left is None:
                node.left = TreeNode(user_id, username, points)
                self.insertion_steps.append(
                    f"Inserted {username} ({points} pts) as LEFT child of {node.username} ({node.points} pts)"
                )
            else:
                self._insert_recursive(node.left, user_id, username, points)
        else:
            # Go right (higher or equal points)
            if node.right is None:
                node.right = TreeNode(user_id, username, points)
                self.insertion_steps.append(
                    f"Inserted {username} ({points} pts) as RIGHT child of {node.username} ({node.points} pts)"
                )
            else:
                self._insert_recursive(node.right, user_id, username, points)

    def get_sorted_descending(self):
        """
        Traverse tree and return sorted list in DESCENDING order
        Uses REVERSE in-order traversal (Right -> Root -> Left)
        Time Complexity: O(n) - visits each node once
        """
        result = []
        self._reverse_inorder_traversal(self.root, result)
        return result

    def _reverse_inorder_traversal(self, node, result):
        """
        Recursive reverse in-order traversal
        Visit order: Right subtree -> Root -> Left subtree
        This gives us descending order (highest to lowest)
        Demonstrates: Tree traversal algorithm, recursion
        """
        if node is not None:
            # First traverse right subtree (higher values)
            self._reverse_inorder_traversal(node.right, result)

            # Then visit current node
            result.append({
                'user_id': node.user_id,
                'username': node.username,
                'points': node.points
            })

            # Finally traverse left subtree (lower values)
            self._reverse_inorder_traversal(node.left, result)

    def get_tree_height(self):
        return self._calculate_height(self.root)

    def _calculate_height(self, node):
        if node is None:
            return 0
        left_height = self._calculate_height(node.left)
        right_height = self._calculate_height(node.right)
        return 1 + max(left_height, right_height)

    def count_nodes(self):
        return self._count_nodes_recursive(self.root)

    def _count_nodes_recursive(self, node):
        if node is None:
            return 0
        return 1 + self._count_nodes_recursive(node.left) + self._count_nodes_recursive(node.right)

    def get_tree_for_display(self): # convert tree to nested dict for template rendering
        if self.root is None:
            return None
        return self._node_to_dict(self.root)

    def _node_to_dict(self, node):    #  convert a node and its children to dictionary

        if node is None:
            return None
        return {
            'user_id': node.user_id,
            'username': node.username,
            'points': node.points,
            'left': self._node_to_dict(node.left),
            'right': self._node_to_dict(node.right)
        }


# ============ OOP: Graph Class for Study Buddies ============
from collections import deque


class StudyBuddyGraph:
    """
    Graph data structure for finding study buddies
    Demonstrates: Graph theory, BFS/DFS algorithms, adjacency list representation
    """

    def __init__(self):
        self.graph = {}  # Adjacency list: {user_id: [connected_user_ids]}
        self.user_data = {}  # Store user information
        self.connections = 0
        self.traversal_path = []

    def add_user(self, user_id, username, points, subjects): # add user to ggraph
        if user_id not in self.graph:
            self.graph[user_id] = []
            self.user_data[user_id] = {
                'username': username,
                'points': points,
                'subjects': set(subjects)
            }

    def add_connection(self, user1_id, user2_id):
        if user1_id in self.graph and user2_id in self.graph:
            if user2_id not in self.graph[user1_id]:
                self.graph[user1_id].append(user2_id)
                self.graph[user2_id].append(user1_id)
                self.connections += 1

    def calculate_compatibility(self, user1_id, user2_id):
        user1 = self.user_data[user1_id]
        user2 = self.user_data[user2_id]

        # Shared subjects score (0-50 points)
        shared = user1['subjects'].intersection(user2['subjects'])
        total_subjects = max(len(user1['subjects']), len(user2['subjects']))
        subject_score = (len(shared) / total_subjects * 50) if total_subjects > 0 else 0

        # Points similarity score (0-50 points)
        point_diff = abs(user1['points'] - user2['points'])
        max_possible_diff = 1000  # Assume max difference of 1000 points
        point_score = max(0, 50 - (point_diff / max_possible_diff * 50))

        total_score = int(subject_score + point_score)
        return total_score, list(shared), point_diff

    def bfs_find_buddies(self, start_user_id, max_buddies=10):
        """
        Breadth-First Search to find study buddies
        BFS explores level by level - finds closest connections first
        Time Complexity: O(V + E) where V = vertices, E = edges
        Demonstrates: BFS algorithm, queue data structure
        """
        if start_user_id not in self.graph:
            return []

        visited = set()
        queue = deque([start_user_id])
        visited.add(start_user_id)
        buddies = []
        self.traversal_path = [f"BFS Start: {self.user_data[start_user_id]['username']}"]
        nodes_explored = 0
        max_depth = 0

        current_depth = 0
        nodes_at_current_depth = 1
        nodes_at_next_depth = 0

        while queue and len(buddies) < max_buddies:
            current_user = queue.popleft()
            nodes_explored += 1
            nodes_at_current_depth -= 1

            # Calculate compatibility with all connected users
            for neighbor_id in self.graph[current_user]:
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append(neighbor_id)
                    nodes_at_next_depth += 1

                    if neighbor_id != start_user_id:
                        score, shared, point_diff = self.calculate_compatibility(
                            start_user_id, neighbor_id
                        )

                        neighbor = self.user_data[neighbor_id]
                        buddies.append({
                            'user_id': neighbor_id,
                            'username': neighbor['username'],
                            'points': neighbor['points'],
                            'compatibility': score,
                            'shared_subjects': shared,
                            'point_diff': point_diff,
                            'depth': current_depth
                        })

                        self.traversal_path.append(
                            f"→ {neighbor['username']} (depth {current_depth}, score {score})"
                        )

            # Track depth levels
            if nodes_at_current_depth == 0:
                current_depth += 1
                max_depth = max(max_depth, current_depth)
                nodes_at_current_depth = nodes_at_next_depth
                nodes_at_next_depth = 0

        # Sort by compatibility score
        buddies.sort(key=lambda x: x['compatibility'], reverse=True)

        return buddies[:max_buddies], {
            'algorithm': 'BFS (Breadth-First Search)',
            'nodes_explored': nodes_explored,
            'max_depth': max_depth,
            'traversal_path': ' '.join(self.traversal_path)
        }

    def dfs_find_buddies(self, start_user_id, max_buddies=10):
        """
        Depth-First Search to find study buddies
        DFS explores deeply before backtracking
        Time Complexity: O(V + E) where V = vertices, E = edges
        Demonstrates: DFS algorithm, recursion, stack-based traversal
        """
        if start_user_id not in self.graph:
            return []

        visited = set()
        buddies = []
        self.traversal_path = [f"DFS Start: {self.user_data[start_user_id]['username']}"]
        stats = {'nodes_explored': 0, 'max_depth': 0}

        def dfs_recursive(user_id, depth=0):
            if len(buddies) >= max_buddies:
                return

            visited.add(user_id)
            stats['nodes_explored'] += 1
            stats['max_depth'] = max(stats['max_depth'], depth)

            for neighbor_id in self.graph[user_id]:
                if neighbor_id not in visited and len(buddies) < max_buddies:
                    if neighbor_id != start_user_id:
                        score, shared, point_diff = self.calculate_compatibility(
                            start_user_id, neighbor_id
                        )

                        neighbor = self.user_data[neighbor_id]
                        buddies.append({
                            'user_id': neighbor_id,
                            'username': neighbor['username'],
                            'points': neighbor['points'],
                            'compatibility': score,
                            'shared_subjects': shared,
                            'point_diff': point_diff,
                            'depth': depth
                        })

                        self.traversal_path.append(
                            f"→ {neighbor['username']} (depth {depth}, score {score})"
                        )

                    dfs_recursive(neighbor_id, depth + 1)

        dfs_recursive(start_user_id)

        # Sort by compatibility score
        buddies.sort(key=lambda x: x['compatibility'], reverse=True)

        return buddies[:max_buddies], {
            'algorithm': 'DFS (Depth-First Search)',
            'nodes_explored': stats['nodes_explored'],
            'max_depth': stats['max_depth'],
            'traversal_path': ' '.join(self.traversal_path)
        }

    def get_graph_density(self):# calculate graph density (% of possible connections)
        num_users = len(self.graph)
        if num_users <= 1:
            return 0
        max_connections = (num_users * (num_users - 1)) / 2
        return int((self.connections / max_connections * 100)) if max_connections > 0 else 0


def build_study_buddy_graph(current_user_id):
    graph = StudyBuddyGraph()

    users = User.query.all()

    for user in users: # userss as nodes
        subjects = [sw.subject for sw in user.subject_weights]
        graph.add_user(user.id, user.username, user.points, subjects)

    # Create edges based on compatibility
    COMPATIBILITY_THRESHOLD = 30  # Only connect users with 30%+ compatibility

    for i, user1 in enumerate(users):
        for user2 in users[i + 1:]:
            score, _, _ = graph.calculate_compatibility(user1.id, user2.id)
            if score >= COMPATIBILITY_THRESHOLD:
                graph.add_connection(user1.id, user2.id)

    return graph


# ============ Route for Study Groups ============
@app.route('/study_groups')
def study_groups():
    if not g.user:
        return redirect(url_for('login'))

    # Build the study buddy graph
    graph = build_study_buddy_graph(g.user.id)

    # Use BFS to find study buddies (change to dfs_find_buddies to use DFS)
    buddies, search_info = graph.bfs_find_buddies(g.user.id, max_buddies=10)

    # Add score classes for visual styling
    for buddy in buddies:
        if buddy['compatibility'] >= 70:
            buddy['score_class'] = 'high'
        elif buddy['compatibility'] >= 50:
            buddy['score_class'] = 'medium'
        else:
            buddy['score_class'] = 'low'

    # Calc average path length
    total_depth = sum(b['depth'] for b in buddies)
    avg_path_length = round(total_depth / len(buddies), 1) if buddies else 0

    graph_info = {
        'algorithm': search_info['algorithm'],
        'nodes_explored': search_info['nodes_explored'],
        'max_depth': search_info['max_depth'],
        'connections': graph.connections,
        'density': graph.get_graph_density(),
        'avg_path_length': avg_path_length,
        'traversal_path': search_info['traversal_path']
    }

    total_users = User.query.count()

    return render_template(
        'study_groups.html',
        user=g.user,
        potential_buddies=buddies,
        total_users=total_users,
        graph_info=graph_info
    )


# ============ __main__ ============
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

### This was a test
        # Add points column to existing users if it doesn't exist
        try:
            from sqlalchemy import inspect

            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('user')]

            if 'points' not in columns:
                # Add points column to existing table
                with db.engine.connect() as conn:
                    conn.execute(db.text('ALTER TABLE user ADD COLUMN points INTEGER DEFAULT 0'))
                    conn.commit()
                print("Added 'points' column to User table")

                # Set random points for existing users
                users = User.query.all()
                for user in users:
                    user.points = random.randint(100, 1000)
                db.session.commit()
                print(f"Updated {len(users)} users with random points")
        except Exception as e:
            print(f"Migration note: {e}")

        # Verify all tables exist
        print("Database tables created:")
        print(db.metadata.tables.keys())

    app.run(host='0.0.0.0', port=5050, debug=True)
