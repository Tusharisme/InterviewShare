# InterviewShare 🎓

**InterviewShare** is a full-stack web application designed to help students share and browse interview experiences. Built with Flask and Vue.js, it offers a secure and interactive platform for placement preparation.

## 🌟 Features
- **User Authentication**: Secure Login and Registration (Flask-Security).
- **Share Experiences**: Post detailed interview experiences (Company, Role, Description).
- **Browse Feed**: View experiences shared by other students.
- **Manage Content**: Delete your own posts.
- **Responsive Design**: Modern UI built with Vue.js.

## 🛠 Tech Stack
- **Backend**: Flask, Flask-SQLAlchemy, Flask-Security, SQLite.
- **Frontend**: Vue.js 3, Vite, Axios, Vue Router.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`.

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   The application will be available at `http://localhost:5173`.

## 📝 API Documentation
- **POST /register**: Register a new user.
- **POST /login**: Authenticate user and receive token.
- **GET /api/experiences**: List all experiences.
- **POST /api/experiences**: Create a new experience (Auth required).
- **DELETE /api/experiences/<id>**: Delete an experience (Auth required).

## 📄 License
MIT
