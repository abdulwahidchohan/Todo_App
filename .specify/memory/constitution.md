# Todo App - Project Memory & Constitution

This file serves as the authoritative memory for the Todo App project, capturing architecture, conventions, patterns, and key decisions for AI assistants working on this codebase.

## Project Overview

**Name**: Todo App  
**Purpose**: A full-stack task management application that evolves from console app to AI-powered web application  
**Current Phase**: Phase II - Full-Stack Web Application  
**Development Approach**: Spec-Driven Development (SDD)

## Tech Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **ORM**: SQLModel 0.0.16
- **Language**: Python 3.14.0
- **Database**: 
  - Local: SQLite (`sqlite:///./todo_app.db`)
  - Production: PostgreSQL (Neon Serverless)
- **Server**: Uvicorn
- **Dependencies**: See `requirements.txt`

### Frontend
- **Framework**: Next.js 14.0.4 (App Router)
- **Language**: TypeScript 5.3.3
- **Styling**: Tailwind CSS 3.3.0
- **UI Features**: 
  - Gradient color scheme (purple/indigo)
  - Glassmorphism effects (backdrop blur)
  - Smooth animations (fade-in, slide-up)
  - Modern, attractive design

### Development Tools
- **Package Manager**: npm (frontend), pip (backend)
- **Containerization**: Docker & docker-compose
- **Deployment**: Kubernetes (k8s/ directory)

## Project Structure

```
Todo_App/
├── .specify/              # AI assistant memory and templates
│   └── memory/
│       └── constitution.md  # This file
├── app/                   # Next.js App Router pages
│   ├── layout.tsx        # Root layout
│   ├── page.tsx          # Home page (main todo interface)
│   └── globals.css       # Global styles and Tailwind directives
├── backend/               # FastAPI backend
│   ├── main.py           # FastAPI app entry point
│   ├── models.py         # SQLModel database models
│   ├── database.py       # Database connection and session management
│   ├── todo_logic.py     # Business logic (CRUD operations)
│   ├── mcp_server.py     # MCP server for AI tools
│   └── todo_app.db       # SQLite database (local dev)
├── components/            # React components
│   └── ChatInterface.tsx # AI chat interface component
├── lib/                   # Utility libraries
│   └── api.ts            # API client for backend communication
├── specs/                 # Specifications (Spec-Driven Development)
│   ├── features/         # Feature specifications
│   └── phase1-architecture.md
├── types.ts              # TypeScript type definitions
├── package.json          # Frontend dependencies
├── requirements.txt      # Backend dependencies
├── tailwind.config.js    # Tailwind CSS configuration
├── postcss.config.js     # PostCSS configuration
├── next.config.js        # Next.js configuration
└── docker-compose.yml    # Docker Compose configuration

```

## Architecture

### Backend Architecture

**Layered Architecture**:
1. **API Layer** (`backend/main.py`)
   - FastAPI routes and endpoints
   - Request validation
   - Response formatting
   - Authentication middleware (currently mock)

2. **Business Logic Layer** (`backend/todo_logic.py`)
   - CRUD operations
   - Task management logic
   - Reusable functions for API and MCP server

3. **Data Layer** (`backend/models.py`, `backend/database.py`)
   - SQLModel ORM models
   - Database connection management
   - Session handling

### Frontend Architecture

**Component Structure**:
- **Pages**: `app/page.tsx` - Main application page
- **Components**: `components/ChatInterface.tsx` - Reusable UI components
- **API Client**: `lib/api.ts` - Centralized API communication
- **Types**: `types.ts` - Shared TypeScript interfaces

**Styling Approach**:
- Tailwind CSS utility classes
- Custom gradients and animations
- Glassmorphism effects (backdrop-blur)
- Responsive design (mobile-first)

## Database Schema

### Task Table

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- SQLite
    -- id SERIAL PRIMARY KEY,              -- PostgreSQL
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'incomplete',
    user_id VARCHAR(255) NOT NULL,  -- UUID as string
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Constraints**:
- `title`: Required, min 1 character, max 255 characters
- `status`: Must be either 'incomplete' or 'complete'
- `description`: Optional, max 1000 characters
- `user_id`: Required (currently using mock UUID)

