"""
snippets/q_nextjs.py — BATCH 7: 56 brand-new Next.js questions
Zero overlap with batches 1-6 archives.
"""

Q_NEXTJS = [

'''**Task (Code Generation):**
Implement a Next.js App Router layout that uses Parallel Routes for a dashboard with independent loading states:

```
app/
  dashboard/
    layout.tsx          ← Root layout with @team and @revenue slots
    @team/
      page.tsx          ← Team metrics (slow query ~2s)
      loading.tsx
    @revenue/
      page.tsx          ← Revenue chart (fast query ~200ms)
      loading.tsx
    page.tsx            ← Default (empty/redirect)
```

```tsx
// layout.tsx:
export default function DashboardLayout({
  children,
  team,
  revenue,
}: { children: React.ReactNode; team: React.ReactNode; revenue: React.ReactNode }) {
  return (
    <section className="dashboard-grid">
      <Suspense fallback={<TeamSkeleton />}>{team}</Suspense>
      <Suspense fallback={<RevenueSkeleton />}>{revenue}</Suspense>
    </section>
  );
}
```

Show: the `@folder` naming convention, `default.tsx` required for non-matching slots, independent streaming (revenue appears at 200ms, team at 2s without blocking each other), and URL independence (each slot can navigate independently via Intercepting Routes).''',

'''**Task (Code Generation):**
Build a Next.js `generateStaticParams` for a deeply nested dynamic route:

```
app/
  blog/
    [slug]/
      page.tsx
  docs/
    [version]/
      [...slug]/         ← Catch-all
        page.tsx
```

```ts
// docs/[version]/[...slug]/page.tsx:
export async function generateStaticParams() {
  const versions = ['v1', 'v2', 'v3'];
  const allPaths: { version: string; slug: string[] }[] = [];

  for (const version of versions) {
    const pages = await getDocPages(version);
    pages.forEach(page => {
      allPaths.push({ version, slug: page.path.split('/').filter(Boolean) });
    });
  }

  return allPaths;
}
```

Show: the `params` type for catch-all routes (`slug: string[]`), using `dynamicParams = false` to 404 on unknown paths (vs `dynamicParams = true` to SSR them), and `generateStaticParams` at the layout level for shared outer params.''',

'''**Task (Code Generation):**
Implement a `routeSegmentConfig` export pattern for granular caching control per route:

```tsx
// app/api/products/route.ts — Dynamic, no cache:
export const dynamic = 'force-dynamic';
export const revalidate = 0;

// app/api/categories/route.ts — ISR with tags:
export const revalidate = 3600;
export const fetchCache = 'force-cache';

export async function GET() {
  const categories = await fetch('https://api.example.com/categories', {
    next: { tags: ['categories'], revalidate: 3600 },
  });
  return Response.json(await categories.json());
}

// On category update (admin action):
import { revalidateTag } from 'next/cache';
revalidateTag('categories'); // Invalidates all cached fetches with this tag
```

Show: the complete set of route segment config exports (`dynamic`, `dynamicParams`, `revalidate`, `fetchCache`, `runtime`, `preferredRegion`), the `revalidateTag` vs `revalidatePath` difference, and the App Router's per-fetch caching granularity.''',

'''**Task (Code Generation):**
Build a Next.js middleware chain with multiple independent middlewares:

```ts
// middleware.ts — Chain approach since Next.js only supports one middleware file:
import { chain } from '@/lib/middleware-chain';
import { authMiddleware } from './middlewares/auth';
import { localeMiddleware } from './middlewares/locale';
import { rateLimiterMiddleware } from './middlewares/rate-limit';
import { securityHeadersMiddleware } from './middlewares/security';

export default chain([
  securityHeadersMiddleware,  // Add HSTS, CSP, XFO headers
  rateLimiterMiddleware,       // Rate limit before auth
  authMiddleware,              // Validate session
  localeMiddleware,            // Detect and redirect locale
]);

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};
```

Show: the `chain` helper that sequences middlewares (each calls `NextResponse.next()` or returns early), a `compose(middlewares)` implementation, and passing data between middlewares via `request.headers` set (`NextResponse.next({ request: { headers: newHeaders } })`).''',

'''**Task (Code Generation):**
Implement a Next.js Server Action with optimistic updates and error recovery:

```tsx
'use server';
export async function toggleTodo(id: string, currentDone: boolean) {
  const updated = await db.todo.update({
    where: { id },
    data: { done: !currentDone },
  });
  revalidatePath('/todos');
  return updated;
}

// Client component:
'use client';
function TodoItem({ todo }: { todo: Todo }) {
  const [optimisticTodo, addOptimistic] = useOptimistic(
    todo,
    (state, done: boolean) => ({ ...state, done })
  );

  return (
    <form action={async () => {
      addOptimistic(!optimisticTodo.done); // Optimistic update
      await toggleTodo(todo.id, todo.done);
    }}>
      <label>
        <input type="checkbox" checked={optimisticTodo.done} readOnly />
        {todo.text}
      </label>
      <button type="submit">Toggle</button>
    </form>
  );
}
```

Show: React 19's `useOptimistic`, the `action` attribute on `<form>` for progressive enhancement (works without JS), `revalidatePath` for cache invalidation, and `useFormStatus` for showing pending state during the server action.''',

'''**Task (Code Generation):**
Build a Next.js App Router authentication system using Iron Session:

```ts
// lib/session.ts:
import { getIronSession } from 'iron-session';

export async function getSession(req: Request | NextRequest, res: Response | NextResponse) {
  return getIronSession<SessionData>(req, res, {
    password: process.env.SESSION_SECRET!,
    cookieName: 'app-session',
    cookieOptions: {
      secure: process.env.NODE_ENV === 'production',
      httpOnly: true,
      sameSite: 'lax',
      maxAge: 60 * 60 * 24 * 7, // 1 week
    },
  });
}

// Route Handler:
export async function POST(req: Request) {
  const session = await getSession(req, new Response());
  const { email, password } = await req.json();
  const user = await validateCredentials(email, password);
  if (!user) return Response.json({ error: 'Invalid credentials' }, { status: 401 });
  session.userId = user.id;
  session.role = user.role;
  await session.save();
  return Response.json({ user: { id: user.id, email: user.email } });
}
```

Show: Iron Session's encrypted cookie (server-side session data encrypted in the cookie), `getServerSideSession` in RSC, and the middleware pattern for protecting routes.''',

'''**Task (Code Generation):**
Implement a Next.js `notFound` and `redirect` pattern with proper status codes:

```ts
// app/products/[slug]/page.tsx:
import { notFound, redirect } from 'next/navigation';

export default async function ProductPage({ params }: { params: { slug: string } }) {
  const product = await db.product.findUnique({ where: { slug: params.slug } });

  if (!product) notFound();  // Renders the nearest not-found.tsx

  if (product.redirectTo) {
    redirect(`/products/${product.redirectTo}`);  // 307 temporary in RSC
    // permanentRedirect(`/products/${product.redirectTo}`); // 308 permanent
  }

  return <ProductDetail product={product} />;
}

// app/products/not-found.tsx:
export default function NotFound() {
  return <div><h2>Product Not Found</h2><Link href="/products">Browse Products</Link></div>;
}
```

Show: `notFound()` throws a special error caught by the nearest `not-found.tsx`, `redirect()` throwing a special error (must not be in try/catch), `permanentRedirect()` for 308, and catching `notFound` and `redirect` in error boundaries.''',

'''**Task (Code Generation):**
Build a Next.js image optimization pipeline with `next/image` and custom loader:

```tsx
// Custom loader for Cloudinary:
const cloudinaryLoader = ({ src, width, quality }: ImageLoaderProps) =>
  `https://res.cloudinary.com/${process.env.NEXT_PUBLIC_CLOUDINARY_ID}/image/upload` +
  `/f_auto,c_limit,w_${width},q_${quality ?? 'auto'}` +
  `/${src}`;

<Image
  loader={cloudinaryLoader}
  src="products/hero.jpg"
  alt="Product hero"
  width={1200}
  height={630}
  priority              // LCP image — preload it
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  placeholder="blur"
  blurDataURL={product.lqip}
/>
```

Show: the `sizes` attribute for responsive images (srcset generation), `priority` for LCP images (adds `<link rel="preload">`), custom loader returning the correct CDN URL, and `next.config.js`'s `images.domains` vs `images.remotePatterns`.''',

'''**Task (Code Generation):**
Implement a Next.js App Router multi-tenant setup using subdomain routing in middleware:

```ts
// middleware.ts:
export function middleware(req: NextRequest) {
  const host = req.headers.get('host') ?? '';
  const subdomain = host.split('.')[0];

  // Rewrite the URL to the tenant-specific route:
  if (subdomain !== 'www' && subdomain !== 'app') {
    const url = req.nextUrl.clone();
    url.pathname = `/tenants/${subdomain}${url.pathname}`;
    return NextResponse.rewrite(url);
  }
}

// app/tenants/[tenant]/page.tsx handles the rewritten URL
// The user sees: acme.example.com/dashboard
// Next.js serves: example.com/tenants/acme/dashboard
```

Show: `NextResponse.rewrite()` (changes the URL internally without redirecting the browser), extracting the subdomain from the `host` header, `x-forwarded-host` handling in production (behind a proxy), and split-tenancy (tenant-specific layout at `app/tenants/[tenant]/layout.tsx`).''',

'''**Task (Code Generation):**
Build a Next.js 14 Route Handler with request body streaming and edge runtime:

```ts
// app/api/transform/route.ts:
export const runtime = 'edge';

export async function POST(req: Request) {
  if (!req.body) return Response.json({ error: 'No body' }, { status: 400 });

  const transform = new TransformStream({
    transform(chunk, controller) {
      const text = new TextDecoder().decode(chunk);
      const upper = text.toUpperCase();
      controller.enqueue(new TextEncoder().encode(upper));
    },
  });

  req.body.pipeThrough(transform);

  return new Response(transform.readable, {
    headers: { 'Content-Type': 'text/plain', 'Transfer-Encoding': 'chunked' },
  });
}
```

Show: `export const runtime = 'edge'` for Edge Runtime (Vercel Edge Functions), streaming request and response bodies, `TransformStream` for real-time data transformation, the Edge Runtime limitations (no Node.js built-ins), and when to use Edge vs Node.js runtime.''',

'''**Task (Code Generation):**
Implement a Next.js `generateMetadata` with OpenGraph images using the `ImageResponse` API:

```ts
// app/blog/[slug]/opengraph-image.tsx:
import { ImageResponse } from 'next/og';

export const runtime = 'edge';
export const size = { width: 1200, height: 630 };
export const contentType = 'image/png';

export default async function OGImage({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug);
  const font = await fetch(new URL('/fonts/Inter-Bold.ttf', baseURL)).then(r => r.arrayBuffer());

  return new ImageResponse(
    <div style={{ display: 'flex', width: '100%', height: '100%', background: '#1e1b4b', padding: 60 }}>
      <h1 style={{ color: '#fff', fontSize: 72, fontFamily: 'Inter' }}>{post.title}</h1>
    </div>,
    { ...size, fonts: [{ name: 'Inter', data: font, weight: 700 }] }
  );
}
```

Show: the file-based metadata convention (`opengraph-image.tsx` auto-generates the og:image meta tag), `ImageResponse` using Satori under the hood (renders JSX to SVG/PNG), custom font loading, and `generateMetadata` for dynamic meta tags.''',

'''**Task (Code Generation):**
Build a Next.js search page with URL state syncing using `useSearchParams` and `useRouter`:

```tsx
'use client';
import { useSearchParams, useRouter, usePathname } from 'next/navigation';

export function SearchFilters() {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const router = useRouter();

  const updateFilter = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams.toString());
    if (value) params.set(key, value);
    else params.delete(key);
    router.push(`${pathname}?${params.toString()}`, { scroll: false });
  };

  return (
    <>
      <input
        defaultValue={searchParams.get('q') ?? ''}
        onChange={e => updateFilter('q', e.target.value)}
        placeholder="Search..."
      />
      <select
        defaultValue={searchParams.get('sort') ?? 'newest'}
        onChange={e => updateFilter('sort', e.target.value)}
      >
        <option value="newest">Newest</option>
        <option value="price-asc">Price ↑</option>
      </select>
    </>
  );
}
```

Show: the `URLSearchParams` building, `router.push` vs `router.replace` for browser history (replace for filter changes — no back-button spam), debouncing the search input update, and the Server Component reading parameters via `searchParams` prop.''',

'''**Task (Code Generation):**
Implement a Next.js App Router global error boundary with Sentry integration:

```tsx
// app/global-error.tsx:
'use client';
import * as Sentry from '@sentry/nextjs';
import { useEffect } from 'react';

export default function GlobalError({ error, reset }: { error: Error; reset: () => void }) {
  useEffect(() => {
    Sentry.captureException(error, {
      tags: { source: 'global-error-boundary' },
      extra: { url: window.location.href },
    });
  }, [error]);

  return (
    <html><body>
      <h1>Something went wrong</h1>
      <button onClick={reset}>Try again</button>
    </body></html>
  );
}

// Sentry Next.js config (next.config.js):
const { withSentryConfig } = require('@sentry/nextjs');
module.exports = withSentryConfig(nextConfig, { silent: true, org: 'my-org', project: 'my-project' });
```

Show: `global-error.tsx` replacing the entire page (including layout) on error, `error.tsx` for route-specific errors (without replacing layout), Sentry's Next.js SDK — `instrumentation.ts` for Node.js + Edge initialization, and `sentry.client.config.ts`.''',

'''**Task (Code Generation):**
Build a Next.js i18n setup using the App Router with dictionary-based translations:

```
app/
  [locale]/
    layout.tsx
    page.tsx
    about/page.tsx
middleware.ts           ← Locale detection and redirect
dictionaries/
  en.json
  fr.json
  es.json
```

```ts
// middleware.ts — detect and redirect to locale:
import Negotiator from 'negotiator';
import { match } from '@formatjs/intl-localematcher';

export function middleware(req: NextRequest) {
  const locale = getLocale(req);
  if (!req.nextUrl.pathname.startsWith(`/${locale}`)) {
    return NextResponse.redirect(new URL(`/${locale}${req.nextUrl.pathname}`, req.url));
  }
}

// getDictionary.ts:
const dictionaries = { en: () => import('./dictionaries/en.json'), fr: () => import('./dictionaries/fr.json') };
export const getDictionary = async (locale: string) => (await dictionaries[locale]?.())?.default ?? {};
```

Show: the `[locale]` dynamic segment, `generateStaticParams` for known locales, `Intl.Collator` for locale-aware sorting, and `next-intl` library as a simpler alternative.''',

'''**Task (Code Generation):**
Implement a Next.js App Router protected layout with role-based access control:

```tsx
// app/(dashboard)/layout.tsx — Protected layout:
import { getSession } from '@/lib/session';
import { redirect } from 'next/navigation';

export default async function DashboardLayout({ children }: { children: React.ReactNode }) {
  const session = await getSession();

  if (!session?.userId) redirect('/login');

  const user = await db.user.findUnique({
    where: { id: session.userId },
    select: { id: true, name: true, role: true, permissions: true },
  });

  if (!user) redirect('/login');

  return (
    <RBACProvider user={user}>
      <DashboardShell user={user}>
        {children}
      </DashboardShell>
    </RBACProvider>
  );
}

// In any child route page:
// app/(dashboard)/admin/page.tsx:
export default async function AdminPage() {
  const user = await getCurrentUser();         // Uses cache() — no extra DB call
  if (user.role !== 'admin') notFound();
  return <AdminPanel />;
}
```

Show: the `(dashboard)` route group (no URL segment), `cache()` from React for de-duplicating DB calls across the same request, and `RBACProvider` passing permissions to client components.''',

'''**Task (Code Generation):**
Build a Next.js API rate limiter using Upstash Redis:

```ts
// lib/rate-limit.ts:
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'),  // 10 requests per 10 seconds
  analytics: true,
  prefix: 'api-rate-limit',
});

// app/api/protected/route.ts:
export async function GET(req: Request) {
  const ip = req.headers.get('x-forwarded-for') ?? '127.0.0.1';
  const { success, limit, remaining, reset } = await ratelimit.limit(ip);

  if (!success) {
    return Response.json(
      { error: 'Rate limit exceeded' },
      { status: 429, headers: { 'Retry-After': String(Math.ceil((reset - Date.now()) / 1000)) } }
    );
  }

  return Response.json({ data: 'OK', rateLimit: { limit, remaining } });
}
```

Show: Upstash Redis HTTP client (edge-compatible, no TCP), sliding window vs fixed window vs token bucket algorithms, the `Retry-After` header convention, and applying the rate limiter via middleware for global protection.''',

'''**Task (Code Generation):**
Implement a Next.js `prefetch` strategy for faster navigation using `router.prefetch`:

```tsx
'use client';
export function ProductGrid({ products }: { products: Product[] }) {
  const router = useRouter();

  return products.map(product => (
    <article
      key={product.id}
      onPointerEnter={() => router.prefetch(`/products/${product.slug}`)}
    >
      <Link
        href={`/products/${product.slug}`}
        prefetch={false}  // Disable auto-prefetch (too many in a large grid)
      >
        {product.name}
      </Link>
    </article>
  ));
}
```

Show: `router.prefetch('/path')` for imperative hover-intent prefetching, `<Link prefetch={false}>` to disable automatic prefetching for performance (many links), the App Router's automatic prefetch of linked layouts (but not leaf page data), and `<Link prefetch={true}>` to eagerly prefetch even when not in viewport.''',

'''**Task (Code Generation):**
Build a Next.js A/B testing setup using Edge Middleware with sticky assignment:

```ts
// middleware.ts:
export function middleware(req: NextRequest) {
  const variant = req.cookies.get('ab-checkout')?.value ??
    (Math.random() < 0.5 ? 'control' : 'treatment');

  const res = NextResponse.rewrite(
    new URL(`/experiments/checkout-${variant}${req.nextUrl.pathname}`, req.url)
  );

  // Sticky assignment — same variant for the session:
  if (!req.cookies.has('ab-checkout')) {
    res.cookies.set('ab-checkout', variant, { maxAge: 60 * 60 * 24 * 30 });
  }

  // Pass variant to pages via header:
  res.headers.set('x-ab-variant', variant);

  return res;
}
```

Show: the cookie-based sticky assignment, consistent user bucketing (hash user ID instead of random for logged-in users), `x-ab-variant` header forwarding to analytics, and reading the variant in the page component (`headers().get('x-ab-variant')`).''',

'''**Task (Code Generation):**
Implement Next.js Draft Mode for CMS preview with a secure token:

```ts
// app/api/draft/route.ts — Enable draft mode:
export async function GET(req: Request) {
  const url = new URL(req.url);
  const token = url.searchParams.get('token');
  const slug  = url.searchParams.get('slug');

  if (token !== process.env.DRAFT_SECRET) {
    return Response.json({ error: 'Invalid token' }, { status: 401 });
  }

  const { enableDraftMode } = await import('next/headers');
  enableDraftMode();

  return Response.redirect(new URL(`/blog/${slug}`, req.url));
}

// In page.tsx:
import { draftMode } from 'next/headers';

export default async function BlogPost({ params }) {
  const { isEnabled } = draftMode();
  const post = await cms.getPost(params.slug, { draft: isEnabled });
  return <Article post={post} isDraft={isEnabled} />;
}
```

Show: `draftMode()` from `next/headers`, the secure token validation, disabling draft mode via `/api/disable-draft`, and configuring the CMS webhook to call the preview URL.''',

'''**Task (Code Generation):**
Build a Next.js sitemap generator using the file-based `sitemap.ts` convention:

```ts
// app/sitemap.ts:
import { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const [posts, products, categories] = await Promise.all([
    db.post.findMany({ select: { slug: true, updatedAt: true }, where: { published: true } }),
    db.product.findMany({ select: { slug: true, updatedAt: true } }),
    db.category.findMany({ select: { slug: true } }),
  ]);

  return [
    { url: 'https://example.com', lastModified: new Date(), changeFrequency: 'daily', priority: 1 },
    ...posts.map(p => ({ url: `https://example.com/blog/${p.slug}`, lastModified: p.updatedAt, changeFrequency: 'weekly' as const, priority: 0.8 })),
    ...products.map(p => ({ url: `https://example.com/products/${p.slug}`, lastModified: p.updatedAt, changeFrequency: 'daily' as const, priority: 0.9 })),
  ];
}
```

Show: Next.js 13.3+ file-based sitemap, returning the `MetadataRoute.Sitemap` type, the `changeFrequency` and `priority` fields, segmenting large sitemaps (split into `sitemap/[id]/route.ts`), and `robots.ts` companion file.''',

'''**Task (Code Generation):**
Implement a Next.js data mutation pattern using the `useFormState` (React 19 `useActionState`) hook:

```tsx
'use client';
import { useActionState } from 'react'; // React 19; or useFormState from react-dom in 18
import { createPost, FormState } from './actions';

const initialState: FormState = { errors: {}, message: null };

export function CreatePostForm() {
  const [state, formAction, isPending] = useActionState(createPost, initialState);

  return (
    <form action={formAction}>
      <input name="title" aria-describedby="title-error" />
      {state.errors?.title && <span id="title-error">{state.errors.title[0]}</span>}

      <textarea name="content" />
      {state.errors?.content && <span>{state.errors.content[0]}</span>}

      <button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create Post'}
      </button>
      {state.message && <p role="alert">{state.message}</p>}
    </form>
  );
}
```

Show: the Server Action returning `FormState`, Zod validation inside the action, `isPending` from `useActionState` for loading UI, and progressive enhancement (form submits without JS via standard form POST).''',

'''**Debug Scenario:**
A Next.js App Router page throws "Dynamic server usage: `headers` was called" during `next build`:

```tsx
// app/user/page.tsx:
import { headers } from 'next/headers';

export default async function UserPage() {
  const userAgent = headers().get('user-agent'); // Error at build time!
  return <div>UA: {userAgent}</div>;
}
```

App Router tries to statically render all pages at build time unless told otherwise. `headers()` is dynamic — can't be known at build time. Show: adding `export const dynamic = 'force-dynamic'` to the page, or `export const revalidate = 0` (implies dynamic), and why `cookies()`, `headers()`, and `searchParams` all trigger dynamic rendering.''',

'''**Debug Scenario:**
A Next.js middleware `NextResponse.rewrite()` causes infinite redirect loops:

```ts
// middleware.ts:
export function middleware(req: NextRequest) {
  if (req.nextUrl.pathname === '/') {
    return NextResponse.rewrite(new URL('/home', req.url)); // Rewrites / to /home
  }
  if (req.nextUrl.pathname === '/home') {
    return NextResponse.rewrite(new URL('/', req.url)); // Rewrites /home back to /! Loop!
  }
}
```

The middleware matches `/home` and rewrites back to `/`, which matches again and rewrites to `/home` — infinite loop. Show: using a guard condition to detect rewritten requests (`req.headers.get('x-middleware-subrequest')`), checking `req.nextUrl.pathname` before rewriting, and using `NextResponse.next()` as the default case to avoid accidental catch-all behavior.''',

'''**Debug Scenario:**
A Next.js Server Component throws "Error: async/await is not yet supported in Client Components":

```tsx
// app/page.tsx (default — Server Component):
async function Page() {
  const data = await getData(); // ✓ Allowed in Server Components
  return <ClientComponent data={data} />;
}

// Somewhere in the component tree:
'use client';
async function AsyncClientComponent() {
  const data = await fetch('/api'); // Error! Client Components cannot be async
}
```

`async` Client Components are not supported — the `async` function can't be used as a React component with `'use client'`. Show: removing `async` and using `useEffect` + state for data fetching in Client Components, or moving the async work to a Server Component that passes data as props, or React Query's `useQuery` hook.''',

'''**Debug Scenario:**
A Next.js image with a remote src fails in production with "Invalid src prop — hostname not configured":

```tsx
<Image src="https://images.contentful.com/abc/photo.jpg" alt="..." width={800} height={600} />
// Error: hostname "images.contentful.com" is not configured under images in next.config.js
```

`next/image` requires all remote hostnames to be allowlisted for security. Show:

```js
// next.config.js:
images: {
  remotePatterns: [
    { protocol: 'https', hostname: 'images.contentful.com', port: '', pathname: '/**' },
  ],
}
```

The difference between `domains` (deprecated, less specific) vs `remotePatterns` (precise wildcard matching), and why this allowlist exists (prevents SSRF attacks via Next.js image optimization endpoint).''',

'''**Debug Scenario:**
A Next.js App Router Client Component using `useState` causes hydration mismatch because it reads `localStorage` during initial render:

```tsx
'use client';
function ThemeToggle() {
  const [theme, setTheme] = useState(localStorage.getItem('theme') ?? 'light');
  // Server: no localStorage → throws ReferenceError
  // OR: server renders 'light', client reads 'dark' from storage → mismatch
}
```

`localStorage` is unavailable in SSR, and even if guarded, the server value may differ from the client. Show: using `useState('light')` as default (always matches server), then updating from `localStorage` in a `useEffect` after hydration, `suppressHydrationWarning` on the element for intentional mismatches, and Next.js's `dynamic(() => import('./ThemeToggle'), { ssr: false })` to skip SSR entirely for this component.''',

'''**Debug Scenario:**
A Next.js 14 App Router `fetch()` inside a Server Component is not being cached despite using `force-cache`:

```tsx
async function ProductPage() {
  const product = await fetch(`/api/products/${id}`, {
    cache: 'force-cache',
  });
  // Product is fetched fresh every request — cache not working!
}
```

Relative URLs in `fetch()` inside Server Components cause issues — the request goes to `http://localhost:3000/api/products/id` in development, and the relative URL resolution may differ in production (especially on Vercel). Show: using an absolute URL (`${process.env.NEXT_PUBLIC_API_URL}/api/products/${id}`), or better — calling the database/service directly (no HTTP roundtrip needed inside RSC), and Next.js's `cache` function for de-duplicating work within a single request.''',

'''**Debug Scenario:**
A Next.js App Router `loading.tsx` file doesn't show while the page's data is loading:

```
app/
  products/
    loading.tsx  ← Exists but never shows!
    page.tsx
```

```tsx
// page.tsx — NOT using async/await:
'use client';
function ProductsPage() {
  const [products, setProducts] = useState([]);
  useEffect(() => { fetch('/api/products').then(r => r.json()).then(setProducts); }, []);
  // Page renders immediately (empty), then data loads client-side
  // loading.tsx only works for SERVER component route suspense, not client-side fetching!
}
```

`loading.tsx` wraps the page in a `<Suspense>` boundary — this only activates for async Server Components. Client-side `useEffect` data fetching bypasses it. Show: converting to an async Server Component + `Suspense` (activates `loading.tsx`), or showing a skeleton in the Client Component while the data loads (`if (products.length === 0) return <Skeleton />`).''',

'''**Debug Scenario:**
A Next.js Edge middleware reads from a Prisma database but throws build errors:

```ts
// middleware.ts:
import { db } from '@/lib/db'; // Imports Prisma client!

export const config = { matcher: ['/dashboard/:path*'] };

export async function middleware(req: NextRequest) {
  const session = await db.session.findUnique(...); // Error: Prisma not supported in Edge Runtime
}
```

Prisma uses Node.js APIs not available in the Edge Runtime (no `fs`, no TCP sockets for database connections). Show: using Prisma's Accelerate edge adapter, lightweight alternatives (Upstash Redis, `@vercel/kv`, or a JWT from a signed cookie), and keeping the middleware lightweight — defer database calls to API routes or Server Components.''',

'''**Debug Scenario:**
A developer's Next.js API route returns a 405 Method Not Allowed when testing with a REST client:

```ts
// app/api/users/route.ts:
export async function GET(req: Request) {
  return Response.json(await db.user.findMany());
}

// Testing: POST /api/users → 405 Method Not Allowed
```

The `app/api/users/route.ts` only exports `GET`. For `POST /api/users`, a `POST` export is needed. Show: adding `export async function POST(req: Request) { ... }`, the App Router Route Handler convention (named exports: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`), and the `OPTIONS` handler for CORS preflight.''',

'''**Debug Scenario:**
A Next.js page using `getStaticPaths` with `fallback: 'blocking'` shows the wrong content for low-traffic pages:

```ts
export async function getStaticPaths() {
  const topProducts = await db.product.findMany({ take: 100, orderBy: { views: 'desc' } });
  return { paths: topProducts.map(p => ({ params: { slug: p.slug } })), fallback: 'blocking' };
}
```

With `fallback: 'blocking'`, unbuilt pages are SSR'd on first request, then cached as static. This is correct. The actual bug: the first visitor to an unbuilt page triggers SSR, but if `getStaticProps` throws, the error page is statically cached and subsequent visitors see the error. Show: proper try/catch in `getStaticProps` with `notFound: true` for missing products, `revalidate` to eventually re-try failed pages, and `fallback: 'blocking'` vs App Router's `dynamicParams = true` equivalent.''',

'''**Task (Code Generation):**
Build a Next.js `instrumentation.ts` for OpenTelemetry tracing:

```ts
// instrumentation.ts (runs on server startup):
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    const { NodeSDK } = await import('@opentelemetry/sdk-node');
    const { getNodeAutoInstrumentations } = await import('@opentelemetry/auto-instrumentations-node');
    const { OTLPTraceExporter } = await import('@opentelemetry/exporter-trace-otlp-http');

    const sdk = new NodeSDK({
      traceExporter: new OTLPTraceExporter({ url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT }),
      instrumentations: [getNodeAutoInstrumentations({
        '@opentelemetry/instrumentation-http': { enabled: true },
        '@opentelemetry/instrumentation-fs': { enabled: false }, // Too noisy
      })],
    });

    sdk.start();
    process.on('SIGTERM', () => sdk.shutdown());
  }
}
```

Show: the `instrumentation.ts` convention (Next.js 13.4+), `NEXT_RUNTIME` guard for Edge vs Node.js, `@vercel/otel` as a simpler Vercel-native alternative, and the `next.config.js` `experimental.instrumentationHook: true` flag.''',

'''**Task (Code Generation):**
Implement a Next.js `cacheLife` and `cacheTag` pattern with the React `cache` function:

```ts
// lib/data.ts — Cached data fetchers with request deduplication:
import { cache } from 'react';
import { unstable_cache } from 'next/cache';

// Request-level dedup (per request, not persisted):
export const getCurrentUser = cache(async (userId: string) => {
  return db.user.findUnique({ where: { id: userId } });
});

// Full data cache (persisted across requests, ISR-like):
export const getProductsByCategory = unstable_cache(
  async (category: string) => db.product.findMany({ where: { category } }),
  ['products-by-category'],      // Cache key prefix
  { tags: ['products'], revalidate: 3600 }
);

// Multiple RSCs calling getCurrentUser(userId) in the same request →
// only ONE database query (React cache deduplicates).
```

Show: `cache()` for request-scoping (like React Query per-render dedup), `unstable_cache` for cross-request caching (like ISR for data), tag-based invalidation with `revalidateTag('products')`, and when to use each.''',

]
