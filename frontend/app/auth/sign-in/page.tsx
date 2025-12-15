"use client";
import { useState } from "react";
import { signIn, signUp } from "../../lib/auth-client";
import { useRouter } from "next/navigation";

export default function AuthPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [isSignUp, setIsSignUp] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const router = useRouter();

  const handleAuth = async () => {
    if (!email || !password) {
      setError("Email and password are required");
      return;
    }
    if (password.length < 8) {
      setError("Password must be at least 8 characters long");
      return;
    }

    setLoading(true);
    setError("");

    try {
      if (isSignUp) {
        await signUp.email(
          {
            email,
            password,
            name: name || email.split("@")[0],
          },
          {
            onSuccess: () => router.push("/chat"),
            onError: (ctx: { error: { message: string } }) => {
              setError(ctx.error.message || "Sign up failed");
              setLoading(false);
            },
          }
        );
      } else {
        await signIn.email(
          { email, password },
          {
            onSuccess: () => router.push("/chat"),
            onError: (ctx: { error: { message: string } }) => {
              setError(ctx.error.message || "Invalid credentials");
              setLoading(false);
            },
          }
        );
      }
    } catch (err: unknown) { // Use 'unknown' for better type safety
      setError((err instanceof Error) ? err.message : "Something went wrong");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 px-4 py-8">
      <div className="relative bg-white rounded-3xl p-8 sm:p-10 max-w-md w-full shadow-2xl border border-slate-200 hover:shadow-3xl hover:border-indigo-200 transition-all duration-300 overflow-hidden group">
        
        {/* Decorative Background Gradient */}
        <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-indigo-100/50 to-transparent rounded-full blur-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
        
        <div className="relative z-10">
          {/* Icon */}
          <div className="flex justify-center mb-6">
            <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-2xl bg-gradient-to-br from-indigo-600 to-blue-600 shadow-xl shadow-indigo-500/40 flex items-center justify-center transform hover:scale-110 hover:rotate-3 transition-all duration-300">
              <svg 
                className="text-white w-8 h-8 sm:w-10 sm:h-10" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
                strokeWidth={2}
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" 
                />
              </svg>
            </div>
          </div>

          {/* Title */}
          <h2 className="text-3xl sm:text-4xl font-bold text-center text-slate-900 mb-2">
            {isSignUp ? "Create Account" : "Welcome Back"}
          </h2>
          <p className="text-center text-slate-600 mb-8 text-base">
            {isSignUp ? "Sign up to get started" : "Sign in to continue"}
          </p>

          {/* Form */}
          <div className="space-y-5">
            {isSignUp && (
              <div className="space-y-2">
                <label className="block text-sm font-semibold text-slate-700">
                  Name (optional)
                </label>
                <input
                  type="text"
                  placeholder="Your name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  disabled={loading}
                  className="w-full px-4 py-3 rounded-xl border-2 border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 outline-none transition-all duration-200 text-slate-900 placeholder-slate-400 disabled:bg-slate-50 disabled:cursor-not-allowed"
                />
              </div>
            )}

            <div className="space-y-2">
              <label className="block text-sm font-semibold text-slate-700">
                Email
              </label>
              <input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={loading}
                className="w-full px-4 py-3 rounded-xl border-2 border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 outline-none transition-all duration-200 text-slate-900 placeholder-slate-400 disabled:bg-slate-50 disabled:cursor-not-allowed"
              />
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-semibold text-slate-700">
                Password
              </label>
              <input
                type="password"
                placeholder="Min 8 characters"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
                className="w-full px-4 py-3 rounded-xl border-2 border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 outline-none transition-all duration-200 text-slate-900 placeholder-slate-400 disabled:bg-slate-50 disabled:cursor-not-allowed"
              />
            </div>

            {error && (
              <div className="bg-red-50 border-2 border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm font-medium animate-pulse">
                {error}
              </div>
            )}

            <button
              onClick={handleAuth}
              disabled={loading}
              className="w-full bg-gradient-to-r from-indigo-600 to-blue-600 text-white font-semibold py-3.5 rounded-xl shadow-lg shadow-indigo-500/30 hover:shadow-xl hover:shadow-indigo-500/50 transform hover:-translate-y-0.5 active:translate-y-0 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-2 text-base"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                  Processing...
                </>
              ) : (
                <>
                  {isSignUp ? "Sign Up" : "Sign In"}
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </>
              )}
            </button>

            <button
              onClick={() => {
                setIsSignUp(!isSignUp);
                setError("");
              }}
              disabled={loading}
              className="w-full bg-white text-slate-700 font-semibold py-3.5 rounded-xl border-2 border-slate-200 hover:border-indigo-400 hover:bg-slate-50 transform hover:-translate-y-0.5 active:translate-y-0 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none text-base"
            >
              {isSignUp ? "Already have an account? Sign In" : "Create new account"}
            </button>
          </div>

          {/* Footer Text */}
          <p className="text-center text-sm text-slate-500 mt-6">
            By continuing, you agree to our{" "}
            <span className="text-indigo-600 font-semibold hover:underline cursor-pointer">
              Terms
            </span>
            {" "}&{" "}
            <span className="text-indigo-600 font-semibold hover:underline cursor-pointer">
              Privacy Policy
            </span>
          </p>
        </div>
      </div>
    </div>
  );
}