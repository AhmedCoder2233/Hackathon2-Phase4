import { betterAuth } from "better-auth";
import { Pool } from "pg";
import { generateUserId } from "./uuid"; // Import the UUID generator

// Test database connection
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

// Test connectionA
pool.query("SELECT NOW()", (err, res) => {
  if (err) {
    console.error("❌ Database connection failed:", err);
  } else {
    console.log("✅ Database connected:", res.rows[0]);
  }
});

export const auth = betterAuth({
  database: pool,
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
    // Assuming better-auth provides an onSignUp hook or similar
    // This is an assumption based on the task description "Add unique user_id generation on signup in Better Auth config"
    onSignUp: async (user:any) => {
      // Assuming 'id' is where betterAuth stores its primary identifier
      // If user.id is already set by betterAuth, we might not want to override it.
      // The task says "Add unique user_id generation", implying we should ensure it's set.
      if (!user.id) {
        user.id = generateUserId(); // Assign the generated UUID as user_id
      }
      // Assuming better-auth will automatically persist changes made to 'user' object in onSignUp.
      return user;
    },
  },
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
  logger: {
    level: "debug", // Enable detailed logging
  },
});