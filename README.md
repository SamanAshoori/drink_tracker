# Personal Drink Tracker

A full-stack web application for tracking personal caffeine consumption. The system allows users to manage a library of beverage brands and drinks, log consumption events, and view historical data.

## Architecture

* **Frontend:** Svelte (Vite build tool)
* **Backend:** Python FastAPI
* **Database:** Supabase (PostgreSQL)
* **Communication:** REST API via HTTP

## Prerequisites

* Python 3.8+
* Node.js 16+
* Supabase Account

## Project Structure

* `/backend` - FastAPI application, database schemas, and logic.
* `/frontend` - Svelte UI and API integration.

## Installation and Setup

### 1. Database Configuration
1.  Create a project in Supabase.
2.  Navigate to the SQL Editor.
3.  Execute the schema definitions for `brands`, `drinks`, and `consumptions` tables.
4.  Note your `Project URL` and `anon/public` API Key from Project Settings > API.

### 2. Backend Setup
Navigate to the backend directory:
```bash
cd backend
```

Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate
# Windows: venv\Scripts\activate
```

Install dependencies:
```bash
pip install fastapi uvicorn supabase python-dotenv pydantic
```

Create a `.env` file in the `/backend` directory:
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### 3. Frontend Setup
Navigate to the frontend directory:
```bash
cd ../frontend
```

Install Node dependencies:
```bash
npm install
```

## Usage

### Starting the Application
You must run the backend and frontend in separate terminal instances.

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```
The API will be available at http://127.0.0.1:8000.
Interactive API documentation is available at http://127.0.0.1:8000/docs.

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```
The UI will be available at http://localhost:5173.

## Features
* **Brand Management:** Database seeded with initial brands.
* **Drink Library:** Create new drinks with calculated caffeine content (input as mg/100ml, stored as total mg).
* **Logging:** Record consumption events.
* **History:** View chronological list of consumed beverages.
