# Lightweight Feedback System

A simple, lightweight web-based feedback system with role-based login for **Managers** and **Employees**.  
Managers can create and review feedbacks. Employees can view and acknowledge their feedback.

---

## 🔧 Tech Stack

- **Backend**: Django, Django REST Framework  
- **Frontend**: React.js  
- **Database**: SQLite (can be switched to PostgreSQL/MySQL)  
- **Auth**: Token-based Authentication (DRF Token)  
- **Deployment-ready**: Docker  

---

## 📁 Folder Structure

<pre>
lightweightfeedbacksystem/
│
├── feedback_system_backend/          # Django backend
│   ├── manage.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .gitignore
│   ├── feedback/                     # Django app
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── ...
│   └── feedback_system/              # Django project
│       ├── settings.py
│       ├── urls.py
│       └── ...
│
├── frontend/                         # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.js
│   │   │   ├── SignUp.js
│   │   │   ├── ManagerDashboard.js
│   │   │   ├── EmployeeDashboard.js
│   │   │   ├── FeedbackForm.js
│   │   │   ├── CreateFeedbackPage.js
│   │   │   ├── FeedbackHistoryPage.js
│   │   │   ├── EditFeedbackPage.js
│   │   │   └── ...
│   │   ├── pages/
│   │   │   ├── Login.css
│   │   │   ├── SignUp.css
│   │   │   ├── ManagerDashboard.css
│   │   │   └── ...
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
│
└── README.md                         # This file
</pre>

---

## 🚀 Features

### 👨‍💼 Manager:
- Login/Signup  
- View all employees  
- Create feedback  
- View and edit past feedbacks  
- Dashboard with feedback stats & sentiment graph  

### 👩‍💼 Employee:
- Login/Signup  
- View personal feedbacks  
- Acknowledge feedback  

---

## 🔑 Login Info

- Username format:  
  - Managers: `name@manager`  
  - Employees: `name@employee`  

---

## ⚙️ Backend Setup

<pre>
cd feedback_system_backend
python -m venv venv
venv\Scripts\activate      # On Windows
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Run development server
python manage.py runserver
</pre>

---

## ⚙️ Frontend Setup

<pre>
cd frontend
npm install
npm start
</pre>

---

## 🐳 Running with Docker (Backend Only)

### 1. Create `Dockerfile` inside `feedback_system_backend/`:

<pre>
# Use official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
</pre>

### 2. Build and run Docker:

<pre>
cd feedback_system_backend
docker build -t feedback-backend .
docker run -p 8000:8000 feedback-backend
</pre>

---

## ✅ API Endpoints

| Method | Endpoint                          | Description                    |
|--------|-----------------------------------|--------------------------------|
| POST   | `/login/`                         | Login for manager/employee     |
| POST   | `/signup/`                        | User registration              |
| GET    | `/feedbacks/`                     | List feedbacks (manager)       |
| POST   | `/feedbacks/`                     | Create feedback (manager only) |
| PATCH  | `/feedbacks/<id>/acknowledge/`    | Acknowledge by employee        |
| GET    | `/feedbacks/my-feedbacks/`        | List own feedbacks (employee)  |

---

