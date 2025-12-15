import { auth } from "../../../lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

// Export handlers
export const { POST, GET } = toNextJsHandler(auth);