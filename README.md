# Smart Study Planner

A comprehensive web-based study planning application that helps students organize their study schedules, track progress, earn points, and connect with study buddies. Built with Flask and SQLAlchemy, this application demonstrates advanced data structures and algorithms including Binary Search Trees (BST) and Graph algorithms (BFS/DFS).

---

## 📋 Description

**Smart Study Planner** is a personalized study management system designed to help students optimize their learning experience. The application allows users to:

- Set weekly availability schedules
- Assign priority weights to different subjects
- Log study sessions and earn points based on study time
- View leaderboards powered by Binary Search Tree algorithms
- Find compatible study buddies using Graph traversal algorithms
- Track progress through an intuitive dashboard

The app features a clean, modern interface with a dark theme and smooth navigation across all pages.

---

## ✨ Features

### **User Management**
- **User Registration & Authentication**: Secure login system with password protection
- **Personalized Dashboard**: Overview of study progress, session statistics, and subject status
- **Points System**: Earn 1 point per minute of logged study time

### **Subject Management**
- **Subject Weighting**: Assign priority weights (1-6) to six predefined subjects
- **Automatic Time Allocation**: System calculates study time allocation based on weights and availability
- **Unique Weight Assignment**: Each weight (1-6) must be assigned to exactly one subject

### **Schedule Planning**
- **Weekly Availability**: Set study hours for each day of the week (15 minutes to 24 hours)
- **Flexible Scheduling**: Mark days as unavailable when needed
- **Visual Time Selectors**: Easy-to-use range sliders for setting study duration

### **Study Log**
- **Session Tracking**: Log study sessions by subject and duration
- **Quick Time Presets**: Fast logging with preset durations (15, 30, 45, 60, 90, 120 minutes)
- **Session History**: View recent study sessions with timestamps
- **Point Rewards**: Automatic point calculation and user total updates

### **Leaderboard (BST Implementation)**
- **Binary Search Tree**: User rankings organized using BST data structure
- **Dual Views**: Toggle between sorted leaderboard and tree structure visualization
- **Tree Analytics**: View tree height, node count, and insertion steps
- **Algorithm Demonstration**: Educational display of BST construction process

### **Study Groups (Graph Implementation)**
- **BFS/DFS Algorithms**: Find study buddies using Breadth-First Search or Depth-First Search
- **Compatibility Scoring**: Matches based on shared subjects and similar point totals
- **Graph Visualization**: Display of graph density, connections, and traversal paths
- **Connection System**: See potential study partners with compatibility percentages

### **Dashboard Analytics**
- **Study Statistics**: Total sessions, completed subjects, in-progress subjects
- **Time Tracking**: Total study hours and assigned hours per subject
- **Interactive Calendar**: Monthly calendar view with current date highlighting
- **Status Badges**: Visual indicators for subject completion status (Done, In Progress, Not Started)

---

## 📁 Files

### **Core Application Files**

#### `app.py` (Main Application File)
The heart of the application containing:
- **Flask Configuration**: App initialization, database setup, secret key management
- **Database Models**: User, Availability, SubjectWeight, StudySession tables
- **Route Handlers**: All page routes and API endpoints
- **OOP Classes**: TreeNode, LeaderboardBST, StudyBuddyGraph classes implementing data structures
- **Helper Functions**: calculate_allocations(), build_leaderboard_tree(), build_study_buddy_graph()
- **Algorithm Implementations**: BST insertion, reverse in-order traversal, BFS, DFS

#### `users.db` (SQLite Database)
Stores all persistent application data:
- User credentials and points
- Weekly availability schedules
- Subject weights and allocations
- Study session logs with timestamps

### **HTML Templates** (in `/templates` directory)

#### `welcome.html`
- Landing page with branding and call-to-action buttons
- Navigation to registration or login

#### `register.html`
- User registration form
- Username and password input
- Form validation and error messaging
- Tips section for new users

#### `login.html`
- User authentication form
- Remember me checkbox
- Password visibility toggle
- Forgot password link

#### `dashboard.html`
- Main user interface after login
- Interactive calendar widget with month navigation
- Subject overview table showing assigned hours and status
- Study statistics panel (sessions, hours, completed subjects)
- Alerts section for notifications
- Milestones display

#### `weight.html`
- Subject weight assignment interface
- Six subjects with weight selectors (1-6 dropdown)
- Weight validation to ensure unique assignments
- Save functionality that triggers allocation recalculation

#### `schedule.html`
- Weekly availability editor
- Seven-day schedule with time range sliders
- "No Availability" checkbox option per day
- Real-time duration display (hours and minutes)

#### `study_log.html`
- Study session logging form
- Subject selector dropdown
- Duration input with quick preset buttons
- Recent sessions list with delete functionality
- Statistics display (total points, hours, sessions)

#### `leaderboard.html`
- View toggle between sorted list and tree structure
- Sorted leaderboard with rankings and points
- Tree visualization using Jinja2 macros
- Tree construction steps display
- BST statistics (height, node count, complexity)

