"""
snippets/q_nextjs.py - 28 Next.js Advanced questions
"""

Q_NEXTJS = [

"""**Context:**
Our dashboard has a RelativeTime component showing "3 minutes ago" timestamps rendered in a Server Component and hydrated on the client.

**Observed Issue:**
We get hydration mismatch warnings. Both server and client show "4 minutes ago" visually, but React still warns. Millisecond timing drift between server render and hydration causes the mismatch.

**Specific Ask:**
What's the correct Next.js 14 pattern for time-sensitive content that differs between server and client? Is suppressHydrationWarning, a useEffect-deferred render, or converting to a Client Component with a stable initial value the right approach? How does each affect streaming and Lighthouse scores?""",

"""**Context:**
Our dashboard migrated to App Router with RSC + streaming. Multiple Suspense boundaries exist on the page. The KPI section is above-fold but streams last because its query is slowest (900ms vs 400ms for the table).

**Observed Issue:**
React streams DataTableSection first since it resolves first, even though KPI is visually more important. The KPI skeleton stays visible longer than it should.

**Specific Ask:**
Is there a way to hint React's streaming scheduler to prioritize KPI despite it resolving later? Or is the only fix making the KPI query faster? How does React determine stream order with multiple sibling Suspense boundaries -- strictly promise-resolution order?""",

"""**Context:**
We're migrating our DataTable to RSC. The table needs row selection state (useState) but row data should come from server-side DB queries.

**Observed Issue:**
Adding 'use client' to DataTable converts it and all its children to client components. Row components that could be pure RSC now ship to the client, inflating our JS bundle by 80KB.

**Specific Ask:**
What's the correct RSC composition pattern for mixing server data with client interactivity? Is the "pass server components as children to client components" pattern the right approach? What are its limitations and how do you type the children prop when it carries RSC output?""",

"""**Context:**
We use Next.js Middleware to enforce JWT-based RBAC, redirecting users without the required permission. It runs and works on full page loads.

**Observed Issue:**
When using router.push() for client-side navigation in App Router, the middleware doesn't seem to run -- users can navigate to /dashboard/admin client-side without the middleware redirect triggering.

**Specific Ask:**
Is Next.js Middleware guaranteed to run on every client-side navigation in App Router? If not, where should client-side permission enforcement live -- a layout Server Component, a route guard hook? How do you prevent a determined user from bypassing client-side guards entirely?""",

"""**Context:**
Our route handler at /api/rows uses export const revalidate = 30. After a user creates a new row via POST, the GET still returns stale data for up to 30 seconds.

**Observed Issue:**
Calling revalidatePath('/dashboard') in the Server Action after POST doesn't flush the route handler's cache. The two caches appear to be separate layers.

**Specific Ask:**
What's the difference between revalidatePath, revalidateTag, and the route segment revalidate config in Next.js 14? Which one controls a route handler's cached response? How do you tag a route handler fetch so a specific mutation can invalidate only the relevant cache entry?""",

"""**Context:**
We use a Server Action to handle form submission. When the action fails, we need to show an inline error without losing form values.

**Code:**
```tsx
async function saveReport(formData: FormData) {
  const result = await db.save(parse(formData));
  if (!result.ok) throw new Error(result.message); // propagates to error.tsx
}
```

**Observed Issue:**
When the action throws, Next.js sends the error to the nearest error.tsx boundary, wiping out the form. We need the error returned to the form component, not thrown.

**Specific Ask:**
What's the correct Server Action error-handling pattern that keeps the user on the form? Should we return a discriminated union { ok: true } | { ok: false; error: string } instead of throwing? How does this interact with useFormState / useActionState in React 19?""",

"""**Context:**
We enabled Partial Prerendering (PPR) on our dashboard page. The static shell should prerender at build time while the dynamic DataTable streams in.

**Observed Issue:**
The build fails with "Dynamic server usage: cookies() was called." The cookies() call is deep in a component we assumed was static.

**Specific Ask:**
How does Next.js determine what's "static" vs "dynamic" for PPR? Is any component that transitively calls cookies(), headers(), or searchParams() automatically dynamic? How do you audit a component tree for all dynamic call sites without triggering build errors one by one?""",

"""**Context:**
Our /dashboard/reports/[id] route uses generateStaticParams. We have 80,000 reports and the build times out trying to generate all static pages.

**Code:**
```ts
export async function generateStaticParams() {
  const ids = await db.reports.findMany({ select: { id: true } }); // 80k rows
  return ids.map(({ id }) => ({ id: String(id) }));
}
```

**Specific Ask:**
What's the recommended strategy for generateStaticParams at scale? Should we only pre-generate the top N most visited pages and use fallback: 'blocking' for the rest? How does Next.js 14 handle ISR for the non-pregenerated pages when they're first accessed?""",

"""**Context:**
We have a parallel route for a notification drawer (@notifications) with its own loading.tsx. It shows a skeleton on initial hard navigation correctly.

**Observed Issue:**
During client-side navigation between routes, the drawer doesn't show its loading state again. It shows stale content until the new data arrives, with no visual feedback.

**Specific Ask:**
Are parallel route loading states only shown on hard (full page) navigation, not soft (client-side) navigation? How do you show a drawer-level loading indicator during client-side route transitions without converting the drawer to a client component with manual loading state?""",

"""**Context:**
We use an intercepting route to show a report detail modal on client navigation but the full page on direct URL access. The modal works on client nav, but refreshing the modal URL shows the full page, which is expected.

**Observed Issue:**
The URL while in modal-view is /dashboard/reports/123. Refreshing shows the full page at the same URL. Users are confused about what the URL represents.

**Specific Ask:**
Is this a fundamental limitation of intercepting routes -- they only intercept client-side navigations? What's the UX pattern to handle this gracefully? Should modal state live in a query param instead, so the base route always renders consistently?""",

"""**Context:**
User preferences are fetched in the root App Router layout. Navigating between /dashboard/* routes seems to re-run this data fetch on every route transition.

**Observed Issue:**
Network tab shows the user preferences fetch firing on every client navigation, even though preferences don't change within a session.

**Specific Ask:**
How does Next.js 14 App Router handle layout data re-fetching during client navigation? Is layout data cached between navigations, or re-fetched? Should we use React cache(), a long revalidate time, or move preferences to cookies to avoid the re-fetch?""",

"""**Context:**
We need /dashboard/reports/[id] to always serve fresh data (no caching) because the report updates in real-time. We also have generateStaticParams for SEO pre-generation.

**Code:**
```ts
export const dynamic = 'force-dynamic';
export async function generateStaticParams() { ... } // conflict?
```

**Observed Issue:**
Using force-dynamic with generateStaticParams causes a build warning. We're unclear which takes precedence.

**Specific Ask:**
What's the precedence order among dynamic, revalidate, and generateStaticParams in Next.js 14? If force-dynamic is set, does generateStaticParams still run? Can we pre-render a static shell for fast initial load while keeping data always fresh on request?""",

"""**Context:**
We use next/image for product screenshots in a responsive grid. Images display at 33% viewport width on desktop, 50% on tablet, 100% on mobile.

**Code:**
```tsx
<Image src={screenshot} alt="..." fill sizes="100vw" />
```

**Observed Issue:**
Lighthouse flags images are much larger than their display size -- a 400px-wide image is served at 1920px because sizes="100vw" tells next/image the image takes the full viewport.

**Specific Ask:**
How do you correctly write the sizes attribute for a responsive grid where image width varies by breakpoint? Does next/image's optimization use the sizes attribute to pick the right srcset entry, and what breakpoints does it use?""",

"""**Context:**
We use next/font with Inter (variable font) to self-host and avoid layout shift. The variable font woff2 is 310KB, causing FOUT on slow mobile connections.

**Code:**
```ts
const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });
```

**Observed Issue:**
The full variable font file is always downloaded even though we only use weights 400 and 600, and only the latin subset.

**Specific Ask:**
Does next/font support subsetting variable fonts by weight range or unicode range beyond the built-in subset options? Is the correct approach to switch from variable font to static weights for body text and only load the variable font for display text?""",

"""**Context:**
Our /report/[id] page calls the same getReport function in both generateMetadata and the page component, resulting in two DB calls per page render.

**Code:**
```ts
export async function generateMetadata({ params }) {
  const report = await getReport(params.id); // DB call 1
  return { title: report.title };
}
export default async function Page({ params }) {
  const report = await getReport(params.id); // DB call 2
}
```

**Specific Ask:**
Does Next.js 14 deduplicate fetch calls between generateMetadata and the page component if they share the same cache key? Does React's cache() function work across the metadata generation and page render boundary? What's the recommended pattern for sharing fetched data between the two?""",

"""**Context:**
We read session cookies in an RSC to personalize a dashboard section. After adding cookies(), our page opts into dynamic rendering entirely.

**Code:**
```ts
const session = cookies().get('session');
const data = await getDataForUser(session?.value);
```

**Observed Issue:**
The static parts of the page (marketing header, nav) are now also dynamically rendered, losing CDN cacheability.

**Specific Ask:**
Is cookies() a dynamic API that always forces the entire page into dynamic rendering in Next.js 14? How do you isolate the cookie-reading logic so only the personalized section is dynamic while the rest remains static? Is PPR the only solution or can async component boundaries help?""",

"""**Context:**
Our Middleware reads request.geo.country (Vercel Edge) to detect EU users for GDPR banner logic. This works in production but breaks in local dev and staging (non-Vercel).

**Observed Issue:**
request.geo is undefined outside Vercel, causing a runtime error in Middleware. We've added null guards but need a proper multi-environment strategy.

**Specific Ask:**
What's the right architecture for geo-dependent logic that needs to work across Vercel, local dev, and non-Vercel staging? Should geo detection move to a client-side check (MaxMind, ipinfo.io API) with a display delay? What are the latency and privacy tradeoffs of client-side vs. edge geo detection?""",

"""**Context:**
Our Middleware has a relatively expensive JWT decode on every request. Despite the matcher excluding static assets, some _next/static requests still hit the Middleware.

**Code:**
```ts
export const config = {
  matcher: ['/((?!api|_next/static|favicon.ico).*)'],
};
```

**Observed Issue:**
Network tab shows the JWT decode running even on some static chunk requests. Performance profiling shows this adds ~8ms to those requests.

**Specific Ask:**
Is the negative lookahead regex matcher the correct way to exclude _next/static from Next.js Middleware? Are there known edge cases where it fails? If Middleware runs on chunk requests, how significantly does it affect perceived performance vs. only adding latency to the first byte?""",

"""**Context:**
We use useSearchParams() to read URL filter state in a Client Component. Next.js requires it be wrapped in Suspense.

**Observed Issue:**
The Suspense fallback skeleton flashes briefly on every server-initiated navigation, even when the search params haven't changed and the component is already mounted client-side.

**Specific Ask:**
Why does useSearchParams require a Suspense boundary in Next.js 14 App Router? Is it related to streaming SSR where params may not exist in the initial server shell? What's the pattern to suppress the fallback flash on client navigations where the component is already rendered?""",

"""**Context:**
In an RSC page, three independent data fetches run sequentially due to sequential awaits, adding ~600ms to TTFB.

**Code:**
```tsx
const users = await getUsers();       // 200ms
const metrics = await getMetrics();   // 300ms
const alerts = await getAlerts();     // 100ms
```

**Specific Ask:**
Does using Promise.all for parallel RSC fetches interact correctly with Next.js's fetch deduplication? If we parallelize, does the entire page wait for the slowest fetch, or can individual Suspense boundaries stream as each promise resolves?""",

"""**Context:**
We're incrementally migrating from Pages Router to App Router. Pages in /pages and /app need to share a current-user Context.

**Observed Issue:**
Context providers in App Router layouts don't wrap Pages Router pages. We can't put a shared Provider at the application root because the two routers have separate React trees.

**Specific Ask:**
What's the recommended strategy for sharing state between Pages Router and App Router during migration? Should shared state live in cookies (readable by both routers' server code), URL params, or a module-level store? Is there an official Next.js migration pattern for this coexistence period?""",

"""**Context:**
We switched to Turbopack for local development (next dev --turbo). HMR improved dramatically but our internal @company/design-tokens package fails to compile.

**Observed Issue:**
The package uses a PostCSS transform and some Webpack-specific loader syntax. Turbopack throws "SWC cannot process this file" on the package's CSS entry.

**Specific Ask:**
What are the known limitations of Turbopack vs. Webpack as of Next.js 14 -- specifically around CSS, PostCSS, and custom loaders? Can you configure Turbopack to use Webpack for specific packages? Or must the package be updated to be Turbopack-compatible?""",

"""**Context:**
Our next.config.js rewrites /api/legacy/* to an old Express backend. In production, some paths cause an infinite redirect loop.

**Observed Issue:**
The legacy API server redirects certain paths back to the Next.js app domain. Next.js then rewrites those again to the legacy server. The loop continues until the request times out.

**Specific Ask:**
How do you detect and break out of rewrite-induced redirect loops in Next.js? Is there a way to mark a rewritten request so Next.js doesn't re-apply the rewrite rule on the return trip? Or should the fix be applied at the origin server?""",

"""**Context:**
We're evaluating Vercel Edge Config for feature flags to reduce Middleware latency vs. our LaunchDarkly SDK (~50ms per request vs. <1ms for Edge Config).

**Observed Issue:**
Edge Config has a 512KB limit and no native targeting rules (percentage rollouts, user segment targeting). We'd need to implement targeting logic ourselves.

**Specific Ask:**
For a 200k DAU app with 30+ feature flags and user-segment targeting, is Edge Config a viable LaunchDarkly replacement or only suitable for simple on/off flags? What's the pattern for percentage rollouts in Edge Config? For which flag capabilities would you still keep LaunchDarkly?""",

"""**Context:**
We use output: standalone in next.config.js to produce a minimal Docker image. The resulting image is 1.8GB despite standalone supposedly including only necessary files.

**Code:**
```dockerfile
FROM node:20-alpine
COPY .next/standalone ./
COPY .next/static ./.next/static
RUN node server.js
```

**Observed Issue:**
Native binary packages (sharp for image optimization, bcrypt) are included with all platform variants. Building for linux/arm64 includes linux/x64 binaries too.

**Specific Ask:**
What's the correct multi-stage Dockerfile pattern for Next.js standalone to minimize image size? How do you handle native binaries that must match the target platform? And does standalone correctly exclude unnecessary devDependencies from the final image?""",

"""**Context:**
Our Server Actions mutate data and then call revalidatePath(). The mutation works but the UI doesn't update until the user manually refreshes.

**Observed Issue:**
revalidatePath('/dashboard') is called inside the Server Action but the dashboard page doesn't re-fetch after the form submission. The Next.js Router Cache is serving the stale page.

**Specific Ask:**
What's the interaction between Server Action revalidation and the Next.js Router Cache (client-side) vs. the Data Cache (server-side)? Does revalidatePath clear both? Is router.refresh() needed on the client after a Server Action mutations, or should revalidatePath alone be sufficient?""",

"""**Context:**
We want to use Next.js 14 Parallel Routes to build a split-pane layout where the left panel shows a list and the right panel shows the selected item detail. Both panels should be independently navigable (deep-linkable).

**Observed Issue:**
Setting up @list and @detail parallel route slots works for the initial URL. But client-side navigation within @detail (e.g., navigating to the next report) updates the URL but doesn't update the @list slot -- it stays on the previous list page.

**Specific Ask:**
How does Next.js handle URL synchronization across multiple parallel route slots during client navigation? When navigating within @detail, does @list need to explicitly define its own navigation? Is this pattern the right use case for Parallel Routes or should we use a different approach for split-pane?""",

"""**Context:**
We use ISR (Incremental Static Regeneration) with revalidate: 60 on our blog listing page. After publishing a new post, the listing page isn't updating even after waiting several minutes past the revalidation window.

**Observed Issue:**
The stale-while-revalidate model means the first request after the revalidation window triggers a background regeneration, but serves the stale page. The NEXT request should get the fresh page. We're waiting 10+ minutes and still seeing the old content.

**Specific Ask:**
What conditions must be true for ISR background revalidation to actually fire? Does it require an actual user request to trigger, or does Next.js poll proactively? In a multi-region edge deployment (Vercel Edge Network), does each edge node maintain its own ISR state independently -- meaning stale content can persist per-region for much longer than the revalidate window suggests?""",

]
