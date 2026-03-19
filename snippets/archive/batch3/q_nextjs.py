"""
snippets/q_nextjs.py — BATCH 3: 28 brand-new Next.js questions
Zero overlap with batch1 or batch2 archives.
"""

Q_NEXTJS = [

"""**Task (Code Generation):**
Implement a multi-tenant Next.js 14 App Router application where each tenant has a subdomain (`tenant.app.com`) routed to their own data and theme:

```ts
// middleware.ts:
const tenant = req.nextUrl.hostname.split('.')[0]; // 'acme' from acme.app.com
// Rewrite to /tenants/acme/dashboard without changing the URL
```

Show: the Middleware rewriting strategy, how tenant config (theme, feature flags) is fetched once per request and stored in a request-scoped variable, Next.js `generateStaticParams` for pre-building known tenant pages, and the database multi-tenancy pattern (row-level security vs separate schemas).""",

"""**Debug Scenario:**
A Next.js 14 Server Action that handles a file upload fails silently in production. The action works in development but in production the `FormData` body is empty.

```ts
'use server';
async function uploadFile(formData: FormData) {
  const file = formData.get('file'); // null in production
}
```

Investigation reveals Vercel has a 4.5MB default body size limit, and the upload is a 6MB file. Show: configuring `export const config = { api: { bodyParser: false } }` (doesn't apply to Server Actions), the correct way to configure the Vercel function body size limit, and an alternative — streaming the upload directly to S3 with a presigned URL bypassing Next.js entirely.""",

"""**Task (Code Generation):**
Build a `generateSitemap` utility for a Next.js App Router app that creates a dynamic `sitemap.xml` from database content:

```ts
// app/sitemap.ts
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const [staticRoutes, blogPosts, products] = await Promise.all([...]);
  return [...staticRoutes, ...blogPosts, ...products];
}
```

Requirements:
- Static routes with fixed priority/changefreq
- Blog posts from CMS with `lastModified` from `updated_at` column
- Product pages with `changefreq: 'daily'`
- Sitemap index (split into multiple sitemaps) when > 50,000 URLs
- Revalidate every 24 hours (`revalidate = 86400`)""",

"""**Debug Scenario:**
A Next.js App Router page uses `useSearchParams()` inside a component wrapped with `<Suspense>`. When users navigate to the page directly (no Suspense parent), the page crashes with:

```
Error: `useSearchParams()` should be wrapped in a suspense boundary at the page level.
```

But the component IS wrapped in Suspense. Investigate: the error happens because `useSearchParams()` triggers Suspense but the Suspense boundary is below the component — it must be above. Show the correct component tree structure and why Next.js requires `useSearchParams` to be in a Client Component with a Suspense boundary at the page export level.""",

"""**Task (Code Generation):**
Implement optimistic UI for a Next.js Server Action that "likes" a post:

```tsx
// The like count updates immediately (optimistic) and confirms/reverts from server
const [optimisticLikes, addOptimisticLike] = useOptimistic(
  post.likes,
  (state, userId: string) => [...state, userId]
);

async function handleLike() {
  addOptimisticLike(currentUser.id);
  await likePost(post.id); // Server Action
}
```

Show: `useOptimistic` setup, the Server Action with `revalidatePath`, handling the case where the action fails (automatic rollback), and the transition to show "pending" state while the server processes.""",

"""**Debug Scenario:**
A Next.js app's `generateMetadata` function fetches from the same API as the page component. This causes two identical API requests per page render.

```ts
// page.tsx
export async function generateMetadata({ params }) {
  const post = await getPost(params.id); // request 1
  return { title: post.title };
}
export default async function Page({ params }) {
  const post = await getPost(params.id); // request 2, identical
  return <Article post={post} />;
}
```

Show how `React.cache()` deduplicates these requests within a single render tree (unlike `fetch` deduplication which only works for `fetch` calls, not arbitrary async functions). Show the `getPost` wrapper with `React.cache()` and verify deduplication with timing logs.""",

"""**Task (Code Generation):**
Build a `useServerAction<T>` hook that wraps Next.js Server Actions with loading, error, and optimistic state:

```ts
const { execute, isPending, error, data } = useServerAction(createReport);
// Usage:
await execute({ title, content });
// Shows loading spinner during action, handles errors, shows success state
```

Show: `useTransition` for pending state, error boundary integration for thrown errors, `useOptimistic` for immediate UI response, and TypeScript inference of the action's parameter and return types from the Server Action function signature.""",

"""**Debug Scenario:**
A Next.js 14 Parallel Route shows a blank loading state instead of the `default.js` fallback. The folder structure is:

```
app/
  layout.tsx
  @analytics/
    page.tsx
  @main/
    page.tsx
```

The `@analytics` slot renders a slow component. During navigation, the page shows a blank slot instead of the previous content while loading. Explain when Next.js shows `loading.js` vs renders the previous slot vs shows `default.js`, and how `loading.js` inside a slot vs at the layout level produces different UX.""",

"""**Task (Code Generation):**
Implement a Next.js API Rate Limiter middleware using Edge Runtime and Upstash Redis:

```ts
// middleware.ts
const rateLimit = createRateLimiter({
  requests: 10,
  window: '60s',
  identifier: (req) => req.headers.get('x-forwarded-for') ?? 'anonymous',
  onLimit: (req, limit) => new Response(`Rate limited. Retry after ${limit.reset}s`, { status: 429 }),
});
```

Show: Upstash Redis sliding window algorithm, the `RateLimitResult` type, adding `X-RateLimit-*` headers to all responses, exempting authenticated users from the limit, and distributing the check across Vercel Edge regions.""",

"""**Debug Scenario:**
A Next.js app's static pages (generated at build time with `generateStaticParams`) show stale data for up to 24 hours because `revalidate = 86400` is set. After a CMS content update, the team triggers `revalidatePath('/blog/my-post')` via a webhook — but the page still shows stale data.

Investigation shows `revalidatePath` is called in a Route Handler but the path parameter doesn't exactly match the page's route. Show the exact path formats that `revalidatePath` accepts, the difference between `revalidatePath('/blog/my-post')` vs `revalidatePath('/blog/[slug]', 'page')`, and how to use `revalidateTag` as a more robust alternative.""",

"""**Task (Code Generation):**
Build a real-time notification system using Next.js Route Handlers with Server-Sent Events (SSE):

```ts
// app/api/notifications/stream/route.ts
export async function GET(req: Request) {
  const stream = new ReadableStream({
    start(controller) {
      // Send events to controller.enqueue()
    },
  });
  return new Response(stream, {
    headers: { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache' },
  });
}
```

Show: the SSE stream implementation, client-side `EventSource` hook, reconnection handling, authentication via cookie in the SSE request, and cleanup when the client disconnects.""",

"""**Debug Scenario:**
A Next.js App Router app has a `layout.tsx` that renders a complex navigation sidebar. The sidebar re-renders on every page navigation because a `'use client'` directive was added to `layout.tsx` to use `usePathname()`.

The fix should preserve the sidebar as a Server Component. Show: extracting `usePathname()` into a small `<ActiveLink>` Client Component nested inside the Server Component sidebar, the pattern of "pushing `use client` down the tree," and why this dramatically reduces client-side JavaScript for the navigation.""",

"""**Task (Code Generation):**
Implement a Next.js middleware that handles authentication and authorization:

```ts
export function middleware(req: NextRequest) {
  const token = req.cookies.get('session')?.value;
  
  if (!token && isProtected(req.nextUrl.pathname)) {
    return NextResponse.redirect(new URL('/login', req.url));
  }
  
  if (token && !hasPermission(token, req.nextUrl.pathname)) {
    return NextResponse.redirect(new URL('/403', req.url));
  }
}
```

Show: JWT verification in Edge Runtime (using `jose`, not `jsonwebtoken`), the `isProtected` path matcher with wildcards, role-based `hasPermission` checks, setting request headers to pass user context to Server Components, and the `matcher` config to skip static assets.""",

"""**Debug Scenario:**
A Next.js app's `next/image` component shows oversized images on Retina displays (2x), loading 2400px images when 1200px would suffice visually. The `sizes` prop is missing.

```tsx
<Image src={hero} alt="Hero" width={1200} height={600} />
// On 2x screen → loads 2400px intrinsic width image
```

Explain how `next/image` uses `srcset` + `sizes` to determine which image variant to load, show the correct `sizes` attribute for a full-width image, a half-width sidebar image, and a card grid item. Calculate the exact byte savings from correct `sizes` on a typical page load.""",

"""**Task (Code Generation):**
Build a `<FeatureGate>` component for Next.js that enables/disables features per-user in Server Components:

```tsx
<FeatureGate feature="new-checkout" fallback={<OldCheckout />}>
  <NewCheckout />
</FeatureGate>
```

Requirements:
- Feature flags fetched server-side (no client flash)
- User targeting: percentage rollout, user ID allowlist, beta flag
- Flag values passed from Middleware to Server Components via request headers
- Client Component support with a `useFeatureFlag` hook backed by the same flags
- TypeScript: `feature` prop is typed as `keyof FeatureFlags` (no magic strings)""",

"""**Debug Scenario:**
A Next.js App Router app's build fails with:

```
Error: Dynamic server usage: Route /dashboard couldn't be rendered statically because it used `cookies`.
```

The dashboard uses `cookies()` to read the auth session. The build tried to pre-render `/dashboard` statically.

Explain Next.js's static/dynamic rendering heuristics: which APIs force dynamic rendering (`cookies`, `headers`, `searchParams`, `noStore()`), how to opt-in to dynamic rendering explicitly with `export const dynamic = 'force-dynamic'`, and when to use PPR (Partial Pre-rendering) to static-render the shell and dynamically render the personalized parts.""",

"""**Task (Code Generation):**
Implement a Next.js Edge Config-backed feature flag system. Edge Config is read in O(1) time from Vercel's edge network:

```ts
// middleware.ts (edge runtime):
const flags = await getEdgeConfig(); // ~1ms, no database call
const isNewDesignEnabled = flags['new-design'] === true;
```

Show: the Vercel Edge Config SDK setup, the Middleware integration, how to update flags via Vercel API (for instant propagation without redeployment), local development with a `.env` fallback, and TypeScript types for the Edge Config schema.""",

"""**Debug Scenario:**
A Next.js app using `app/` directory has a Server Action that updates a database record. After the action runs, the UI doesn't update even though `revalidatePath('/')` is called.

```ts
'use server';
async function updateUser(data: FormData) {
  await db.user.update({ where: { id }, data: { name: data.get('name') } });
  revalidatePath('/profile');
  // UI still shows old name
}
```

The page is at `/profile/[userId]`. `revalidatePath('/profile')` invalidates `/profile` but not `/profile/[userId]`. Show the correct revalidation: `revalidatePath('/profile/[userId]', 'page')`, an alternative using `revalidateTag`, and when `redirect()` is more appropriate than `revalidatePath()`.""",

"""**Task (Code Generation):**
Build a type-safe API client for a Next.js app using Route Handler type inference:

```ts
// Infer types from Route Handler:
const client = createTypedClient<typeof GET>('/api/users');
const { data } = await client.get({ query: { page: 1 } });
// data is typed as UsersResponse ✓
```

Show: the Route Handler type export pattern, the `createTypedClient` factory that infers request/response types, how to handle Next.js's `NextResponse.json()` return type, and the `zod` schema validation on both client and server sides for the same schema definition.""",

"""**Debug Scenario:**
A Next.js app with Server Components fetches user data in a layout:

```tsx
// app/dashboard/layout.tsx (Server Component)
const user = await getUser(session.userId);
// Passes user to all child pages
```

The user data is 3KB and gets fetched on every navigation within `/dashboard`. The fetch has `cache: 'force-cache'` but the cache is invalidated on every navigation because `session.userId` changes reference (it's parsed fresh from the cookie each time).

Show how `JSON.stringify(session.userId) === JSON.stringify(previousUserId)` for cache key comparison, why React's `cache()` deduplicates within a render but not across navigations, and the correct approach using proper cache tags.""",

"""**Task (Code Generation):**
Implement a Next.js app with database-backed sessions (no JWT) using HTTP-only cookies:

```ts
// app/api/auth/login/route.ts
const sessionId = crypto.randomUUID();
await db.sessions.create({ sessionId, userId, expiresAt: Date.now() + SESSION_TTL });
const response = NextResponse.json({ ok: true });
response.cookies.set('session', sessionId, { httpOnly: true, secure: true, sameSite: 'lax' });
```

Show: session creation/validation/deletion Route Handlers, Middleware that validates the session on every request (reads from database), session rotation on sensitive operations, absolute vs sliding expiry, and CSRF protection (why `sameSite: 'lax'` + `Origin` header check covers most cases).""",

"""**Debug Scenario:**
A Next.js app's ISR (Incremental Static Regeneration) pages are being regenerated every 30 seconds as configured, but Vercel logs show 10x more revalidation invocations than expected. Each page view seems to trigger a background revalidation even when the page isn't stale.

Diagnose: Vercel's edge caches across multiple regions each have their own staleness timers. A page stale in 5 regions triggers 5 revalidations. Show how to reduce revalidation traffic with `revalidate = false` + tag-based on-demand revalidation, and the Vercel CDN override headers that prevent per-region re-generation.""",

"""**Task (Code Generation):**
Build a Next.js App Router app with full internationalization using `next-intl`:

```
app/
  [locale]/
    layout.tsx  ← loads messages for locale
    page.tsx
middleware.ts ← detects locale, redirects /about → /en/about
```

Show: the locale detection in Middleware (Accept-Language + cookie + path), the `[locale]` segment, loading translation messages in Server Components, the `useTranslations` hook in Client Components, and `generateStaticParams` to pre-build all 5 supported locales at build time.""",

"""**Debug Scenario:**
A Next.js Route Handler that streams a large CSV file from the database runs fine locally but crashes on Vercel with a timeout after 30 seconds (Vercel's maximum function execution time for the Pro plan).

The route fetches 100,000 rows, builds a CSV string in memory, then sends it. Show: the streaming response pattern using `ReadableStream` + `TransformStream` for database cursor-based streaming, how to set `export const maxDuration = 60` for long-running functions, and why the streaming approach avoids the memory spike that crashes the function.""",

"""**Task (Code Generation):**
Implement a content management workflow in Next.js with draft/publish states:

```ts
// Preview mode: editors see unpublished draft content
// app/api/preview/route.ts
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const secret = searchParams.get('secret');
  if (secret !== process.env.PREVIEW_SECRET) return new Response('Unauthorized', { status: 401 });
  
  const response = NextResponse.redirect(targetUrl);
  response.cookies.set('__prerender_bypass', draftModeToken);
  return response;
}
```

Show: enabling/disabling Draft Mode with `draftMode()`, fetching draft vs published content based on draft mode, the preview URL workflow for editors, and securing preview routes against public access.""",

"""**Debug Scenario:**
A Next.js app uses `next/headers`'s `headers()` function inside a utility function called from both Server Components and Client Components. The utility crashes with an error when called from a Client Component:

```
Error: headers() cannot be called from a Client Component
```

Show how to create a server-only utility using the `server-only` package (importing it throws at build time if a Client Component tries to import it), the correct pattern of passing pre-fetched headers to client utilities as props, and the `'use server'` vs `server-only` distinction.""",

"""**Task (Code Generation):**
Build a `useNextRouter` hook that wraps Next.js App Router navigation with transition states and scroll management:

```ts
const { navigate, isPending, currentPath } = useNextRouter();

await navigate('/dashboard', {
  scroll: 'top',               // scroll to top after navigation
  transition: 'slide-left',     // animate page transition
  prefetch: true,              // prefetch on mount
});
```

Show: `useTransition` for pending state, `startTransition` + `router.push()` for non-blocking navigation, custom CSS transitions between routes using route change events, and scroll position management with `scrollTo` after navigation commit.""",

"""**Debug Scenario:**
A Next.js app uses `fetch` inside a Server Component with `cache: 'force-cache'`. After the developer runs `revalidatePath('/')`, they expect all data on the home page to refresh. But some data is still stale — specifically, data from `fetch('/api/products')` which uses a different cache tag.

`revalidatePath('/')` only invalidates the route cache for `/`, not the fetch cache entries. The fetch cache uses its own tags. Show: the difference between `revalidatePath` (route cache) and `revalidateTag` (fetch cache), how to tag a `fetch` call with `{ next: { tags: ['products'] } }`, calling `revalidateTag('products')` to invalidate that specific fetch cache entry, and when to use each approach.""",

]
