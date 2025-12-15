"use client";

import Link from "next/link";
import { useSession, signOut } from "../app/lib/auth-client";
import { useRouter } from "next/navigation";

export default function Home() {
  const { data: session, isPending } = useSession();
  const router = useRouter();

  const handleSignOut = async () => {
    await signOut();
    router.push("/");
  };

  if (isPending) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
        <div className="flex flex-col items-center space-y-4">
          <div className="relative">
            <div className="animate-spin rounded-full h-16 w-16 border-4 border-indigo-200 border-t-indigo-600"></div>
            <div className="absolute inset-0 rounded-full h-16 w-16 border-4 border-transparent border-t-indigo-400 animate-ping opacity-75"></div>
          </div>
          <p className="text-lg text-slate-700 font-medium animate-pulse">
            Loading user session...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header with Logout Button */}
      {session?.user && (
        <header className="absolute top-0 right-0 p-4 sm:p-6">
          <button
            onClick={handleSignOut}
            className="group flex items-center gap-2 px-4 py-2 bg-white text-slate-700 text-sm font-medium rounded-lg shadow-md hover:shadow-lg border border-slate-200 hover:border-red-300 hover:bg-red-50 hover:text-red-600 transform hover:-translate-y-0.5 transition-all duration-200"
          >
            <svg 
              className="w-4 h-4" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
              strokeWidth={2}
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round"
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" 
              />
            </svg>
            Logout
          </button>
        </header>
      )}

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="min-h-screen flex flex-col items-center justify-center py-12 sm:py-16 lg:py-20">
          
          {/* Logo/Icon with Gradient */}
          <div className="mb-8 sm:mb-10">
            <div className="w-20 h-20 sm:w-24 sm:h-24 rounded-2xl bg-gradient-to-br from-indigo-600 to-blue-600 shadow-2xl shadow-indigo-500/40 flex items-center justify-center transform hover:scale-110 hover:rotate-3 transition-all duration-300 ease-out">
              <svg 
                className="text-white w-10 h-10 sm:w-12 sm:h-12" 
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

          {/* Heading with Gradient Text */}
          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold text-center text-slate-900 mb-6 leading-tight">
            Organize Your Life
            <br />
            <span className="bg-gradient-to-r from-indigo-600 via-blue-600 to-purple-600 bg-clip-text text-transparent animate-pulse">
              One Task at a Time
            </span>
          </h1>

          {/* Description */}
          <p className="text-base sm:text-lg md:text-xl text-slate-600 text-center max-w-2xl mb-10 sm:mb-12 px-4 leading-relaxed">
            A simple, beautiful, and powerful todo app to help you stay organized and productive. 
            Track your tasks, set priorities, and achieve your goals.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 mb-16 sm:mb-20 w-full sm:w-auto px-4">
            {session?.user ? (
              <button
                onClick={() => router.push("/chat")}
                className="group relative px-8 py-4 bg-gradient-to-r from-indigo-600 to-blue-600 text-white text-base sm:text-lg font-semibold rounded-xl shadow-lg shadow-indigo-500/30 hover:shadow-2xl hover:shadow-indigo-500/50 transform hover:-translate-y-1 active:translate-y-0 transition-all duration-300 overflow-hidden"
              >
                <span className="relative z-10 flex items-center justify-center gap-2">
                  Go to Dashboard
                  <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </span>
                <div className="absolute inset-0 bg-gradient-to-r from-indigo-700 to-blue-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </button>
            ) : (
              <>
                <Link 
                  href="/chat" 
                  className="group relative px-8 py-4 bg-gradient-to-r from-indigo-600 to-blue-600 text-white text-base sm:text-lg font-semibold rounded-xl shadow-lg shadow-indigo-500/30 hover:shadow-2xl hover:shadow-indigo-500/50 transform hover:-translate-y-1 active:translate-y-0 transition-all duration-300 overflow-hidden text-center"
                >
                  <span className="relative z-10 flex items-center justify-center gap-2">
                    Get Started
                    <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  </span>
                  <div className="absolute inset-0 bg-gradient-to-r from-indigo-700 to-blue-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                </Link>
                
                <Link 
                  href="/auth/sign-in" 
                  className="px-8 py-4 bg-white text-slate-700 text-base sm:text-lg font-semibold rounded-xl shadow-md hover:shadow-xl border-2 border-slate-200 hover:border-indigo-400 hover:bg-slate-50 transform hover:-translate-y-1 active:translate-y-0 transition-all duration-300 text-center"
                >
                  Sign Up Free
                </Link>
              </>
            )}
          </div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8 max-w-6xl w-full px-4">
            
            {/* Feature 1 - Fast & Simple */}
            <div className="group relative bg-white rounded-2xl p-6 sm:p-8 shadow-lg hover:shadow-2xl border border-slate-200 hover:border-blue-300 transform hover:-translate-y-2 transition-all duration-300 overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-blue-100/50 to-transparent rounded-full blur-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="relative z-10">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center mb-5 shadow-lg shadow-blue-500/30 group-hover:scale-110 group-hover:rotate-3 transition-transform duration-300">
                  <svg 
                    className="text-white w-7 h-7" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                    strokeWidth={2}
                  >
                    <path 
                      strokeLinecap="round" 
                      strokeLinejoin="round"
                      d="M13 10V3L4 14h7v7l9-11h-7z" 
                    />
                  </svg>
                </div>
                <h3 className="text-xl sm:text-2xl font-bold text-slate-900 mb-3 group-hover:text-blue-600 transition-colors duration-300">
                  Fast & Simple
                </h3>
                <p className="text-slate-600 leading-relaxed">
                  Add and manage tasks in seconds with our intuitive interface.
                </p>
              </div>
            </div>

            {/* Feature 2 - Stay Organized */}
            <div className="group relative bg-white rounded-2xl p-6 sm:p-8 shadow-lg hover:shadow-2xl border border-slate-200 hover:border-purple-300 transform hover:-translate-y-2 transition-all duration-300 overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-purple-100/50 to-transparent rounded-full blur-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="relative z-10">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-purple-500 to-purple-600 flex items-center justify-center mb-5 shadow-lg shadow-purple-500/30 group-hover:scale-110 group-hover:rotate-3 transition-transform duration-300">
                  <svg 
                    className="text-white w-7 h-7" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                    strokeWidth={2}
                  >
                    <path 
                      strokeLinecap="round" 
                      strokeLinejoin="round"
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" 
                    />
                  </svg>
                </div>
                <h3 className="text-xl sm:text-2xl font-bold text-slate-900 mb-3 group-hover:text-purple-600 transition-colors duration-300">
                  Stay Organized
                </h3>
                <p className="text-slate-600 leading-relaxed">
                  Filter, search, and prioritize your tasks effortlessly.
                </p>
              </div>
            </div>

            {/* Feature 3 - Track Progress */}
            <div className="group relative bg-white rounded-2xl p-6 sm:p-8 shadow-lg hover:shadow-2xl border border-slate-200 hover:border-green-300 transform hover:-translate-y-2 transition-all duration-300 overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-green-100/50 to-transparent rounded-full blur-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="relative z-10">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-green-500 to-green-600 flex items-center justify-center mb-5 shadow-lg shadow-green-500/30 group-hover:scale-110 group-hover:rotate-3 transition-transform duration-300">
                  <svg 
                    className="text-white w-7 h-7" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                    strokeWidth={2}
                  >
                    <path 
                      strokeLinecap="round" 
                      strokeLinejoin="round"
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" 
                    />
                  </svg>
                </div>
                <h3 className="text-xl sm:text-2xl font-bold text-slate-900 mb-3 group-hover:text-green-600 transition-colors duration-300">
                  Track Progress
                </h3>
                <p className="text-slate-600 leading-relaxed">
                  Visualize your productivity with insightful statistics.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="py-8 border-t border-slate-200/60 bg-white/60 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-slate-600 font-medium">
            Built with{" "}
            <span className="text-red-500 animate-pulse inline-block">❤️</span>
            {" "}using Next.js & Tailwind CSS
          </p>
        </div>
      </footer>
    </div>
  );
}