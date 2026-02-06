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