**Model Classes**:
- `Task` (table=True): Database model
- `TaskCreate`: Input model for creating tasks
- `TaskUpdate`: Input model for updating tasks
- `TaskPublic`: Output model for API responses

## API Endpoints

Base URL: `http://localhost:8000` (development)

### Task Endpoints

#### GET `/api/tasks`
- **Description**: Retrieve all tasks for authenticated user
- **Authentication**: Required (currently mock)
- **Response**: `200 OK` - Array of `TaskPublic` objects
- **Logic**: `get_tasks_logic()` in `todo_logic.py`

#### POST `/api/tasks`
- **Description**: Create a new task
- **Authentication**: Required
- **Request Body**: `TaskCreate` (title, optional description)
- **Response**: `201 Created` - `TaskPublic` object
- **Logic**: `create_task_logic()` in `todo_logic.py`

#### PUT `/api/tasks/{id}`
- **Description**: Update an existing task
- **Authentication**: Required
- **Path Parameters**: `id` (integer)
- **Request Body**: `TaskUpdate` (optional title, optional description)
- **Response**: `200 OK` - `TaskPublic` object
- **Error**: `404 Not Found` if task doesn't exist
- **Logic**: `update_task_logic()` in `todo_logic.py`

#### DELETE `/api/tasks/{id}`
- **Description**: Delete a task
- **Authentication**: Required
- **Path Parameters**: `id` (integer)
- **Response**: `204 No Content`
- **Error**: `404 Not Found` if task doesn't exist
- **Logic**: `delete_task_logic()` in `todo_logic.py`

#### PATCH `/api/tasks/{id}/complete`
- **Description**: Toggle task completion status
- **Authentication**: Required
- **Path Parameters**: `id` (integer)
- **Response**: `200 OK` - `TaskPublic` object
- **Error**: `404 Not Found` if task doesn't exist
- **Logic**: `toggle_task_status_logic()` in `todo_logic.py`

### Chat Endpoint

#### POST `/api/chat`
- **Description**: Chat with AI assistant (MCP agent)
- **Request Body**: `{ message: string, userId?: string }`
- **Response**: `200 OK` - `{ response: string }`
- **Status**: Currently placeholder/simulation

### Root Endpoint

#### GET `/`
- **Description**: API welcome message
- **Response**: `200 OK` - `{ "message": "Welcome to the Todo API" }`

## Development Workflow

### Spec-Driven Development (SDD)

**Mandatory Workflow**:
1. **Specify**: Document requirements in `specs/features/`
2. **Plan**: Create architecture plan in `specs/`
3. **Tasks**: Break down into tasks in `specs/`
4. **Implement**: Write code in `/backend` or `/app`

**Rules**:
- NEVER write code without a corresponding specification
- All code must trace back to a documented requirement
- Check `specs/features/` before implementing any feature
- See `AGENTS.md` for full SDD guidelines

### Running the Application

#### Backend
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
- Runs on `http://localhost:8000`
- Auto-reload on file changes
- SQLite database: `backend/todo_app.db`

#### Frontend
```bash
npm run dev
```
- Runs on `http://localhost:3000`
- Hot module replacement enabled
- Uses `NEXT_PUBLIC_API_URL` env var (defaults to `http://localhost:8000`)

#### Docker Compose
```bash
docker-compose up
```
- Runs all services (PostgreSQL, backend, frontend)
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- Database: PostgreSQL on port 5432

## Code Conventions

### Python (Backend)

**Style**: Follow PEP 8
- Use type hints
- Docstrings for all functions and classes
- SQLModel for database models
- Business logic separated in `todo_logic.py`

**File Organization**:
- `main.py`: FastAPI routes only
- `models.py`: SQLModel models only
- `todo_logic.py`: Business logic functions
- `database.py`: Database configuration

