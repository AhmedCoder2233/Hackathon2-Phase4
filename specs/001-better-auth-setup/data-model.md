# Data Model for Better Auth Setup

This document outlines the core data entities and their relationships for the Better Auth Setup feature. Better Auth automatically manages the `user`, `session`, and `account` tables.

## Entities

### User

Represents an application user. Better Auth automatically generates unique `id` values using `nanoid`.

| Field         | Type       | Description                                  | Constraints       |
| :------------ | :--------- | :------------------------------------------- | :---------------- |
| `id`          | `TEXT`     | Unique user identifier                       | Primary Key       |
| `email`       | `TEXT`     | User's email address                         | Unique, Not Null  |
| `emailVerified` | `BOOLEAN`  | Indicates if the user's email has been verified |                   |
| `name`        | `TEXT`     | User's display name                          |                   |
| `createdAt`   | `TIMESTAMP`| Timestamp of user creation                   |                   |
| `updatedAt`   | `TIMESTAMP`| Timestamp of last update to user information |                   |
| `image`       | `TEXT`     | URL to user's profile image                  |                   |

**Relationships**:
- One-to-many with `Session` (a user can have multiple active sessions)
- One-to-many with `Account` (a user can have multiple associated accounts, e.g., for different authentication providers)

### Session

Represents an active authentication session for a user. Managed automatically by Better Auth.

| Field         | Type       | Description                                  | Relationships    |
| :------------ | :--------- | :------------------------------------------- | :--------------- |
| `id`          | `TEXT`     | Unique session identifier                    | Primary Key      |
| `userId`      | `TEXT`     | Foreign key referencing the `User` entity    | Many-to-one to User |
| `expires`     | `TIMESTAMP`| Timestamp when the session expires           |                  |
| `sessionToken`| `TEXT`     | Unique token used to identify the session    | Unique, Not Null |

### Account

Represents a link between a user and an authentication provider. Managed automatically by Better Auth.

| Field         | Type       | Description                                  | Relationships    |
| :------------ | :--------- | :------------------------------------------- | :--------------- |
| `id`          | `TEXT`     | Unique account identifier                    | Primary Key      |
| `userId`      | `TEXT`     | Foreign key referencing the `User` entity    | Many-to-one to User |
| `type`        | `TEXT`     | Type of authentication provider (e.g., "email")| Not Null         |
| `provider`    | `TEXT`     | Name of the provider (e.g., "emailAndPassword")| Not Null         |
| `providerAccountId` | `TEXT`     | Unique ID of the user within the provider| Not Null         |

---
**Note**: The exact schema details for `Session` and `Account` tables are derived from typical `better-auth` (and similar auth libraries) implementations and are primarily managed internally by the library. The focus is on the logical relationships.
