# Feature Specification: JWT Authentication & User ID Retrieval for ChatKit Endpoint

**Feature Branch**: `006-jwt-auth`  
**Created**: December 14, 2025  
**Status**: Draft  
**Input**: User description: "# JWT Authentication & User ID Retrieval - Implementation Specification ## Overview Implement JWT token validation and user identification system for the `/support/chatkit` endpoint in FastAPI backend. ## Objective When a request hits `/support/chatkit`, validate the Better Auth JWT token, extract user information, and retrieve the associated user_id from the sessions table. ## Current State - **File Location**: `backend/app/main.py` - **Endpoint**: `POST /support/chatkit` - **Current Behavior**: JWT token is received in Authorization header as `Bearer 0fOyRVonMqRyD20kP9Qi` but not validated - **Token Format**: Better Auth JWT token (e.g., `0fOyRVonMqRyD20kP9Qi`) ## Database Schema ### User Table (`public.user`) ```sql Columns: - id (TEXT, PRIMARY KEY) - name (TEXT) - email (TEXT, UNIQUE, NOT NULL) - emailVerified (BOOLEAN, DEFAULT false) - image (TEXT) - createdAt (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP) - updatedAt (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP) - sessions (RELATIONSHIP to Session table) ``` ### Session Table (`public.session`) ```sql Columns: - id (TEXT, PRIMARY KEY) - userId (TEXT, FOREIGN KEY -> public.user.id) - expiresAt (TIMESTAMP) - token (TEXT) - ipAddress (TEXT) - userAgent (TEXT) ``` **Relationship**: User table has a `sessions` column that relates to the Session table via `userId` ## Implementation Requirements ### 1. JWT Token Validation - **Input**: JWT token from `Authorization` header (format: `Bearer <token>`) - **Process**: - Extract token from header - Validate JWT token using Better Auth configuration - Decode token to extract payload (including email) - **Output**: Decoded payload with user email ### 2. Database Query Flow **Step 1**: Extract email from JWT payload ```python email = decoded_token['email'] # or appropriate field from Better Auth JWT ``` **Step 2**: Query User table by email ```sql SELECT * FROM public.user WHERE email = :email ``` **Step 3**: Access related sessions ```python user = db.query(User).filter(User.email == email).first() sessions = user.sessions # Access relationship ``` **Step 4**: Extract user_id from sessions ```python for session in sessions: print(f"User ID: {session.userId}") ``` ### 3. Expected Output Print the `user_id` from the session table that is associated with the matched user. ```python print(f"✅ User ID from session: {session.userId}") ``` ## Implementation Steps ### Step 1: Install Required Dependencies ```bash pip install python-jose[cryptography] sqlalchemy psycopg2-binary ``` ### Step 2: Create Database Models - File: `backend/app/database.py` - Create SQLAlchemy models for User and Session tables - Define relationship between tables - Setup database connection to NeonDB ### Step 3: Create JWT Validation Utility - File: `backend/app/auth.py` - Implement JWT decode and validation function - Handle Better Auth JWT token format - Extract email from token payload ### Step 4: Update `/support/chatkit` Endpoint - File: `backend/app/main.py` - Add JWT validation before processing request - Query database for user by email - Access sessions relationship - Print user_id from sessions - Return appropriate error responses for invalid tokens ## Error Handling ### Invalid Token ```json { "error": "Invalid or expired JWT token", "status": 401 } ``` ### User Not Found ```json { "error": "User not found with provided email", "status": 404 } ``` ### No Active Sessions ```json { "error": "No active sessions found for user", "status": 404 } ``` ## Environment Variables Required ```env DATABASE_URL=postgresql://user:password@neondb-host/database BETTER_AUTH_SECRET=your_better_auth_secret_key BETTER_AUTH_ISSUER=your_issuer # Optional ``` ## Success Flow Example ### Request ```http POST /support/chatkit Authorization: Bearer 0fOyRVonMqRyD20kP9Qi Content-Type: application/json { "message": "Hello" } ``` ### Processing 1. Extract token: `0fOyRVonMqRyD20kP9Qi` 2. Validate JWT ✅ 3. Extract email: `user@example.com` 4. Query database: Find user with `email = 'user@example.com'` 5. Access sessions: `user.sessions` 6. Print: `User ID: abc123xyz` ### Response ```http HTTP/1.1 200 OK Content-Type: text/event-stream [Normal ChatKit response continues...] ``` ### Console Output ``` 🔑 JWT Token: 0fOyRVonMqRyD20kP9Qi... ✅ JWT Validated 📧 Email from token: user@example.example.com 👤 User found: John Doe (ID: user_abc123) 🔗 Sessions found: 2 ✅ User ID from session: abc123xyz ``` ## Testing Checklist - [ ] Valid JWT token returns user_id - [ ] Invalid JWT token returns 401 error - [ ] Expired JWT token returns 401 error - [ ] Non-existent email returns 404 error - [ ] User with no sessions handles gracefully - [ ] Database connection errors handled - [ ] CORS headers still work correctly ## Additional Notes - Keep existing ChatKit functionality intact - JWT validation should happen before ChatKit processing - User context should be available throughout the request - Consider adding user_id to the request context for downstream use - Log all authentication attempts for security monitoring ## Success Criteria ✅ JWT token is validated on every `/support/chatkit` request ✅ Email is extracted from valid JWT token ✅ User is found in database by email ✅ Sessions relationship is accessed correctly ✅ User ID from sessions table is printed to console ✅ Invalid tokens return appropriate error responses ✅ Existing ChatKit functionality remains unaffected"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Authenticated ChatKit Request (Priority: P1)

