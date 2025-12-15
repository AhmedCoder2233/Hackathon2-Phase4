# Data Model: JWT Authentication & User ID Retrieval

**Date**: December 14, 2025
**Feature**: `006-jwt-auth`
**Spec**: `specs/006-jwt-auth/spec.md`

## Entities

### User

Represents a user in the system.

-   **id**: `TEXT` (Primary Key) - Unique identifier for the user.
-   **name**: `TEXT` - User's display name.
-   **email**: `TEXT` (Unique, Not Null) - User's email address, used for identification via JWT.
-   **emailVerified**: `BOOLEAN` (Default: `false`) - Indicates if the user's email has been verified.
-   **image**: `TEXT` - URL or path to user's profile image.
-   **createdAt**: `TIMESTAMP` (Default: `CURRENT_TIMESTAMP`) - Timestamp of user creation.
-   **updatedAt**: `TIMESTAMP` (Default: `CURRENT_TIMESTAMP`) - Timestamp of last user update.
-   **sessions**: `RELATIONSHIP` - One-to-many relationship with the Session entity.

### Session

Represents an active session for a user.

-   **id**: `TEXT` (Primary Key) - Unique identifier for the session.
-   **userId**: `TEXT` (Foreign Key -> User.id) - Links the session to a specific user.
-   **expiresAt**: `TIMESTAMP` - Timestamp when the session expires.
-   **token**: `TEXT` - The session token.
-   **ipAddress**: `TEXT` - IP address from which the session was initiated.
-   **userAgent**: `TEXT` - User-Agent string from the client.

## Relationships

-   **User to Session**: A `User` can have multiple `Session`s. Each `Session` belongs to one `User` via the `userId` foreign key.
