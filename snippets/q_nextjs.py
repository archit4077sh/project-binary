"""
snippets/q_nextjs.py — BATCH 5: 28 brand-new Next.js questions
Zero overlap with batch1, batch2, batch3, or batch4 archives.
"""

Q_NEXTJS = [

"""**Task (Code Generation):**
Implement a Next.js Partial Prerendering (PPR) page where static shell and dynamic content are combined:

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react';
import { StaticHero } from './StaticHero';        // prerendered at build
import { LiveMetrics } from './LiveMetrics';       // dynamic at runtime
import { RecentActivity } from './RecentActivity'; // dynamic per-user

export default function DashboardPage() {
  return (
    <>
      <StaticHero />
      <Suspense fallback={<MetricsSkeleton />}>
        <LiveMetrics />
      </Suspense>
      <Suspense fallback={<ActivitySkeleton />}>
        <RecentActivity />
      </Suspense>
    </>
  );
}
```

Show: enabling PPR via `experimental.ppr: true` in `next.config.js`, `unstable_noStore()` inside dynamic components, the static shell being served from CDN while dynamic holes are streamed, and measuring the TTFB improvement with Vercel Speed Insights.""",

"""**Debug Scenario:**
A Next.js app using `next-auth` has a redirect loop. After login, users are redirected to `/auth/signin?callbackUrl=%2Fauth%2Fsignin` — the callback URL is pointing to the sign-in page itself:

```ts
// middleware.ts:
export function middleware(req: NextRequest) {
  const token = req.cookies.get('next-auth.session-token');
  if (!token) {
    return NextResponse.redirect(new URL('/auth/signin', req.url));
  }
}
```

The middleware matches ALL routes including `/auth/signin`, creating an infinite redirect. Show: excluding auth routes from middleware with:

```ts
export const config = {
  matcher: ['/((?!auth|_next/static|_next/image|favicon.ico).*)'],
};
```

And the `authorized` callback in `next-auth` config as the idiomatic way to protect routes without manual middleware redirect logic.""",

"""**Task (Code Generation):**
Build a Next.js image optimization pipeline using `next/image` with custom loaders:

```tsx
// For self-hosted images using Cloudflare Images:
const cloudflareLoader: ImageLoader = ({ src, width, quality }) => {
  return `https://imagedelivery.net/ABC/${src}/w=${width},q=${quality ?? 75}`;
};

<Image
  src="profile-photo-id"
  loader={cloudflareLoader}
  width={400}
  height={400}
  alt="User profile"
  sizes="(max-width: 768px) 100vw, 400px"
  priority={isAboveFold}
/>
```

Show: the custom loader interface, `sizes` attribute for responsive images (let browser pick the right size), `priority` for LCP images (preloads the image), `placeholder="blur"` with `blurDataURL` for LQIP, and the `remotePatterns` config in `next.config.js` for allowing external image domains.""",

"""**Debug Scenario:**
A Next.js App Router app uses `revalidatePath('/products')` in a Server Action after a product is updated, but the product list page doesn't reflect the update for 30+ seconds.

`revalidatePath` marks the path for on-demand revalidation, but only takes effect AFTER the NEXT request to that path — not immediately for the current response. Also, the route may be cached at multiple layers (CDN, Next.js data cache, router cache).

Show: the difference between `revalidatePath` (on-demand re-render on next request) and `revalidateTag` (invalidate by cache tag across paths), clearing the client-side Router Cache using `router.refresh()` after the Server Action completes, and using Vercel's Purge Cache API for CDN-level cache invalidation.""",

"""**Task (Code Generation):**
Implement a streaming RSC response for a search feature that shows results progressively:

```tsx
// app/search/page.tsx
export default async function SearchPage({ searchParams }) {
  const query = searchParams.q;
  return (
    <div>
      <SearchBar initialQuery={query} />
      <Suspense fallback={<QuickResultsSkeleton />}>
        <QuickResults query={query} limit={5} />
      </Suspense>
      <Suspense fallback={<FullResultsSkeleton />}>
        <FullResults query={query} />  {/* slower, more comprehensive */}
      </Suspense>
    </div>
  );
}
```

Show: `QuickResults` using a fast Redis search, `FullResults` using a slower Elasticsearch query, both as async Server Components, `<SearchBar>` as a Client Component with `useOptimistic` for immediate UI feedback, and HTTP streaming behavior (browser renders Quick Results before Full Results completes).""",

"""**Debug Scenario:**
A Next.js middleware reads request headers to detect the user's country (`x-vercel-ip-country`) and redirects to a localized path. In local development, the header is always absent, so developers are redirected to the default locale regardless of their testing intent.

Show: a dev-mode fallback that reads `?country=US` from the query string when the Vercel header is absent, a mock middleware for local development that injects the header from an environment variable (`process.env.MOCK_COUNTRY`), and a `__test_country` cookie override that takes precedence over the header for QA testing of specific locales.""",

"""**Task (Code Generation):**
Build a Next.js API route with streaming responses using `ReadableStream`:

```ts
// app/api/ai-chat/route.ts
export async function POST(request: Request) {
  const { messages } = await request.json();

  const stream = new ReadableStream({
    async start(controller) {
      const openai = new OpenAI();
      const completion = await openai.chat.completions.create({
        model: 'gpt-4',
        messages,
        stream: true,
      });

      for await (const chunk of completion) {
        const text = chunk.choices[0]?.delta?.content ?? '';
        controller.enqueue(new TextEncoder().encode(text));
      }
      controller.close();
    },
  });

  return new Response(stream, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}
```

Show: the client-side reader using `response.body.getReader()`, `ReadableStreamDefaultReader.read()` loop, accumulating chunks into a `useState` string, and the `use` hook alternative with React's new streaming data support.""",

"""**Debug Scenario:**
A Next.js page with `generateStaticParams` for a dynamic route (`[slug]`) fails to build because one of the slugs contains a forward slash: `"category/electronics"`:

```ts
export async function generateStaticParams() {
  return products.map(p => ({ slug: p.slug }));
  // slug: "category/electronics" → crashes build
}
```

Next.js treats `/` in params as a path separator — it tries to render `/products/category/electronics` instead of treating the whole thing as `slug`. Show: using catch-all routes (`[...slug]`) with `slug: ['category', 'electronics']` as an array, URL-encoding the slash (`slug: encodeURIComponent('category/electronics')`), or restructuring the URL to use separate path segments (`/products/[category]/[slug]`).""",

"""**Task (Code Generation):**
Implement a Next.js analytics middleware that tracks page views without blocking rendering:

```ts
// middleware.ts
export function middleware(request: NextRequest) {
  // Track the page view, then immediately continue:
  const headers = new Headers(request.headers);
  headers.set('x-page-view-id', crypto.randomUUID());

  // Non-blocking analytics via waitUntil:
  ctx.waitUntil(
    trackPageView({
      url: request.url,
      userAgent: request.headers.get('user-agent'),
      country: request.geo?.country,
    })
  );

  return NextResponse.next({ request: { headers } });
}
```

Show: Vercel Edge Runtime's `waitUntil` for non-blocking async work in middleware, the `EdgeRuntime` type for the middleware context, using `fetch` to send analytics to a background endpoint, the `x-` custom header forwarding to Server Components, and the Segment/Mixpanel server-side event API format.""",

"""**Debug Scenario:**
A Next.js app has a Server Component that fetches user data and a Client Component child that displays it. When the user updates their profile (via a Server Action), the Server Component re-renders but the Client Component shows a stale `user` prop for a few seconds:

```tsx
// Server Component:
async function ProfilePage() {
  const user = await getUser(); // re-fetches after Server Action
  return <ProfileEditor user={user} />;  // Client Component
}
```

The Client Component receives fresh props from the Server Component, but React's router cache still serves the old rendered version of the Server Component tree. Show: calling `router.refresh()` in the Client Component after a successful Server Action mutation, using the `useTransition` + Server Action pattern where the Server Action returns updated state and the transition updates the UI, and the `redirect()` function from `next/navigation` which forces a fresh Server Component render.""",

"""**Task (Code Generation):**
Build a `useNextRouter` hook that wraps `useRouter` with type-safe query parameters:

```ts
const router = useNextRouter({
  schema: {
    page:     z.coerce.number().default(1),
    sort:     z.enum(['asc', 'desc']).default('desc'),
    category: z.string().optional(),
    tags:     z.array(z.string()).default([]),
  },
});

const { params, setParam, setParams } = router;
// params.page: number (not string!)
// params.tags: string[] (comma-separated in URL parsed to array)

setParam('page', 2);             // updates URL: ?page=2
setParams({ sort: 'asc', page: 1 }); // merges with existing params
```

Show: reading from `useSearchParams()`, Zod parsing with defaults, the `setParam`/`setParams` that call `router.push` with `shallow: true`, and TypeScript inference of the params type from the schema.""",

"""**Debug Scenario:**
A large Next.js monorepo with 200 pages takes 45 minutes to run `next build` in CI. Turborepo is used, but the build cache is missing from CI on the first run.

Show: configuring Turborepo remote cache with `TURBO_TOKEN` and `TURBO_TEAM` environment variables for persistent caching across CI runs, setting up `next build` as a Turborepo task that depends on TypeScript compilation (`"dependsOn": ["^tsc"]`), using `next build --no-lint` in CI jobs that run ESLint separately, and `turbo prune --scope=my-app` to build only the affected workspace in a monorepo.""",

"""**Task (Code Generation):**
Implement a `generateSitemap` function that produces a dynamic sitemap with priorities:

```ts
// app/sitemap.ts
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const [pages, posts, products] = await Promise.all([
    getStaticPages(),
    getPublishedPosts(),
    getActiveProducts(),
  ]);

  return [
    { url: 'https://example.com', changeFrequency: 'monthly', priority: 1.0, lastModified: new Date() },
    ...posts.map(p => ({
      url: `https://example.com/blog/${p.slug}`,
      lastModified: p.updatedAt,
      changeFrequency: 'weekly' as const,
      priority: 0.8,
    })),
    ...products.map(p => ({
      url: `https://example.com/products/${p.slug}`,
      lastModified: p.updatedAt,
      changeFrequency: 'daily' as const,
      priority: 0.9,
    })),
  ];
}
```

Show: the `MetadataRoute.Sitemap` TypeScript type, splitting into multiple sitemaps using a sitemap index (for > 50,000 URLs), and configuring `robots.txt` to reference the sitemap.""",

"""**Debug Scenario:**
A Next.js app uses `cookies().set('session', token)` inside a Server Component to set a cookie after authentication. The cookie is never set in the browser:

```ts
// Server Component:
async function LoginPage() {
  const token = await getToken();
  cookies().set('session', token); // silently fails!
  redirect('/dashboard');
}
```

`cookies().set()` can only be called in Server Actions, Route Handlers, or Middleware — NOT in Server Components (which are read-only during render). Show: moving the cookie-setting to a Server Action that the login form submits to, or a Route Handler (`POST /api/login`) that returns `Set-Cookie` headers, and why Server Component rendering is write-forbidden for cookies and headers.""",

"""**Task (Code Generation):**
Build a Next.js error monitoring integration with structured error context:

```ts
// app/global-error.tsx
'use client';
export default function GlobalError({ error, reset }: { error: Error; reset: () => void }) {
  useEffect(() => {
    reportError(error, {
      component: 'GlobalError',
      url: window.location.href,
      userId: getCachedUser()?.id,
      buildId: process.env.NEXT_PUBLIC_BUILD_ID,
      severity: 'critical',
    });
  }, [error]);
  
  return (
    <html><body>
      <h1>Something went wrong</h1>
      <button onClick={reset}>Try again</button>
    </body></html>
  );
}
```

Show: Sentry integration with `Sentry.captureException`, the difference between `error.tsx` (within root layout) and `global-error.tsx` (replaces root layout), `next.config.js` `sentry` plugin for source maps, and the `instrumentation.ts` file for server-side Sentry initialization.""",

"""**Debug Scenario:**
A Next.js route `app/api/export/route.ts` streams a large CSV file. In production on Vercel, the response is truncated at exactly 4.5MB. The same export works fine on the local dev server.

Vercel has a 4.5MB response body limit for Serverless Functions. Show: rewriting the export as an Edge Function (no response size limit, streaming is native), chunking the export into paginated requests (client downloads 1MB pages and concatenates), or generating the export to S3/R2 in a background job and returning a presigned download URL instead of streaming it directly.""",

"""**Task (Code Generation):**
Implement a type-safe Next.js environment variable system:

```ts
// env.ts — server-side only
import { z } from 'zod';

const serverEnvSchema = z.object({
  DATABASE_URL:      z.string().url(),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
  SENDGRID_API_KEY:  z.string(),
  NODE_ENV:          z.enum(['development', 'test', 'production']),
});

const publicEnvSchema = z.object({
  NEXT_PUBLIC_API_URL:    z.string().url(),
  NEXT_PUBLIC_GA_ID:      z.string().optional(),
});

export const env = serverEnvSchema.merge(publicEnvSchema).parse(process.env);
// Type error if DATABASE_URL is undefined or wrong format:
const db = connect(env.DATABASE_URL);
```

Show: separate client/server schemas, the `NEXT_PUBLIC_` prefix requirement for client-side variables, validation at startup (fails fast if env is misconfigured), and preventing server-side env vars from leaking to client bundles.""",

"""**Debug Scenario:**
A Next.js page using `generateMetadata` returns dynamic `og:image` metadata, but social media crawlers (Twitter, LinkedIn) still show the default fallback image:

```ts
export async function generateMetadata({ params }) {
  const post = await getPost(params.slug);
  return {
    openGraph: {
      images: [{ url: `https://example.com/og?title=${post.title}` }],
    },
  };
}
```

Show: verifying with Facebook's Sharing Debugger / Twitter Card Validator that the `og:image` URL is accessible by crawlers (authentication, rate limiting, or CORS may block it), ensuring the OG image endpoint returns the correct `Content-Type: image/png` header, using `ImageResponse` from `next/og` for server-rendered OG images, and setting explicit `width`/`height` on the image metadata object (required by some platforms).""",

"""**Task (Code Generation):**
Build a Next.js route handler for webhook processing with signature verification:

```ts
// app/api/webhooks/github/route.ts
export async function POST(request: Request) {
  const rawBody = await request.text(); // must use text(), not json()
  const signature = request.headers.get('x-hub-signature-256');
  
  if (!verifyGitHubSignature(rawBody, signature, process.env.GITHUB_WEBHOOK_SECRET!)) {
    return new Response('Unauthorized', { status: 401 });
  }
  
  const event = JSON.parse(rawBody);
  const eventType = request.headers.get('x-github-event');
  await processGitHubEvent(event, eventType);
  
  return new Response('OK', { status: 200 });
}
```

Show: `crypto.createHmac('sha256', secret).update(rawBody).digest('hex')`, why you MUST use `request.text()` for signature verification (JSON parsing loses exact bytes), idempotency for retried webhooks (store event GUID in DB, skip if already processed), and the `export const dynamic = 'force-dynamic'` to prevent Next.js from caching POST routes.""",

"""**Debug Scenario:**
A Next.js 14 app with `next/font` renders fonts correctly on first load but after client-side navigation to a new page, the font briefly flashes to the system fallback before the correct font renders again:

The font is being fetched as a separate resource on each navigation instead of being cached. Show: next/font injects `<style>` tags during SSR that set the `@font-face` — on client navigation, the style injection happens after the first paint. The fix: ensuring `next/font` is used with `variable` CSS property and applied at the root layout level (not per-page), so the font stylesheet persists during client navigation, and verifying with Chrome DevTools' "Preserve log" that the font file is served from cache (HTTP 304).""",

"""**Task (Code Generation):**
Implement a Next.js API rate limiter using Edge Middleware with Redis:

```ts
// middleware.ts
export async function middleware(request: NextRequest) {
  if (request.nextUrl.pathname.startsWith('/api/')) {
    const ip = request.ip ?? request.headers.get('x-forwarded-for') ?? 'unknown';
    const { success, limit, remaining, reset } = await ratelimit.limit(ip);

    if (!success) {
      return new NextResponse('Too Many Requests', {
        status: 429,
        headers: {
          'X-RateLimit-Limit': String(limit),
          'X-RateLimit-Remaining': '0',
          'X-RateLimit-Reset': String(reset),
          'Retry-After': String(Math.ceil((reset - Date.now()) / 1000)),
        },
      });
    }
  }
  return NextResponse.next();
}
```

Show: Upstash Redis with `@upstash/ratelimit` (sliding window algorithm), the `Ratelimit.slidingWindow(10, '10 s')` config (10 req/10s), Edge Runtime compatibility (no Node.js APIs), and bypassing rate limits for authenticated users.""",

"""**Debug Scenario:**
A developer adds `loading.tsx` to `app/dashboard/` but the loading skeleton never appears — the page just appears to freeze until the data loads:

```
app/
  dashboard/
    loading.tsx   ← should show during navigation
    page.tsx      ← slow data fetch
```

`loading.tsx` works for DIRECT navigation to `/dashboard` but not for client-side navigation that was initiated from the same layout (the router cache serves the previous page instantly and the loading state is only shown when streaming starts). Show: the difference between client-side navigation (cached views) and direct navigation (loading.tsx shown), using `useRouter` + `startTransition` to show a manual loading indicator during client navigation, and the Next.js `router.prefetch` impact on when loading states are shown.""",

"""**Task (Code Generation):**
Build a Next.js middleware that implements feature flagging at the edge:

```ts
// middleware.ts
export async function middleware(request: NextRequest) {
  const flagKey = `feature-flags:${request.ip}`;
  const flags = await getEdgeFlags(flagKey);

  // A/B test: half of users get new checkout
  if (flags['new-checkout'] && request.nextUrl.pathname === '/checkout') {
    return NextResponse.rewrite(new URL('/checkout-v2', request.url));
  }

  // Beta feature: gradual rollout
  const response = NextResponse.next();
  response.headers.set('x-enabled-features', JSON.stringify(flags));
  return response;
}
```

Show: Vercel Edge Config for ultra-low latency flag reads (< 1ms), the rollout percentage hash function (consistent per-user assignment using `ip + featureName` hashed to 0-100), cookie-based flag override for QA, and the `x-enabled-features` header that Server Components read via `headers().get('x-enabled-features')`.""",

"""**Debug Scenario:**
A Next.js app deployed to Vercel fails with `Error: ENOENT: no such file or directory, open '/tmp/uploads/upload-1234.tmp'` after working correctly for 2 hours:

```ts
// Route handler:
await fs.writeFile(`/tmp/uploads/${filename}`, buffer);
// ... process file ...
const result = await processFile(`/tmp/uploads/${filename}`);
```

Vercel Serverless Functions have an ephemeral `/tmp` filesystem (512MB, cleared between invocations). If the write and read happen in DIFFERENT function invocations (load balancing routes different requests to different instances), the file won't exist.

Show: using S3/R2/Vercel Blob for cross-invocation file storage, passing the file buffer in memory within a single invocation (write → process → respond without writing to disk), and the `@vercel/blob` library for serverless file storage.""",

"""**Task (Code Generation):**
Implement a Next.js ISR with on-demand revalidation via tagged cache:

```ts
// app/products/[id]/page.tsx
export async function generateMetadata({ params }) {
  const product = await fetch(`/api/products/${params.id}`, {
    next: { tags: [`product:${params.id}`, 'products'] },
  });
}

export default async function ProductPage({ params }) {
  const product = await fetch(`https://api.example.com/products/${params.id}`, {
    next: { revalidate: 3600, tags: [`product:${params.id}`] },
  });
  return <ProductView product={await product.json()} />;
}

// app/api/revalidate/route.ts:
export async function POST(req) {
  const { tag, secret } = await req.json();
  if (secret !== process.env.REVALIDATION_SECRET) return new Response('Unauthorized', { status: 401 });
  await revalidateTag(tag);
  return new Response('Revalidated');
}
```

Show: calling the revalidation endpoint from a CMS webhook, revalidating all products at once with the `'products'` tag vs a single product with `'product:${id}'`, and monitoring cache behavior with `x-nextjs-cache` response header.""",

"""**Debug Scenario:**
A Next.js Server Component imports a module that uses `window` at import time (not inside a function), crashing the server:

```ts
// analytics-client.ts (third-party):
const tracker = new Analytics({ window: window.analytics }); // window access at module level
export { tracker };

// Server Component:
import { tracker } from './analytics-client'; // crash!
```

Server Components run in Node.js which has no `window`. Show: wrapping the import in a Client Component (`'use client'` — Client Components still SSR but only execute browser-specific code on the client), using dynamic import inside a `useEffect` (`const { tracker } = await import('./analytics-client')`), and the `typeof window !== 'undefined'` guard as a defensive pattern inside library code.""",

"""**Task (Code Generation):**
Implement a Next.js internationalized routing system with subdomain support:

```ts
// middleware.ts
export function middleware(request: NextRequest) {
  const subdomain = request.headers.get('host')?.split('.')[0];
  const locale = subdomainToLocale(subdomain) ?? getLocaleFromHeader(request);

  // Rewrite /products to /[locale]/products
  const url = request.nextUrl.clone();
  if (!url.pathname.startsWith(`/${locale}`)) {
    url.pathname = `/${locale}${url.pathname}`;
    return NextResponse.rewrite(url);
  }
}
```

Show: the `subdomainToLocale` mapping (`en.example.com → 'en'`, `de.example.com → 'de'`), `Accept-Language` header parsing, using `next-intl` middleware for locale detection and redirection, `next.config.js` `i18n` configuration with `defaultLocale` and `locales`, and the `<link rel="alternate" hreflang="...">` tags in metadata for SEO.""",

"""**Debug Scenario:**
A Next.js app prefetches data in `generateStaticParams` for a `[slug]` route but some pages take 8+ minutes to build because `generateStaticParams` returns 50,000 slugs and Next.js tries to generate all of them at build time:

```ts
export async function generateStaticParams() {
  const posts = await db.posts.findMany(); // returns 50,000 records
  return posts.map(post => ({ slug: post.slug }));
}
```

Show: returning only the most recent/popular 500 slugs from `generateStaticParams`, setting `export const dynamicParams = true` (allow on-demand ISR for slugs not pre-generated), using `revalidate` to periodically update static pages, and the build time comparison between full static generation vs selective static + ISR fallback.""",

]