As an authenticated user, I want to send a message to the `/support/chatkit` endpoint, and have my JWT token validated and my user ID retrieved, so that the ChatKit service can identify me.

**Why this priority**: This is the primary functionality of the feature.

**Independent Test**: Can be fully tested by sending an authorized request to `/support/chatkit` and verifying the user ID is correctly processed internally.

**Acceptance Scenarios**:

1.  **Given** I am an authenticated user with a valid JWT, **When** I send a POST request to `/support/chatkit` with my JWT in the Authorization header, **Then** my JWT is validated, my email is extracted, and my `user_id` from the sessions table is retrieved and printed to the console.
2.  **Given** I am an authenticated user with an invalid/expired JWT, **When** I send a POST request to `/support/chatkit`, **Then** the system returns a 401 Unauthorized error with the message "Invalid or expired JWT token".

---

### User Story 2 - User Not Found (Priority: P2)

As a user, if my email extracted from a valid JWT does not correspond to an existing user in the database, I want the system to handle this gracefully, so that it does not proceed with chat processing for an unknown user.

**Why this priority**: Ensures data integrity and prevents operations for non-existent users.

**Independent Test**: Can be tested by sending a valid JWT for an email not present in the database.

**Acceptance Scenarios**:

1.  **Given** I send a valid JWT for a user whose email is not found in the database, **When** I send a POST request to `/support/chatkit`, **Then** the system returns a 404 Not Found error with the message "User not found with provided email".

---

### User Story 3 - No Active Sessions (Priority: P2)

As a user, if my authenticated account has no active sessions, I want the system to indicate this, so that it does not attempt to retrieve a `user_id` from a non-existent session.

**Why this priority**: Handles a valid user with no current active session, preventing errors.

**Independent Test**: Can be tested by sending a valid JWT for a user who has no associated sessions in the database.

**Acceptance Scenarios**:

1.  **Given** I send a valid JWT for a user who has no active sessions, **When** I send a POST request to `/support/chatkit`, **Then** the system returns a 404 Not Found error with the message "No active sessions found for user".

---

### Edge Cases

-   What happens when the `Authorization` header is missing? (Should be a 401)
-   How does the system handle an incorrect token format (e.g., "Bearer" prefix missing)? (Should be a 401)
-   How does the system handle database connection errors during user/session retrieval? (Should return a 500 internal server error)
-   Does the existing ChatKit functionality remain unaffected by the JWT validation middleware? (Yes, explicitly stated in requirements)

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The system MUST extract the JWT token from the `Authorization` header of incoming requests to `/support/chatkit`.
-   **FR-002**: The system MUST validate the extracted JWT token using Better Auth configuration.
-   **FR-003**: The system MUST decode the valid JWT token to extract the user's email.
-   **FR-004**: The system MUST query the database to find a user by the extracted email.
-   **FR-005**: The system MUST access the sessions relationship associated with the found user.
-   **FR-006**: The system MUST retrieve and internally process the `user_id` from an active session for the authenticated user.
-   **FR-007**: The system MUST return a 401 Unauthorized response with "Invalid or expired JWT token" for invalid, expired, or malformed JWT tokens.
-   **FR-008**: The system MUST return a 404 Not Found response with "User not found with provided email" if the email from the JWT does not match any user.
-   **FR-009**: The system MUST return a 404 Not Found response with "No active sessions found for user" if a user is found but has no active sessions.
-   **FR-010**: The system MUST ensure that existing ChatKit functionality for `/support/chatkit` remains unaffected after JWT validation.
-   **FR-011**: The system MUST make the user context (including `user_id`) available for downstream processing within the `/support/chatkit` endpoint.
-   **FR-012**: The system MUST log all authentication attempts, including successes and failures, for security monitoring purposes.

### Key Entities *(include if feature involves data)*

-   **User**: Represents an individual user with attributes like `id`, `name`, `email`, `emailVerified`, `image`, `createdAt`, `updatedAt`.
-   **Session**: Represents an active user session with attributes like `id`, `userId` (foreign key to User), `expiresAt`, `token`, `ipAddress`, `userAgent`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: 100% of valid JWT authenticated requests to `/support/chatkit` result in successful user ID retrieval and continuation of ChatKit processing.
-   **SC-002**: All invalid or expired JWT tokens are rejected with a 401 Unauthorized response, preventing unauthorized access.
SC-003: User retrieval from the database based on email completes within 100 milliseconds for 99% of requests.
-   **SC-004**: The `user_id` is consistently and correctly identified from the sessions table for every valid authenticated request.
-   **SC-005**: The existing ChatKit functionality of the `/support/chatkit` endpoint functions identically for authenticated requests as it did prior to this feature, aside from the added user context.
SC-006: Authentication-related logs are retained for 30 days and are accessible by the Security Team via a centralized logging system for security monitoring.