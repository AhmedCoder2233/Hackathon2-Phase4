---
id: 14
title: Enabled Email/Password Signup
stage: red
date: 2025-12-13
surface: agent
model: gemini-1.5-pro
feature: 001-better-auth-setup
branch: 001-better-auth-setup
user: Ahmed
command: User reported API error: "Email and password sign up is not enabled" during signup.
labels: ["bug-fix", "better-auth", "nextjs", "configuration"]
links:
  spec: specs/001-better-auth-setup/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - frontend/app/lib/auth.ts
tests:
 null
---

## Prompt

this error when trying to sign up hook.js:608 A tree hydrated but some attributes of the server rendered HTML didn't match the client properties. This won't be patched up. This can happen if a SSR-ed Client Component used:
- A server/client branch `if (typeof window !== 'undefined')`.
- Variable input such as `Date.now()` or `Math.random()` which changes each time it's called.
- Date formatting in a user's locale which doesn't match the server.
- External changing data without sending a snapshot of it along with the HTML.
- Invalid HTML tag nesting.
It can also happen if the client has a browser extension installed which messes with the HTML before React loaded.
https://react.dev/link/hydration-mismatch
  ...
    <HotReload globalError={[...]} webSocket={WebSocket} staticIndicatorState={{pathname:null, ...}}>
      <AppDevOverlayErrorBoundary globalError={[...]}>
        <ReplaySsrOnlyErrors>
        <DevRootHTTPAccessFallbackBoundary>
          <HTTPAccessFallbackBoundary notFound={<NotAllowedRootHTTPFallbackError>}>
            <HTTPAccessFallbackErrorBoundary pathname="/" notFound={<NotAllowedRootHTTPFallbackError>} ...>
              <RedirectBoundary>
                <RedirectErrorBoundary router={{...}}>
                  <Head>
                  <__next_root_layout_boundary__>
                    <SegmentViewNode type="layout" pagePath="layout.tsx">
                      <SegmentTrieNode>
                      <link>
                      <script>
                      <RootLayout>
                        <html lang="en">
                          <body
                            className="geist_a71539c9-module__T19VSG__variable geist_mono_8d43a2aa-module__8Li5zG__var..."
-                           cz-shortcut-listen="true"
                          >
                  ...
forward-logs-shared.ts:95 Signup submitted: 
Object
forward-logs-shared.ts:95 [Fast Refresh] rebuilding
forward-logs-shared.ts:95 [Fast Refresh] done in 1293ms
:3000/api/auth/sign-up/email:1 
 Failed to load resource: the server responded with a status of 400 (BAD_REQUEST)
hook.js:608 Signup error: 
Object
code
: 
"EMAIL_AND_PASSWORD_SIGN_UP_IS_NOT_ENABLED"
message
: 
"Email and password sign up is not enabled"
status
: 
400
statusText
: 
"BAD_REQUEST"
[[Prototype]]
: 
Object

## Response snapshot

Addressed the API error "EMAIL_AND_PASSWORD_SIGN_UP_IS_NOT_ENABLED" by modifying `frontend/app/lib/auth.ts` to explicitly enable email and password sign-up within the `betterAuth` configuration. Added `emailAndPassword: { enabled: true, minPasswordLength: 8, }` to the `betterAuth` initialization. The hydration mismatch error is noted but not addressed as it's likely a browser extension issue.

## Outcome

- ✅ Impact: Enabled email and password sign-up functionality on the server-side, resolving the 400 BAD_REQUEST API error.
- 🧪 Tests: No automated tests run; fix based on error message and library configuration.
- 📁 Files: Modified `frontend/app/lib/auth.ts`.
- 🔁 Next prompts: Verify sign-up functionality and check for any remaining issues.
- 🧠 Reflection: Server-side authentication configurations, especially enabling specific methods like email/password, are crucial and must align with the client-side expectations. Misconfigurations can lead to seemingly functional client code failing due to server-side rejections.

## Evaluation notes (flywheel)

- Failure modes observed: Server-side configuration discrepancy leading to API rejection.
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
