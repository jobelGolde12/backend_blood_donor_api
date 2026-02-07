# Command to Run FastAPI Application

## Start the FastAPI Server

### Option 1: With virtual environment activation
```bash
source .venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 2: Direct execution
```bash
.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### If port 8000 is already in use:
```bash
# Kill existing uvicorn processes
pkill -f uvicorn

# Then run the command again
source .venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Access Points

- **FastAPI Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Adminer Web UI**: http://localhost:8082
  - System: PostgreSQL
  - Server: postgres
  - Username: blood_donor_user
  - Password: blood_donor_pass
  - Database: blood_donor_db

## Notes

- The `--reload` flag enables auto-reloading when code changes
- The server runs on all interfaces (`0.0.0.0`) for accessibility
- Make sure PostgreSQL and Adminer are running before starting the API