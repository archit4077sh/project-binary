"""
snippets/q_nextjs.py — 28 FRESH Next.js questions (mix of debugging + code generation)
Zero overlap with archived set.
"""

Q_NEXTJS = [

"""**Task (Code Generation):**
Implement a Next.js 14 Server Action for a multi-step form that:
- Validates each step server-side using Zod
- Stores intermediate progress in an encrypted cookie (not exposed to client)
- Returns typed errors back to the form via `useActionState`
- Clears the cookie on final submission or abandonment (via a separate cleanup action)

Show the action file, the Zod schemas, and the client form component.""",

"""**Debug Scenario:**
A Next.js 14 App Router page fetches user data in a Server Component and passes it to a Client Component. After deploying to Vercel, the user data is stale on the first request after deployment — it shows the previous user's data for ~30 seconds.

```tsx
// page.tsx (Server Component)
const user = await getUser(userId); // cached with default options
return <ProfileEditor user={user} />;
```

`getUser` uses `fetch` internally without cache options. Explain how Next.js's default fetch cache behaves per-request vs per-build, and show the correct combination of `cache: 'no-store'`, `revalidate`, and `unstable_noStore()` for user-specific data.""",

"""**Task (Code Generation):**
Build a Next.js middleware chain pattern that composes multiple middleware functions:

```ts
// middleware.ts
export default chain([
  withAuth,
  withLocale,
  withRateLimit,
  withSecurityHeaders,
]);
```

Each middleware in the chain can: return a response early, modify the request, or pass to the next middleware. Show the `chain` helper implementation and one complete middleware (`withAuth`) that reads a JWT, validates it, and redirects to `/login` if invalid.""",

"""**Debug Scenario:**
A Next.js 14 app uses `cookies().set()` inside a Server Component to set a theme preference. The deployment throws:

```
Error: Cookies can only be modified in a Server Action or Route Handler.
```

Explain why Next.js restricts cookie mutations to specific contexts, and design a proper theme-setting architecture using a Server Action triggered from a Client Component toggle button.""",

"""**Task (Code Generation):**
Implement a `getMetadataFromCMS` function that generates rich Open Graph metadata for dynamic blog posts in Next.js 14:

```ts
// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  // ...
}
```

Requirements:
- Fetches post data with `cache: 'force-cache'` and a `revalidateTag`
- Generates `og:image` using Next.js's `ImageResponse` (edge runtime)
- Falls back to a default OG image if the post has no image
- Includes Twitter card metadata
- Handles 404 (post not found) by returning minimal metadata

Show the full `generateMetadata` and the dynamic OG image route.""",

"""**Debug Scenario:**
A Next.js app uses `useSearchParams()` in a component. After adding `export const dynamic = 'force-static'` to the page, the build fails:

```
Error: Page "/search" with "force-static" couldn't be rendered statically 
because it used `useSearchParams`.
```

A teammate suggests wrapping the component in `<Suspense>`. Explain precisely why `useSearchParams` requires Suspense in static pages, what happens during SSG if search params aren't known at build time, and show the correct Suspense boundary placement.""",

"""**Task (Code Generation):**
Implement a Next.js Route Handler that acts as a proxy to an external API, adding authentication headers that shouldn't be exposed to the browser:

```
GET /api/proxy/reports?filter=active
→ https://internal-api.company.com/reports?filter=active
   with Authorization: Bearer ${SERVER_SECRET}
```

Requirements:
- Streams the response (don't buffer the entire response)
- Forwards relevant headers (`Content-Type`, `Cache-Control`)
- Validates the request is authenticated (checks session cookie) before proxying
- Handles upstream errors with proper status codes

Show the Route Handler using the Web Streams API.""",

"""**Debug Scenario:**
A Next.js app with App Router has a layout that fetches the current user:

```tsx
// app/layout.tsx
export default async function RootLayout({ children }) {
  const user = await getCurrentUser(); // DB call
  return <html><body><Nav user={user} />{children}</body></html>;
}
```

Users report the layout re-fetches on every navigation even for the same user. The DB call adds 80ms to every route transition. Explain why layout data re-fetches during client navigation, and show how to use React `cache()` to deduplicate the DB call within a single request.""",

"""**Task (Code Generation):**
Build a type-safe feature flag system for Next.js 14 that evaluates flags on the Edge:

```ts
// Usage in Server Component:
const flags = await getFlags(request);
if (flags.newCheckout) { return <NewCheckout />; }
```

Architecture requirements:
- Flags stored in Vercel Edge Config (or a JSON file for local dev)
- User-segment targeting: `{ role: 'beta' }` enables different flags
- Zero latency on the hot path (no external API call per request)
- Type-safe flag definitions (TypeScript)

Show the complete implementation.""",

"""**Debug Scenario:**
A Next.js 14 app with streaming SSR shows blank content for 3 seconds on the initial load, then everything appears at once. The Suspense boundaries are correctly set up.

Investigation with Chrome's Network tab shows a single large HTML response arriving after 3 seconds instead of streaming chunks. The server is running on Node.js with an nginx proxy.

Diagnose why nginx is buffering the streamed response and show the nginx config changes needed to enable true streaming (`X-Accel-Buffering`, `proxy_buffering`, chunked transfer encoding).""",

"""**Task (Code Generation):**
Implement a `useOptimisticAction` hook for Next.js 14 that wraps a Server Action with optimistic UI:

```tsx
const { trigger, optimisticState } = useOptimisticAction(
  deleteRow, // Server Action
  { onOptimistic: (state, id) => state.filter(r => r.id !== id) }
);
```

- Uses React 19's `useOptimistic` under the hood
- Reverts optimistic state if the Server Action throws
- Shows a loading indicator per-item (not full-page)
- Handles concurrent mutations (two deletes in quick succession)""",

"""**Debug Scenario:**
After migrating to Next.js 14 App Router, the team notices `console.log` statements in Server Components appear in both the server terminal AND the browser console. They expected server-only logs to be invisible to users.

Explain why Server Component logs appear in browser DevTools in Next.js development mode, whether this happens in production, and how to use `server-only` package + lint rules to prevent importing server-only code into Client Components.""",

"""**Task (Code Generation):**
Build a Next.js 14 multi-tenant routing system where the subdomain determines the tenant:

```
company1.app.com → tenant: company1
company2.app.com → tenant: company2
```

Requirements:
- Middleware reads the subdomain from `request.headers.get('host')`
- Rewrites the request to `/tenants/[tenant]/...` internally
- Passes the tenant context to Server Components via headers
- Works in local dev with custom hosts in `/etc/hosts`

Show the Middleware, the rewrite logic, and how Server Components read the tenant.""",

"""**Debug Scenario:**
A Next.js 14 dashboard uses Parallel Routes for a split-pane layout. When navigating between items in the `@detail` slot, the `@list` slot shows a loading state even though the list data hasn't changed.

The `@list` slot's `loading.tsx` file is triggering on every `@detail` navigation. Explain how Next.js determines when to show a slot's loading state during soft navigation, and how to prevent the list loading state from appearing when only the detail slot is navigating.""",

"""**Task (Code Generation):**
Implement incremental data loading for a Next.js 14 page that displays a large dataset in sections, using React Suspense and `loading.tsx`:

```
Page loads instantly →
  KPI cards load (fast query) →
    Data table loads (slow query) →
      Chart section loads (slowest)
```

Show the folder structure, the nested Suspense/loading boundaries, and how to use `Promise.all` vs sequential awaits to control load order. Explain when to use `loading.tsx` vs inline `<Suspense>` boundaries.""",

"""**Debug Scenario:**
A Next.js app deployed on Vercel has `revalidateTag('reports')` called in a Server Action. Other Vercel regions still serve stale data for up to 60 seconds after the tag is revalidated.

Explain Next.js's revalidation propagation across Vercel's CDN regions, why there's a propagation delay, and whether `revalidatePath` vs `revalidateTag` behaves differently across regions. What's the architecture for near-instant global consistency after a mutation?""",

"""**Task (Code Generation):**
Build a Next.js 14 authentication system using the new `auth()` pattern (no callbacks), with:
- Session stored in a signed, encrypted cookie (not database)
- `auth()` callable in Server Components, Route Handlers, and Middleware
- Protected routes redirect to `/login` via Middleware
- A `<SignOut>` Server Action that clears the cookie

Show all files: `auth.ts`, `middleware.ts`, `app/login/page.tsx`, `app/dashboard/layout.tsx`.""",

"""**Debug Scenario:**
A team built a Next.js API route that processes file uploads. It works in local dev but fails in production with a 413 error and in Vercel with a function timeout after 10 seconds for files over 4MB.

```ts
// app/api/upload/route.ts
export async function POST(req: Request) {
  const formData = await req.formData(); // buffers entire body
  const file = formData.get('file') as File;
  await uploadToS3(file);
}
```

Design a presigned URL upload pattern that bypasses the serverless function for file content, showing the Route Handler for generating the presigned URL and the client-side direct-to-S3 upload logic.""",

"""**Task (Code Generation):**
Implement a Next.js 14 sitemap generator that handles a large e-commerce site with 500,000 product pages:

```ts
// app/sitemap.ts
export default async function sitemap(): Promise<MetadataRoute.Sitemap>
```

Requirements:
- Can't return 500k entries in one response (memory limit)
- Use sitemap index + multiple sitemap files (`/sitemap/0.xml`, `/sitemap/1.xml`)
- Dynamic Route Handler per shard: `/sitemap/[shard]/route.ts`
- Cached at CDN level with `revalidate = 3600`

Show the index sitemap, the sharded sitemap route, and the database query strategy.""",

"""**Debug Scenario:**
A Next.js app uses `next/font` to load a custom font. In production, the font renders correctly. In development, the font fails to load with a CORS error in the console:

```
Access to font has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header
```

But `next/font` is supposed to self-host fonts automatically. Diagnose why CORS appears for fonts in dev mode vs production, and whether the error affects users or is a dev-mode artifact. Explain `next/font`'s font inlining strategy for production.""",

"""**Task (Code Generation):**
Build a real-time notification system for Next.js 14 using Server-Sent Events (SSE):

```
GET /api/notifications/stream → text/event-stream
```

Requirements:
- Route Handler streams events to connected clients
- Events pushed when a Server Action (e.g., task completion) fires
- Client subscribes with `useEventSource` hook
- Handles reconnection automatically
- Cleans up connections on client disconnect

Show the Route Handler, the server-side event emitter, and the React hook.""",

"""**Debug Scenario:**
A Next.js 14 page exports both `generateStaticParams` and uses `cookies()` in a nested Server Component. The build fails with conflicting requirements: static generation can't use dynamic APIs.

The team wants: pre-rendered pages (for SEO) + personalized content (from cookies). Diagnose the conflict and design a PPR (Partial Prerendering) solution where the static shell is pre-rendered but the personalized section is deferred to request time.""",

"""**Task (Code Generation):**
Implement a Next.js 14 rate limiter for API routes using Upstash Redis:

```ts
// Rate limit: 10 requests per minute per IP
const { success, limit, remaining, reset } = await rateLimit(request);
if (!success) return new Response('Too Many Requests', { status: 429 });
```

Show:
1. The Upstash Redis sliding window rate limiter implementation
2. Integration in a Route Handler middleware helper
3. IP extraction that works behind Vercel's proxy (`x-forwarded-for`)
4. Returning proper `Retry-After` and `X-RateLimit-*` headers""",

"""**Debug Scenario:**
After adding `export const runtime = 'edge'` to a Route Handler for better latency, the handler crashes with:

```
Error: The edge runtime does not support Node.js 'crypto' module.
```

The handler uses `crypto.createHmac` for webhook signature verification. List all Node.js APIs unavailable in the Edge Runtime, show how to replace `crypto.createHmac` with the Web Crypto API (`SubtleCrypto`), and explain when edge runtime is and isn't worth the migration pain.""",

"""**Task (Code Generation):**
Build a `useServerAction` hook that provides loading, error, and optimistic state for any Next.js 14 Server Action:

```tsx
const { execute, isPending, error } = useServerAction(saveReport);

<button onClick={() => execute(formData)} disabled={isPending}>
  {isPending ? 'Saving...' : 'Save'}
</button>
```

Requirements:
- Works with `startTransition` for non-blocking UI
- Captures thrown errors from Server Actions (they become unhandled rejections without this)
- Compatible with `useFormStatus`
- TypeScript generic: `useServerAction<TData, TError>`""",

"""**Debug Scenario:**
A Next.js 14 app with App Router has a layout that uses a React context provider. After deploying, users randomly see each other's data in the layout.

```tsx
// app/layout.tsx
const userCache = {}; // module-level cache
export default async function Layout({ children }) {
  const user = userCache[userId] ?? await getUser(userId);
  userCache[userId] = user;
}
```

Explain why module-level state in Server Components is shared across ALL users (Node.js module singleton), why this is a critical security bug, and the correct patterns for per-request state (React `cache()`, `headers()`, passing as props).""",

"""**Task (Code Generation):**
Implement a complete `robots.txt` + `sitemap.xml` + structured data (JSON-LD) setup for a Next.js 14 e-commerce site:

1. `app/robots.ts` — disallows `/account`, `/cart`, allows everything else, points to sitemap
2. `app/sitemap.ts` — categories and top products with `changefreq` and `priority`
3. A `<JsonLd>` component that injects `application/ld+json` for product pages

Show the TypeScript for all three, with the JSON-LD schema for a `Product` with `offers`, `aggregateRating`, and `breadcrumb`.""",

"""**Debug Scenario:**
A Next.js 14 app uses Prisma to query a PostgreSQL database. In production with multiple serverless function instances, the app hits a "too many database connections" error within minutes of high traffic.

```ts
// lib/db.ts
const prisma = new PrismaClient(); // new client per function invocation!
```

Explain why serverless functions create connection pool exhaustion with ORMs, show the Next.js-safe singleton pattern for PrismaClient using `globalThis`, and discuss PgBouncer vs connection pooling at the application layer.""",

]