#### `study_groups.html`
- Study buddy recommendation system
- Graph algorithm statistics
- Compatibility scoring display
- Shared subjects badges
- Connect button for each potential buddy
- Graph density and traversal information

### **Configuration Files**

#### `.idea/` (PyCharm Project Settings)
- IDE configuration files
- Database connections
- Git integration settings
- Python interpreter configuration

#### `README.md` (Original)
Basic project setup information including:
- Required libraries (flask, flask_sqlalchemy)
- Server URLs and ports
- Debugger PIN

#### `configuration`
Network configuration details for local access

---

## 🔧 Prerequisites and Environment

### **Python Version**
- **Python 3.13** (developed and tested with Python 3.13)
- Minimum: Python 3.8+ should work

### **Operating System**
- **Developed on**: macOS
- **Compatible with**: Windows, Linux, macOS

### **Required Libraries**

```
flask==3.1.0
flask-sqlalchemy==3.1.1
sqlalchemy==2.0.36
```

### **Additional Dependencies**
- **SQLite3**: Built into Python, no separate installation needed
- **jQuery 3.6.0**: Loaded via CDN in HTML templates

### **IDE/Editor**
- Developed using PyCharm Professional
- Any Python-compatible editor will work (VS Code, Sublime, etc.)

---

## 🚀 Installation and Execution

### **Step 1: Download the Project**
1. Download the ZIP file from the repository
2. Extract the ZIP to a location of your choice (e.g., `Desktop`, `Documents/Projects`)
3. Navigate to the extracted folder `ADS-Project/`

### **Step 2: Set Up Python Environment (Optional but Recommended)**

