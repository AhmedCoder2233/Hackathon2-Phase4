# Quickstart Guide: JWT Authentication & User ID Retrieval for ChatKit Endpoint

**Date**: December 14, 2025
**Feature**: `006-jwt-auth`
**Spec**: `specs/006-jwt-auth/spec.md`

This guide provides a quick overview of how to set up and test the JWT authentication and user ID retrieval feature for the `/support/chatkit` endpoint.

## 1. Install Required Dependencies

Ensure you have Python 3.11+ installed. Navigate to the `backend/` directory and install the necessary Python packages:

```bash
cd backend
pip install python-jose[cryptography] sqlalchemy psycopg2-binary
# Ensure other project dependencies are also installed, e.g., FastAPI, Uvicorn
pip install -e .
```

## 2. Environment Variables

Create a `.env` file in the `backend/` directory or set the following environment variables:

```env
DATABASE_URL=postgresql://user:password@neondb-host/database
BETTER_AUTH_SECRET=your_better_auth_secret_key
BETTER_AUTH_ISSUER=your_issuer # Optional, if Better Auth uses an issuer
```

*   `DATABASE_URL`: Connection string for your Neon Serverless PostgreSQL database.
*   `BETTER_AUTH_SECRET`: The secret key used by your Better Auth instance for signing JWT tokens.
*   `BETTER_AUTH_ISSUER`: (Optional) The issuer claim expected in the JWT token.

## 3. Database Setup

This feature requires `User` and `Session` tables in your PostgreSQL database.

*   **Models**:
    *   `backend/app/database.py`: Will contain SQLAlchemy models for `User` and `Session` and define their relationship.
*   **Connection**: Ensure `backend/app/database.py` is configured to connect to your database using the `DATABASE_URL`.
*   **Migrations**: You may need to run database migration scripts (e.g., using Alembic) to create these tables if they don't already exist. (Specific migration steps are outside the scope of this quickstart).

## 4. How to Run the FastAPI Application

From the `backend/` directory, start the FastAPI application (assuming `main.py` is the entry point):

```bash
cd backend
uvicorn app.main:app --reload
```

The API will typically be accessible at `http://127.0.0.1:8000`.

## 5. Quick Test

To quickly test the JWT authentication:

1.  **Obtain a valid JWT token**: This token should be issued by your Better Auth instance and contain an `email` claim corresponding to a user in your database.
2.  **Send a POST request to `/support/chatkit`**: Use a tool like `curl` or Postman.

    ```bash
    curl -X POST "http://127.0.0.1:8000/support/chatkit" \
      -H "Authorization: Bearer YOUR_VALID_JWT_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{ "message": "Hello" }'
    ```

**Expected Behavior**:

*   **Valid Token & User**: The request should be processed by the ChatKit service, and you should see the `user_id` printed to the console (as per implementation details).
*   **Invalid/Expired Token**: You should receive a `401 Unauthorized` response with `{"error": "Invalid or expired JWT token", "status": 401}`.
*   **User Not Found**: You should receive a `404 Not Found` response with `{"error": "User not found with provided email", "status": 404}`.
*   **No Active Sessions**: You should receive a `404 Not Found` response with `{"error": "No active sessions found for user", "status": 404}`.
