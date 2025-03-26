# Gen-AI Data Profiling

This project consists of a frontend and a backend. Follow the instructions below to set up and run the application.

## Prerequisites
- **Node.js** (for frontend) - Download from [nodejs.org](https://nodejs.org/)
- **Python 3.10+** (for backend) - Download from [python.org](https://www.python.org/)
- **pip** (Python package manager)

## Installation and Setup

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/ranaDherya/WF-hackathon
cd WF-hackathon
```

### 2️⃣ Backend Setup
Navigate to the backend folder and install dependencies:
```sh
cd backend
pip install -r requirements.txt
```

Add API keys to .env file

#### Run Backend Server
```sh
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3️⃣ Frontend Setup
Navigate to the frontend folder and install dependencies:
```sh
cd ../frontend
npm install
```

#### Run Frontend Server
```sh
npm start
```

## Running the Project
Once both frontend and backend servers are running:
- Open `http://localhost:3000/` to access the frontend.
- The backend API is accessible at `http://localhost:8000/`.

