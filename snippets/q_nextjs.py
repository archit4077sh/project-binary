"""
snippets/q_nextjs.py — BATCH 4: 28 brand-new Next.js questions
Zero overlap with batch1, batch2, or batch3 archives.
"""

Q_NEXTJS = [

"""**Task (Code Generation):**
Implement a Next.js App Router layout that fetches navigation items from a CMS and caches them for 1 hour with stale-while-revalidate:

```ts
// app/layout.tsx
async function RootLayout({ children }) {
  const navItems = await fetchNav(); // cached
  return (
    <html>
      <body>
        <Nav items={navItems} />
        <main>{children}</main>
      </body>
    </html>
  );
}
```

Show: the `fetchNav` function with `next: { revalidate: 3600, tags: ['nav'] }`, adding a `/api/revalidate/nav` Route Handler that calls `revalidateTag('nav')` for webhook-based invalidation, and the Vercel KV / Upstash fallback when the CMS webhook fails.""",

"""**Debug Scenario:**
A Next.js 14 App Router page uses `generateMetadata` to set Open Graph images. The OG image tag appears in the HTML source but social media scrapers (Facebook, Twitter) still show no image.

Investigation reveals the OG image URL is relative (`/og.png`) instead of absolute. Social media scrapers need a fully-qualified URL (`https://example.com/og.png`).

Show: producing absolute URLs in `generateMetadata` using `process.env.NEXT_PUBLIC_BASE_URL + '/og.png'`, the `metadataBase` property in `layout.tsx` that auto-prefixes relative URLs in all child metadata, and using `<Suspense>` around the dynamic OG image to prevent blocking the initial page response.""",

"""**Task (Code Generation):**
Build a Next.js parallel route dashboard with tabs that each load independently:

```
app/dashboard/
  layout.tsx              ← renders @analytics and @sales side-by-side
  @analytics/page.tsx     ← slow analytics data (4s)
  @analytics/loading.tsx  ← analytics skeleton
  @sales/page.tsx         ← sales data (1s)
  @sales/loading.tsx      ← sales skeleton
```

Show: the layout using `{analytics}` and `{sales}` slot props, how each slot renders its own loading skeleton independently (analytics loads by itself without blocking sales), deep linking (URL reflects active tab), and the `default.js` file needed to prevent 404 when only navigating to one slot.""",

"""**Debug Scenario:**
A Next.js Route Handler uses `NextResponse.json()` to return JSON. When called from a native `fetch`, it works correctly. But when called from the same Next.js app's Server Component, the response body is consumed twice:

```ts
// Route Handler:
export async function GET() {
  return NextResponse.json({ data: 'hello' });
}

// Server Component:
const res = await fetch('/api/data');
console.log(await res.json()); // works
const body = await res.json(); // Error: body already consumed
```

Show: `Response.body` is a readable stream that can only be consumed once (Web Streams spec), the correct fix of storing the first `await res.json()` result, and why `next/server` Route Handlers should be called as functions in Server Components rather than fetched over HTTP (avoids serialization overhead).""",

"""**Task (Code Generation):**
Implement a Next.js middleware chain that applies multiple concerns in sequence:

```ts
// middleware.ts
const chain = createMiddlewareChain([
  rateLimitMiddleware({ maxRequests: 100, window: '1m' }),
  authMiddleware({ protectedPaths: ['/api/private', '/dashboard'] }),
  i18nMiddleware({ locales: ['en', 'fr', 'de'], defaultLocale: 'en' }),
  maintenanceModeMiddleware({ enabled: process.env.MAINTENANCE_MODE === 'true' }),
]);
export default chain;
export const config = { matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'] };
```

Show: the `createMiddlewareChain` factory that calls each middleware in sequence, early return (a middleware can return a redirect or response that bypasses downstream), request header mutation to pass context between middlewares, and TypeScript types for the middleware function signature.""",

"""**Debug Scenario:**
A Next.js app with `output: 'standalone'` (Docker deployment) crashes on startup with:

```
Error: Cannot find module './chunks/ssr/react-jsx-runtime.js'
```

The `standalone` output copies dependencies but some dynamic requires are not traced. Investigation shows a third-party library uses `require(variablePath)` with a runtime-determined path — next's dependency tracer can't discover it statically.

Show: the `experimental.outputFileTracingIncludes` config to manually add missing files to the trace, running `node .next/standalone/server.js` locally to reproduce the error, and the `NEXT_TRACE_UPLOADS` flag for debugging trace issues.""",

"""**Task (Code Generation):**
Build a `generateRobotsTxt` and `generateSitemapIndex` for a large Next.js app with 500,000 pages:

```ts
// app/robots.txt/route.ts:
export function GET() {
  return new Response(`User-agent: *\nAllow: /\nSitemap: https://example.com/sitemap-index.xml`);
}

// app/sitemap-index.xml/route.ts:
// Splits into 10 sitemaps of 50,000 URLs each
```

Show: the dynamic Route Handler that generates the sitemap index XML pointing to `/sitemap/1.xml` through `/sitemap/10.xml`, the paginated sitemap route `app/sitemap/[page]/route.ts` that fetches a slice of URLs from the database, the `lastmod` derived from the most recently updated record in each batch, and caching each sitemap page for 24 hours.""",

"""**Debug Scenario:**
A Next.js API Route Handler uses `ReadableStream` to stream a response. The stream works in development but in production on Vercel, clients receive the full response after a long delay instead of seeing chunks as they arrive.

The Route Handler sets `Transfer-Encoding: chunked` manually, but Vercel's edge proxy buffers the response until the stream closes before forwarding — the buffering defeats the streaming.

Show: setting `X-Accel-Buffering: no` response header to disable Nginx buffering on Vercel, using `text/event-stream` Content-Type for SSE (which has special unbuffering handling), and verifying streaming works with `curl --no-buffer https://example.com/api/stream` in CI.""",

"""**Task (Code Generation):**
Implement a Next.js static site that uses CMS webhook-triggered ISR with a fallback queue:

```ts
// When CMS updates content, it calls:
POST /api/webhook/revalidate { path: '/blog/my-post', secret }
→ calls revalidatePath('/blog/my-post')

// If webhook is missed, cron job runs every 30 min:
GET /api/cron/revalidate-stale
→ finds pages with updatedAt > last revalidation, calls revalidatePath for each
```

Show: the webhook Route Handler with HMAC signature verification, the cron Route Handler protected by a `CRON_SECRET`, the database query that finds stale pages, and Vercel's `cron.json` configuration.""",

"""**Debug Scenario:**
A Next.js App Router app uses `cookies()` inside a utility function called from multiple Server Components. Performance profiling shows each call reinitializes the cookie parsing (~5ms per call).

```ts
// utils/auth.ts:
export function getAuthUser() {
  const cookieStore = cookies(); // re-parses headers every call
  const session = cookieStore.get('session')?.value;
  return parseSession(session);
}
```

`cookies()` in Next.js 14 returns a cached `ReadonlyRequestCookies` object — it doesn't re-parse on every call. Show: confirming this with timing, the actual bottleneck (`parseSession` which calls `jwt.verify()` with an RSA public key on every call), and wrapping `getAuthUser` with `React.cache()` to memoize per-request.""",

"""**Task (Code Generation):**
Build a Next.js multi-tenant SaaS with database-per-tenant architecture:

```ts
// Middleware: identify tenant from subdomain
// app/middleware.ts:
const host = req.headers.get('host'); // 'acme.app.com'
const tenant = extractTenantFromHost(host);
req.headers.set('x-tenant-id', tenant);

// Server Components read the tenant header:
const tenantId = headers().get('x-tenant-id');
const db = await getTenantDatabase(tenantId); // connects to tenant's schema
```

Show: the Middleware logic for subdomain extraction, the database connection pool that maps `tenantId → Prisma client`, connection pooling with PgBouncer for many tenants, and the `notFound()` call for unknown tenants.""",

"""**Debug Scenario:**
A Next.js app uses `next/font` to load a custom local font. The font loads correctly in development but in production, the font shows a flash of unstyled text (FOUT) on the first visit.

`next/font` should add a `<link rel="preload">` for the font file automatically. Investigation shows the preload link is added to `<head>` but the font CSS uses `font-display: optional` (the next/font default), which instructs the browser to use the fallback font if the font hasn't loaded within a very short time window.

Show: changing to `font-display: swap` for FOUT (flash then swaps) vs `font-display: optional` (no flash, just uses fallback if not cached), the CSS size-adjust technique (adjusting fallback font metrics) to minimize the layout shift during swap, and `preloadFont: true` option.""",

"""**Task (Code Generation):**
Implement a Next.js streaming dashboard that shows partial data as it loads:

```tsx
// app/dashboard/page.tsx
export default function DashboardPage() {
  return (
    <main>
      <h1>Dashboard</h1>
      {/* Streams in immediately, no waiting */}
      <Suspense fallback={<StatsSkeleton />}>
        <Stats />  {/* fast: 200ms */}
      </Suspense>
      <Suspense fallback={<ChartSkeleton />}>
        <RevenueChart />  {/* slow: 3s */}
      </Suspense>
    </main>
  );
}
```

Show: how Next.js uses HTTP streaming to flush the HTML progressively (headers sent first, then Suspense shells resolved as they complete), the `defer` attribute on `<script>` tags that insert resolved Suspense content, and how `loading.tsx` IS a Suspense boundary (the difference between layout-level and page-level boundaries).""",

"""**Debug Scenario:**
A developer creates a Server Action but it returns `undefined` instead of the expected object when called from a Client Component form:

```ts
'use server';
async function createPost(formData: FormData) {
  const post = await db.posts.create({ ... });
  return { id: post.id, slug: post.slug }; // returned as undefined on client
}
```

Server Actions serialize the return value using React's serialization protocol. An object with string values should serialize correctly. Investigation reveals `post.id` is a PostgreSQL `BigInt` — which is NOT serializable by React's serializer.

Show: the fix (convert BigInt to string: `id: post.id.toString()`), the list of non-serializable types in Server Actions (functions, Dates not in specific formats, class instances), and using `zod`'s `transform` to auto-serialize query results.""",

"""**Task (Code Generation):**
Build a Next.js image optimization pipeline that generates multiple formats at build time:

```ts
// scripts/optimize-images.ts (runs in next.config.js's webpack config):
// For each source image:
// 1. Generate modern formats: avif, webp
// 2. Generate responsive sizes: 320, 640, 960, 1280, 1920
// 3. Generate LQIP blurred placeholder
// 4. Write manifest: { [origPath]: { avif: [...], webp: [...], lqip: string } }
```

Show: using `sharp` for image processing in a webpack plugin, the manifest JSON generation, a `<OptimizedImage>` component that reads the manifest and renders a `<picture>` element with proper srcset + LQIP placeholder, and skipping already-optimized images using content hash comparison.""",

"""**Debug Scenario:**
A Next.js app has a `layout.tsx` that fetches the user's subscription plan to conditionally render a premium badge. When the user upgrades their subscription, the badge doesn't appear until the browser hard-refreshes — even with `revalidatePath('/dashboard')` called after the upgrade.

`revalidatePath` invalidates the route cache in Next.js's server-side cache. But the client's router cache (client-side in-memory navigation cache) is still showing the old layout.

Show: calling `router.refresh()` on the client side after the mutation succeeds (forces Next.js to re-request the current page from the server, bypassing client router cache), the difference between `router.refresh()` (server re-render, keeps client state) vs `router.push(path)` (full navigation), and where the client router cache TTL is set.""",

"""**Task (Code Generation):**
Implement a Next.js API Gateway pattern that proxies to multiple microservices:

```ts
// app/api/[...path]/route.ts
export async function GET(req: Request, { params }) {
  const [service, ...rest] = params.path;
  const serviceUrl = SERVICE_MAP[service]; // 'users' → 'http://users-service:3001'
  
  const upstream = await fetch(`${serviceUrl}/${rest.join('/')}`, {
    headers: forwardHeaders(req.headers), // forward auth, trace-id
  });
  
  return new Response(upstream.body, {
    status: upstream.status,
    headers: filterResponseHeaders(upstream.headers),
  });
}
```

Show: the `SERVICE_MAP` configuration, the `forwardHeaders` utility (allowlist pattern for security), the `filterResponseHeaders` that removes internal headers before sending to client, adding `X-Request-Id` tracing, and rate limiting per service using Upstash Redis.""",

"""**Debug Scenario:**
A Next.js app uses `@vercel/og` to generate Open Graph images dynamically. In development the images render correctly, but in production on Vercel, Japanese text characters are replaced with tofu (□□□).

`@vercel/og` uses Satori for SVG rendering which requires font files to be explicitly loaded — the default system fonts don't include CJK characters.

Show: loading a CJK-capable font (Noto Sans JP) using `fetch(new URL('./NotoSansJP.ttf', import.meta.url))` in the Route Handler, passing `fonts` array to `ImageResponse`, the correct `weight` and `style` configuration, and caching the fetched font buffer using module-level `let fontBuffer: Buffer | null = null` to avoid re-fetching on every invocation.""",

"""**Task (Code Generation):**
Build a Next.js App Router app with complete authentication using Auth.js (NextAuth v5):

```ts
// auth.ts
export const { auth, signIn, signOut, handlers } = NextAuth({
  providers: [GitHub, Google, Credentials({ ... })],
  callbacks: {
    jwt({ token, user }) { if (user) token.role = user.role; return token; },
    session({ session, token }) { session.user.role = token.role; return session; },
  },
});

// Middleware protection:
export default auth((req) => {
  if (!req.auth && req.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', req.url));
  }
});
```

Show: the Route Handler (`app/api/auth/[...nextauth]/route.ts`), reading session in Server Components with `auth()`, and the CSRF protection built into Auth.js.""",

"""**Debug Scenario:**
A Next.js page exports both `generateStaticParams` and `export const dynamic = 'force-dynamic'`. TypeScript doesn't error, but at runtime, `generateStaticParams` is ignored — the page is always rendered dynamically.

Show: why `force-dynamic` and `generateStaticParams` are mutually exclusive (static params require static rendering, dynamic forces runtime rendering), removing `export const dynamic = 'force-dynamic'` and instead using `export const revalidate = 60` for on-demand revalidation, and the Next.js rendering mode decision tree (static → ISR → dynamic based on config and APIs used).""",

"""**Task (Code Generation):**
Implement a Next.js forms with progressive enhancement — works without JavaScript and improves with it:

```tsx
// Works without JS (pure HTML form submit):
<form action={createPost} method="POST">
  <input name="title" required />
  <textarea name="content" required />
  <button type="submit">Publish Post</button>
</form>
```

Show: the Server Action `createPost` that works as a traditional form submit (returns redirect on success), enhancing with `useFormState` and `useFormStatus` for rich client-side UX (inline errors, loading states, optimistic updates), the `<button disabled={isPending}>` pattern, and the fallback behavior when JavaScript fails to load.""",

"""**Debug Scenario:**
A Next.js app with `output: 'export'` (static HTML export) uses `dynamic` imports with `ssr: false`. The build fails with:

```
Error: Page /dynamic-page used `next/dynamic` with `ssr: false`. 
This is not supported for static HTML export.
```

Show: why `ssr: false` requires a Node.js server to serve the no-SSR fallback HTML (not possible in pure static export), the workaround using `typeof window !== 'undefined'` guard with regular `React.lazy`, the `useEffect` + `useState` client-only render pattern, and when `output: 'export'` is appropriate vs when a server deployment is necessary.""",

"""**Task (Code Generation):**
Build a Next.js search endpoint with full-text search and result highlighting:

```ts
// app/api/search/route.ts
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const q = searchParams.get('q') ?? '';
  
  const results = await db.$queryRaw`
    SELECT id, title, 
      ts_headline('english', content, plainto_tsquery('english', ${q})) as excerpt,
      ts_rank(search_vector, plainto_tsquery('english', ${q})) as rank
    FROM posts
    WHERE search_vector @@ plainto_tsquery('english', ${q})
    ORDER BY rank DESC
    LIMIT 20
  `;
  
  return NextResponse.json({ results });
}
```

Show: creating the `search_vector` column with a GIN index, the `<SearchResults>` client component with debounced query, and caching search results for identical queries using the `unstable_cache` helper.""",

"""**Debug Scenario:**
A Next.js app's Middleware sets a cookie on every request. In production, the Vercel dashboard shows 100% Middleware invocations but Edge Network logs show many requests are served from cache WITHOUT running Middleware.

Vercel CDN serves cached responses from the edge cache without calling Middleware for cached URLs. The cookie set by Middleware is missing for cached responses.

Show: using `Cache-Control: no-store` for authenticated responses (prevents caching), adding `Vary: Cookie` so cached responses are keyed per cookie value, and the correct Vercel CDN configuration where Middleware runs but responses are cached per-user (by setting `Vary` headers correctly).""",

"""**Task (Code Generation):**
Implement a complete Next.js App Router CRUD application with server-side form handling:

```ts
// Server Actions handle all mutations:
createUser(formData) → revalidatePath, redirect to user detail
updateUser(id, formData) → revalidatePath, return success/error
deleteUser(id) → revalidatePath, redirect to list

// Pages:
/users         → list all users
/users/new     → create form
/users/[id]    → detail view
/users/[id]/edit → edit form
```

Show: the complete server action implementations with Zod validation, the `useFormState` hook for inline error display, optimistic deletes using `useOptimistic`, and `redirect()` vs `revalidatePath()` after mutations.""",

"""**Debug Scenario:**
A Next.js app's font loading shows a TypeScript error after upgrading from next 14.1 → 14.2:

```ts
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'], display: 'swap' });
// Error: Type '{ subsets: string[]; display: string; }' is not assignable...
// 'display' type was narrowed to 'swap' | 'auto' | 'block' | 'fallback' | 'optional'
```

The value was previously typed as `string` but was narrowed to a literal union in the new version. Show: the TypeScript fix (`display: 'swap' as const`), why `display: string` was too permissive (could pass invalid values), and how to add a module augmentation if a font option is missing from the type definitions.""",

"""**Task (Code Generation):**
Build a Next.js webhook receiver with request validation, idempotency, and retry tracking:

```ts
// app/api/webhooks/stripe/route.ts
export async function POST(req: Request) {
  // 1. Verify Stripe signature
  const signature = req.headers.get('stripe-signature') ?? '';
  const event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
  
  // 2. Check idempotency (don't process twice)
  const processed = await db.processedWebhooks.findUnique({ where: { eventId: event.id } });
  if (processed) return new Response('Already processed', { status: 200 });
  
  // 3. Process event
  await handleStripeEvent(event);
  
  // 4. Mark as processed
  await db.processedWebhooks.create({ data: { eventId: event.id, processedAt: new Date() } });
  return new Response('OK', { status: 200 });
}
```

Show: the full implementation with error handling (return 200 to Stripe even on our errors to prevent retries), the `processedWebhooks` table schema, and a dead-letter queue for events that fail repeatedly.""",

"""**Debug Scenario:**
A Next.js App Router page uses `notFound()` inside a Server Component to return a 404. The custom `not-found.tsx` file is in the correct app directory, but requests still show Next.js's default 404 page instead of the custom component.

The issue is `not-found.tsx` is placed in `app/products/not-found.tsx` (the route segment), but the `notFound()` call is inside a nested Server Component that's imported into the products page — Next.js only looks for `not-found.tsx` in the same or parent segment directories relative to where `notFound()` is called.

Show: verifying the `not-found.tsx` location (must be co-located with or above the page using `notFound()`), that `app/not-found.tsx` at the root acts as the global 404 handler, the `generateMetadata` export in `not-found.tsx` for proper 404 page metadata, and the HTTP status code verification using `curl -I` to confirm it returns `404` and not `200`.""",

]
