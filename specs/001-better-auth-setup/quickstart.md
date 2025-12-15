# Quick Start Guide: Better Auth Setup

This guide provides the essential steps to quickly get the Better Auth Setup feature up and running in your Next.js application.

## 1. Environment Setup

### 1.1. Install Dependencies

Navigate to your project's `frontend` directory (if applicable, or root if it's a monorepo containing Next.js) and install the required packages:

```bash
npm install better-auth pg
```

### 1.2. Configure Environment Variables

Create a `.env.local` file in the root of your Next.js application (e.g., `frontend/.env.local`) and populate it with the following variables. **Ensure to replace placeholder values with your actual database credentials and a strong secret key.**

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# Better Auth
BETTER_AUTH_SECRET=your-32-character-or-longer-secret-key
BETTER_AUTH_URL=http://localhost:3000

# Next.js Public
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**IMPORTANT**: Generate a secure `BETTER_AUTH_SECRET` using a tool like `openssl`:

```bash
openssl rand -base64 32
```

## 2. Auth Files Setup

Ensure the following files are set up as described in the specification. These are critical for Better Auth integration:

*   `app/api/auth/[...all]/route.ts`
*   `app/lib/auth.ts`
*   `app/lib/auth-client.ts`

Refer to the full feature specification (`specs/001-better-auth-setup/spec.md`) for detailed content of these files.

## 3. Database Initialization

Better Auth automatically creates the necessary database tables (`user`, `session`, `account`) when the application starts if they don't already exist.

## 4. Run the Application

Start your Next.js development server:

```bash
npm run dev
```

The application will typically be accessible at `http://localhost:3000`. You can then navigate to `/` to access the login/signup page and test the authentication flow.

## 5. Testing the Feature

*   **Sign Up**: Create a new account with an email and password.
*   **Login**: Log in with your newly created account.
*   **Dashboard Access**: Verify that you can access the `/dashboard` page after logging in.
*   **Logout**: Test the logout functionality.
*   **Protected Route**: Ensure unauthenticated users are redirected from `/dashboard` to `/`.
