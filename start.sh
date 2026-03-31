#!/bin/bash

# Start backend
cd backend
source venv/bin/activate
uvicorn main:app --reload &
BACKEND_PID=$!

# Start frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Kill both on exit
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT

wait