**Naming Conventions**:
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`

### TypeScript (Frontend)

**Style**: Follow TypeScript best practices
- Use interfaces for types (`types.ts`)
- Client components: `'use client'` directive
- Server components: Default (when possible)

**File Organization**:
- `app/`: Pages and layouts (Next.js App Router)
- `components/`: Reusable React components
- `lib/`: Utility functions and API clients
- `types.ts`: Shared TypeScript interfaces

**Naming Conventions**:
- Components: `PascalCase`
- Functions: `camelCase`
- Types/Interfaces: `PascalCase`
- Files: `kebab-case.tsx` or `PascalCase.tsx`

### CSS/Styling

**Approach**: Tailwind CSS utility classes
- No inline styles (except dynamic values)
- Custom utilities in `globals.css`
- Responsive design with Tailwind breakpoints
- Color scheme: Purple/Indigo gradients

**Current Design Theme**:
- Primary colors: Purple (#9333ea) to Indigo (#4f46e5)
- Background: Gradient from indigo-50 to purple-50
- Cards: White with backdrop-blur (glassmorphism)
- Shadows: Large, soft shadows for depth

## Key Patterns

### Backend Patterns

1. **Dependency Injection**
   - FastAPI `Depends()` for database sessions
   - `get_session()` context manager from `database.py`

2. **Separation of Concerns**
   - Routes in `main.py`
   - Business logic in `todo_logic.py`
   - Models in `models.py`

3. **Model Inheritance**
   - `TaskBase`: Common fields
   - `Task`: Database table
   - `TaskCreate`/`TaskUpdate`/`TaskPublic`: API models

### Frontend Patterns

1. **API Client Pattern**
   - All API calls through `lib/api.ts`
   - Centralized error handling
   - Type-safe with TypeScript interfaces

2. **Component Composition**
   - Page components in `app/`
   - Reusable components in `components/`
   - Shared types in `types.ts`

3. **State Management**
   - React hooks (`useState`, `useEffect`)
   - Local component state
   - API calls on mount/events

## Authentication (Current State)

**Status**: Mock implementation
- Current user ID: `"mock-user-uuid"` (hardcoded)
- `get_current_user_id()` in `main.py` returns mock ID
- Future: Better Auth with JWT tokens
- Future: Real user authentication and authorization

## Environment Variables

### Backend
- `DATABASE_URL`: Database connection string
  - Default: `sqlite:///./todo_app.db` (SQLite)
  - Production: PostgreSQL connection string

### Frontend
- `NEXT_PUBLIC_API_URL`: Backend API URL
  - Default: `http://localhost:8000`
  - Used in `lib/api.ts`

## Testing Strategy

**Current State**: Not yet implemented
**Planned**:
- Unit tests for business logic
- Integration tests for API endpoints
- Frontend component tests
- E2E tests for critical flows

## Deployment

**Configuration Files**:
- `docker-compose.yml`: Local development with Docker
- `k8s/`: Kubernetes deployment manifests
  - `backend-deployment.yaml`
  - `frontend-deployment.yaml`
  - `postgres-deployment.yaml`
  - `ingress.yaml`

**Production Considerations**:
- Use PostgreSQL (not SQLite)
- Environment variables for configuration
- HTTPS enforcement
- Proper authentication implementation

## Important Notes

1. **Database**: SQLite for local dev, PostgreSQL for production
2. **Authentication**: Currently mocked, needs real implementation
3. **MCP Server**: `backend/mcp_server.py` exists but not fully integrated
4. **Chat Interface**: Frontend has chat UI, backend has placeholder endpoint
5. **Spec-Driven**: Always check `specs/` before making changes
6. **File Structure**: Frontend files moved from `frontend/` to root (Next.js App Router requirement)

## Quick Reference

**Backend Entry Point**: `backend/main.py`  
**Frontend Entry Point**: `app/page.tsx`  
**API Base URL**: `http://localhost:8000`  
**Frontend URL**: `http://localhost:3000`  
**Database File**: `backend/todo_app.db` (SQLite)  
**Specifications**: `specs/features/`  
**Business Logic**: `backend/todo_logic.py`  
**API Client**: `lib/api.ts`  
**Type Definitions**: `types.ts` (frontend), `backend/models.py` (backend)

---

*Last Updated: 2025-01-27*  
*This file should be updated when significant architectural changes are made.*
