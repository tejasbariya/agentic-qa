# Testing SentinelQA Step-by-Step

This guide provides step-by-step instructions on how to test the application locally.

## Step 1: Set up the Environment Variables
1. Make sure you have a `.env` file at the root of the project (you can copy from `.env.example` if available).
2. For testing, default values in `docker-compose.yml` are mostly sufficient.

## Step 2: Build and Run the Stack
Run the following command in the root directory where `docker-compose.yml` is located:
```bash
docker compose up --build
```
This will start:
- Postgres (Database)
- Redis (Message broker for Celery)
- ChromaDB (Vector database)
- Backend (FastAPI on port 8080)
- Celery Worker (Background tasks)
- Frontend (React on port 3000)

## Step 3: Run Database Migrations
Before the backend can work properly, the database tables need to be created. You can apply the migrations using Alembic from within the backend container:
```bash
# Get the backend container ID
docker ps

# Execute the migration script inside the backend container
docker exec -it <backend_container_id> alembic upgrade head
```

## Step 4: Access the Frontend Dashboard
1. Open your browser and navigate to `http://localhost:3000`.
2. You should see the React frontend.
3. Test the UI by navigating between Dashboard, Projects, Executions, and Agents pages.

## Step 5: Test the API Endpoints
1. The backend API is running on `http://localhost:8080`.
2. Access the interactive API documentation at:
   `http://localhost:8080/docs` (Swagger UI) or `http://localhost:8080/redoc`
3. Try calling the `/api/v1/users/` endpoint to create a user, and then `/api/v1/auth/login` to retrieve an authentication token.

## Step 6: Test Real-time WebSockets
Navigate to the Executions page on the frontend dashboard. The indicator next to the "Executions" title should turn green (Connected) if the Socket.io client successfully connects to the backend WebSocket at `ws://localhost:8080/ws/dashboard`.

---

# Where to Add New APIs

If you want to add new backend APIs to the platform, follow this pattern to maintain Clean Architecture:

1. **Define the Schema (Pydantic Models)**: 
   Add your request and response models in a new file under `server/app/schemas/` (e.g., `server/app/schemas/my_feature.py`).

2. **Define the Database Model (SQLAlchemy)**: 
   Add your database structure in a new file under `server/app/models/` (e.g., `server/app/models/my_feature.py`). Remember to import it in `server/app/models/__init__.py`.

3. **Create the Endpoint Router**: 
   Create a new file in the endpoints directory: `server/app/api/api_v1/endpoints/my_feature.py` and define your `APIRouter` with the specific routes (`@router.get`, `@router.post`).

4. **Register the Router**: 
   Open `server/app/api/api_v1/api.py` and include your new router:
   ```python
   from app.api.api_v1.endpoints import my_feature
   
   # ... existing code ...
   
   api_router.include_router(my_feature.router, prefix="/my-feature", tags=["my-feature"])
   ```
