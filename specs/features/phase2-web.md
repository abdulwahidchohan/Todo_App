# Phase II: Web Todo Application Specification

## Overview
This specification defines the requirements for a Web-based Todo Application that provides task management functionality through a web interface. The application will be built using a modern tech stack with FastAPI backend, Next.js frontend, Neon Postgres database, and Better Auth for authentication.

## Scope
### In Scope
- Web-based user interface using Next.js 16+ with App Router
- RESTful API endpoints for task management
- Authentication and authorization using Better Auth with JWT
- Database persistence using Neon Serverless Postgres with SQLModel ORM
- Full CRUD operations for tasks
- Responsive design for desktop and mobile devices

### Out of Scope
- Mobile native applications (iOS/Android)
- Desktop native applications
- Email notifications
- Advanced task features like due dates, categories, or priorities
- File attachments
- Collaborative features

## Tech Stack
- **Backend**: Python FastAPI
- **Database**: Neon Serverless Postgres
- **ORM**: SQLModel
- **Frontend**: Next.js 16+ (App Router)
- **Authentication**: Better Auth with JWT

## Database Schema

### Task Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'incomplete',
    user_id UUID NOT NULL,  -- Foreign key to users table (from Better Auth)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Constraints
- `title` cannot be empty
- `status` must be either 'incomplete' or 'complete'
- `user_id` references the user from Better Auth

## API Endpoints

### GET /api/tasks
**Description**: Retrieve all tasks for the authenticated user
**Authentication**: Required (JWT in Authorization header)
**Response**:
- 200: Array of task objects
```json
[
  {
    "id": 1,
    "title": "Sample Task",
    "description": "This is a sample task",
    "status": "incomplete",
    "user_id": "user-uuid",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
]
```
- 401: Unauthorized if JWT is invalid or missing

### POST /api/tasks
**Description**: Create a new task for the authenticated user
**Authentication**: Required (JWT in Authorization header)
**Request Body**:
```json
{
  "title": "New Task",
  "description": "Task description (optional)"
}
```
**Response**:
- 201: Created task object
```json
{
  "id": 1,
  "title": "New Task",
  "description": "Task description (optional)",
  "status": "incomplete",
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```
- 400: Bad request if title is missing or empty
- 401: Unauthorized if JWT is invalid or missing

### PUT /api/tasks/{id}
**Description**: Update an existing task for the authenticated user
**Authentication**: Required (JWT in Authorization header)
**Path Parameter**: `id` - Task ID to update
**Request Body**:
```json
{
  "title": "Updated Task Title",
  "description": "Updated description"
}
```
**Response**:
- 200: Updated task object
- 400: Bad request if title is empty
- 401: Unauthorized if JWT is invalid or missing
- 404: Task not found

### DELETE /api/tasks/{id}
**Description**: Delete a task for the authenticated user
**Authentication**: Required (JWT in Authorization header)
**Path Parameter**: `id` - Task ID to delete
**Response**:
- 204: No content (task deleted successfully)
- 401: Unauthorized if JWT is invalid or missing
- 404: Task not found

### PATCH /api/tasks/{id}/complete
**Description**: Toggle the completion status of a task
**Authentication**: Required (JWT in Authorization header)
**Path Parameter**: `id` - Task ID to update
**Response**:
- 200: Updated task object with toggled status
- 401: Unauthorized if JWT is invalid or missing
- 404: Task not found

## Frontend Requirements

### Pages
1. **Home Page** (`/`): Displays the task list and provides navigation
2. **Task List Page** (`/tasks`): Shows all tasks with filtering and sorting options
3. **Add Task Page** (`/tasks/add`): Form to create new tasks
4. **Edit Task Page** (`/tasks/[id]/edit`): Form to update existing tasks
5. **Authentication Pages** (`/auth/*`): Login, register, and profile management

### Components
1. **Task List Component**: Displays tasks in a responsive grid/list
2. **Task Item Component**: Individual task display with status toggle
3. **Task Form Component**: Reusable form for creating/updating tasks
4. **Navigation Component**: Header with user authentication status
5. **Authentication Component**: Login/logout functionality

### User Experience
- Responsive design that works on mobile, tablet, and desktop
- Real-time updates when tasks are added, updated, or deleted
- Loading states during API requests
- Error handling and user feedback
- Form validation with clear error messages

## Authentication Requirements

### User Registration
- Email and password registration
- Email verification (if required by Better Auth)
- Password strength requirements

### User Login
- Email and password authentication
- JWT token storage in secure HTTP-only cookies
- Automatic token refresh

### Protected Routes
- All task-related pages require authentication
- Redirect unauthenticated users to login page
- Proper error handling for expired/invalid tokens

## Error Handling
- API errors should return appropriate HTTP status codes
- Frontend should display user-friendly error messages
- Network error handling with retry mechanisms
- Validation errors should be displayed near the relevant form fields

## Performance Requirements
- API responses should be under 500ms for 95% of requests
- Frontend should load initial page in under 3 seconds
- Efficient data fetching and caching strategies
- Optimized database queries with proper indexing

## Security Requirements
- All API endpoints require authentication except public routes
- JWT tokens should be properly validated and have appropriate expiration times
- Input validation and sanitization to prevent injection attacks
- Secure HTTP headers and CORS configuration
- HTTPS enforcement in production

## Deployment Requirements
- Backend API should be deployable to platforms supporting Python applications
- Frontend should be deployable to platforms supporting Next.js applications
- Database should be configured with Neon Serverless Postgres
- Environment variables for configuration
- Proper logging and monitoring setup

## Acceptance Criteria
1. All API endpoints function as specified with proper authentication
2. Database schema is implemented with SQLModel ORM
3. Frontend provides a responsive and intuitive user interface
4. Authentication system works with Better Auth and JWT
5. All CRUD operations are available through both API and UI
6. Error handling is implemented at both API and UI levels
7. Application is deployable with the specified tech stack