**Option A: Using Virtual Environment (Recommended)**
```bash
# Open terminal/command prompt in the project directory
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

**Option B: Use System Python**
Skip this step if you prefer to use your system Python installation.

### **Step 3: Install Required Libraries**

```bash
# Make sure you're in the ADS-Project directory
pip install flask flask-sqlalchemy --break-system-packages
```

**Note**: If you're using a virtual environment, you don't need the `--break-system-packages` flag:
```bash
pip install flask flask-sqlalchemy
```

### **Step 4: Run the Application**

```bash
# Make sure you're in the project directory
python app.py
```

You should see output similar to:
```
 * Running on http://127.0.0.1:5050
 * Running on http://192.168.1.36:5050
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 118-686-977
```

### **Step 5: Access the Application**

Open your web browser and navigate to:
```
http://127.0.0.1:5050
```

Or on the same Wi-Fi network from another device:
```
http://192.168.1.36:5050
```

### **Step 6: Create an Account**

1. Click "Get Started" on the welcome page
2. Enter a unique username and secure password
3. Click "Create Account"
4. You'll be redirected to login
5. Enter your credentials and start using the app!

### **Step 7: Stop the Application**

When you're done:
1. Go back to the terminal/command prompt
2. Press `CTRL+C` to stop the server
3. If using a virtual environment, deactivate it:
   ```bash
   deactivate
   ```

---

## 💡 Usage Guide

### **First-Time Setup**

1. **Register an Account**: Create a unique username and password
2. **Set Your Schedule**: Go to "Schedule" and set your weekly availability
3. **Assign Subject Weights**: Navigate to "Subjects" and prioritize your courses (1=lowest, 6=highest)
4. **Review Allocations**: Check the dashboard to see your assigned study hours per subject

### **Daily Workflow**

1. **Log Study Sessions**: Use "Study Log" to record completed study time
2. **Earn Points**: Automatically earn 1 point per minute studied
3. **Track Progress**: Monitor your statistics on the dashboard
4. **Check Leaderboard**: See your ranking among other users
5. **Find Study Buddies**: Explore compatible study partners in "Study Groups"

### **Understanding the Algorithms**

#### **Leaderboard (Binary Search Tree)**
- Users are inserted into a BST based on points
- Lower points go left, higher points go right
- Reverse in-order traversal produces sorted rankings
- O(log n) average insertion time

#### **Study Groups (Graph with BFS/DFS)**
- Each user is a node in the graph
- Edges connect users with 30%+ compatibility
- Compatibility based on shared subjects and point similarity
- BFS explores level-by-level, DFS explores depth-first
- O(V + E) time complexity for traversal

---

## 🎓 Default Subjects

The application comes pre-configured with six subjects (you can modify these in `app.py`):

1. ALGORITHMS & DATA STRUCTURES
2. MATHEMATICS FOR DATA MANAGEMENT AND ANALYSIS
3. PROBABILITY & STATISTICS FOR DATA MANAGEMENT AND ANALYSIS
4. PROGRAMMING FOR DATA MANAGEMENT & ANALYSIS
5. TECHNOLOGY WITH IMPACT
6. TIME SERIES ANALYSIS

---

## 🔄 Further Improvements

### **Potential Enhancements**

1. **Authentication & Security**
   - Password hashing (bcrypt or Argon2)
   - Email verification
   - Password reset functionality
   - Session timeout and CSRF protection

2. **Study Features**
   - Pomodoro timer integration
   - Study reminders and notifications
   - Goal setting with deadlines
   - Study streaks and daily targets
   - Export study logs to CSV/PDF

3. **Social Features**
   - Real messaging system between study buddies
   - Study group creation and management
   - Shared study resources
   - Collaborative study sessions

4. **Analytics & Insights**
   - Detailed study time charts (Chart.js or Plotly)
   - Productivity patterns analysis
   - Subject performance predictions
   - Personalized study recommendations

5. **Customization**
   - Custom subject creation
   - Adjustable points system
   - Theme customization (light/dark modes)
   - Configurable notification preferences

6. **Data Structures & Algorithms**
   - Implement AVL or Red-Black Tree for balanced BST
   - Add Dijkstra's algorithm for optimal study paths
   - Use Priority Queue for upcoming deadlines
   - Implement caching with LRU (Least Recently Used)

7. **Mobile Optimization**
   - Responsive design improvements
   - Progressive Web App (PWA) functionality
   - Touch-friendly interfaces
   - Offline functionality

8. **Database & Performance**
   - Migration to PostgreSQL or MySQL for production
   - Database indexing for faster queries
   - Query optimization
   - Caching layer (Redis)

9. **Testing & Quality**
   - Unit tests with pytest
   - Integration tests
   - Load testing
   - Accessibility improvements (WCAG compliance)

10. **Deployment**
    - Containerization with Docker
    - Cloud deployment (Heroku, AWS, DigitalOcean)
    - CI/CD pipeline
    - Environment configuration management

---

## 📚 Bibliography/Webography

### **Documentation & References**

- **Flask Documentation**: https://flask.palletsprojects.com/
- **Flask-SQLAlchemy Documentation**: https://flask-sqlalchemy.palletsprojects.com/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **Python Official Documentation**: https://docs.python.org/3/
- **SQLite Documentation**: https://www.sqlite.org/docs.html

### **Learning Resources**

- **Data Structures and Algorithms**
  - Introduction to Algorithms (CLRS) - Cormen, Leiserson, Rivest, Stein
  - Grokking Algorithms - Aditya Bhargava
  - VisuAlgo: https://visualgo.net/ (Algorithm visualization)

- **Web Development**
  - MDN Web Docs: https://developer.mozilla.org/
  - W3Schools: https://www.w3schools.com/
  - CSS-Tricks: https://css-tricks.com/

- **Flask & Python**
  - Real Python Flask Tutorials: https://realpython.com/tutorials/flask/
  - Flask Mega-Tutorial by Miguel Grinberg: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
  - Python Package Index (PyPI): https://pypi.org/

### **Design Inspiration**

- **UI/UX Design**
  - Dribbble: https://dribbble.com/
  - Behance: https://www.behance.net/
  - Apple Human Interface Guidelines: https://developer.apple.com/design/

### **Tools & Technologies**

- **PyCharm IDE**: https://www.jetbrains.com/pycharm/
- **Git & GitHub**: https://docs.github.com/
- **jQuery**: https://jquery.com/

---

## 👥 Credits

### **Development Team**

- **rmetchkarovaieu2024-bit** - Lead Developer & Database Design,  Algorithm Implementation & UI/UX
- **alp47** - Developer

### **Course Information**

- **Course**: BDBA25 - Algorithms & Data Structures (ADS)
- **Institution**: IEU Business School
- **Academic Year**: 2025-2026
- **Project**: Smart Study Planner (Final Project)

### **Acknowledgments**

Special thanks to:
- Course instructors for guidance on data structures and algorithms
- Flask community for extensive documentation
- Open-source contributors for inspiration and best practices
- The team behind the scenes that helped develop the project 

---

## 📄 License

© 2025 Smart Study Planner. All rights reserved.

This project was developed as part of an academic assignment for educational purposes.

---

## 🐛 Known Issues

1. **Database Migration**: No migration tool implemented; manual schema updates required
2. **Password Security**: Passwords stored in plain text (not production-ready)
3. **Session Management**: Basic session handling without timeout
4. **Input Validation**: Limited server-side validation on some forms
5. **Error Handling**: Generic error messages in some cases

---

## 📞 Support & Contact

For questions, issues, or suggestions:

- **GitHub Issues**: Open an issue on the repository
- **Email**: Contact through IEU Business School portal
- **Documentation**: Refer to this README and inline code comments

  
- PLEASE DON'T CONTACT US, we have no idea what we are doing 

---

## 🚀 Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Downloaded and extracted project ZIP
- [ ] Opened terminal/command prompt in project directory
- [ ] Installed Flask and Flask-SQLAlchemy
- [ ] Ran `python app.py`
- [ ] Opened browser to `http://127.0.0.1:5050`
- [ ] Created user account
- [ ] Set schedule and subject weights
- [ ] Logged first study session
- [ ] Explored leaderboard and study groups

**Enjoy planning your studies smarter! 📚✨**
