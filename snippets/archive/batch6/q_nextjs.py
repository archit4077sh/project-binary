"""
snippets/q_nextjs.py — BATCH 6: 56 brand-new Next.js questions
Zero overlap with batches 1-5 archives.
"""

Q_NEXTJS = [

"""**Task (Code Generation):**
Implement a Next.js App Router layout with per-page metadata and Open Graph images:

```ts
// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = await getPost(params.slug);
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [{ url: `/api/og?title=${encodeURIComponent(post.title)}`, width: 1200, height: 630 }],
    },
    twitter: { card: 'summary_large_image' },
    alternates: { canonical: `https://blog.example.com/${params.slug}` },
  };
}
```

Show: the `generateMetadata` async function pattern, the dynamic OG image API route using `ImageResponse` from `next/og`, font loading for the OG image, and `robots` metadata for disabling indexing on draft posts.""",

"""**Task (Code Generation):**
Build a Next.js rate limiter middleware using Redis Sliding Window:

```ts
// middleware.ts
export async function middleware(req: NextRequest) {
  const ip = req.ip ?? req.headers.get('x-forwarded-for') ?? 'unknown';
  const key = `rate:${ip}:${Math.floor(Date.now() / 60_000)}`; // per-minute window

  const count = await redis.incr(key);
  if (count === 1) await redis.expire(key, 60);

  if (count > 100) {
    return NextResponse.json({ error: 'Too many requests' }, {
      status: 429,
      headers: { 'Retry-After': '60', 'X-RateLimit-Limit': '100' },
    });
  }
  return NextResponse.next({ headers: { 'X-RateLimit-Remaining': String(100 - count) } });
}
```

Show: the Upstash Redis `@upstash/ratelimit` library as a simpler alternative, sliding window vs fixed window trade-offs, configuring `matcher` to apply only to API routes, and using `req.geo` for country-specific rate limits.""",

"""**Task (Code Generation):**
Implement a Next.js App Router error handling hierarchy with typed error pages:

```ts
// app/error.tsx — catches client-side + RSC errors
'use client';
export default function ErrorPage({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <div>
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}

// app/not-found.tsx — renders for 404s
// app/global-error.tsx — catches root layout errors
```

Show: the `error.tsx` client component requirement (must be `'use client'`), `error.digest` (server-side error identifier that doesn't leak details), `global-error.tsx` requiring its own `<html>` and `<body>`, and how `reset()` re-renders the segment trying the original render.""",

"""**Task (Code Generation):**
Build a Next.js App Router authentication flow using `next-auth` v5 (Auth.js):

```ts
// auth.ts
export const { auth, signIn, signOut, handlers } = NextAuth({
  providers: [
    GitHub({ clientId: process.env.AUTH_GITHUB_ID, clientSecret: process.env.AUTH_GITHUB_SECRET }),
    Credentials({
      authorize: async (credentials) => {
        const user = await db.users.findByEmail(credentials.email as string);
        if (!user || !await bcrypt.compare(credentials.password as string, user.passwordHash)) return null;
        return { id: user.id, email: user.email, name: user.name };
      },
    }),
  ],
  callbacks: {
    jwt({ token, user }) {
      if (user) token.role = user.role;
      return token;
    },
    session({ session, token }) {
      session.user.role = token.role as string;
      return session;
    },
  },
});
```

Show: the App Router route handler (`app/api/auth/[...nextauth]/route.ts`), middleware authentication check, protecting Server Components with `await auth()`, and the `session.user.role` TypeScript augmentation.""",

"""**Task (Code Generation):**
Implement a Next.js App Router with Stripe webhooks handling payment events:

```ts
// app/api/webhooks/stripe/route.ts
export async function POST(req: Request) {
  const body = await req.text(); // raw body for signature verification
  const signature = req.headers.get('stripe-signature')!;

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, signature, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch (err) {
    return Response.json({ error: 'Invalid signature' }, { status: 400 });
  }

  switch (event.type) {
    case 'payment_intent.succeeded':
      await handlePaymentSuccess(event.data.object as Stripe.PaymentIntent);
      break;
    case 'customer.subscription.deleted':
      await cancelSubscription((event.data.object as Stripe.Subscription).id);
      break;
  }

  return Response.json({ received: true });
}
```

Show: disabling Next.js body parsing (`export const config = { api: { bodyParser: false } }` in Pages Router) vs raw body in App Router, idempotency (use `event.id` to prevent double-processing), and storing the webhook event in DB before processing.""",

"""**Task (Code Generation):**
Build a Next.js App Router with typed Server Actions and optimistic UI:

```ts
// actions.ts
'use server';
export async function createPost(formData: FormData): Promise<ActionResult> {
  const title = formData.get('title') as string;
  const validated = PostSchema.safeParse({ title });
  if (!validated.success) return { error: validated.error.flatten().fieldErrors };
  const post = await db.posts.create({ data: { title, authorId: await getCurrentUserId() } });
  revalidatePath('/posts');
  return { success: true, post };
}

// In Client Component:
const [optimisticPosts, addOptimistic] = useOptimistic(posts, (state, newPost) => [...state, newPost]);
```

Show: `useOptimistic` rollback when the action fails, `useFormState` (React 19: `useActionState`) to read server action result, `revalidatePath` vs `revalidateTag` for cache invalidation, and Zod validation within a Server Action.""",

"""**Task (Code Generation):**
Implement a Next.js App Router multi-tenant application with subdomain routing:

```ts
// middleware.ts
export function middleware(req: NextRequest) {
  const hostname = req.headers.get('host')!;
  const subdomain = hostname.split('.')[0];

  // Map subdomain to tenant ID
  const tenantId = subdomain !== 'www' ? subdomain : null;

  if (tenantId) {
    const url = req.nextUrl.clone();
    url.pathname = `/tenant/${tenantId}${url.pathname}`;
    return NextResponse.rewrite(url);
  }
  return NextResponse.next();
}
```

Show: `app/tenant/[tenantId]/layout.tsx` for tenant-specific layout, fetching tenant branding in the layout, setting `x-tenant-id` request header for Server Components downstream, validating the tenant exists (redirect to 404 if not), and wildcard DNS configuration.""",

"""**Task (Code Generation):**
Build a Next.js App Router with a full-text search API using Algolia:

```ts
// app/api/search/route.ts
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const query = searchParams.get('q') ?? '';
  const page = Number(searchParams.get('page') ?? '0');

  const { hits, nbHits, nbPages } = await algolia.search<Product>(query, {
    indexName: 'products',
    hitsPerPage: 20,
    page,
    filters: searchParams.get('category') ? `category:${searchParams.get('category')}` : undefined,
    attributesToHighlight: ['name', 'description'],
    snippetEllipsisText: '…',
  });

  return Response.json({ hits, total: nbHits, pages: nbPages });
}
```

Show: the Algolia `v4` client initialization, Server Component usage of the InstantSearch result hook, reindexing products on DB change via a webhook, and the `<Highlight>` component for displaying search term highlights.""",

"""**Task (Code Generation):**
Implement a Next.js App Router page with server-side caching strategies:

```ts
// Cached for 10 minutes, tagged for on-demand revalidation:
const getProducts = unstable_cache(
  async () => db.products.findMany({ orderBy: { createdAt: 'desc' } }),
  ['products-list'],
  { revalidate: 600, tags: ['products'] }
);

// In Server Component:
const products = await getProducts();

// On product update (Server Action or API route):
revalidateTag('products'); // invalidates all caches tagged 'products'
```

Show: `unstable_cache` function signature, the difference between `revalidate` (time-based) and `tags` (on-demand), `fetch` with `next.revalidate` and `next.tags` options, and the caching layers (Router Cache → Full Route Cache → Data Cache).""",

"""**Task (Code Generation):**
Build a Next.js internationalised app with `next-intl` and locale-based routing:

```ts
// i18n.ts
export default getRequestConfig(async ({ locale }) => ({
  messages: (await import(`./messages/${locale}.json`)).default,
}));

// app/[locale]/layout.tsx
export async function generateStaticParams() {
  return ['en', 'de', 'fr', 'ja'].map(locale => ({ locale }));
}

// Usage: t('products.addToCart') → 'Add to Cart' (en) / 'In den Warenkorb' (de)
```

Show: the `next-intl` middleware for locale detection (Accept-Language header, cookie, URL prefix), `useTranslations` vs server-side `getTranslations()`, number and date formatting with ICU format strings, and pluralization (`{count, plural, one {# item} other {# items}}`).""",

"""**Task (Code Generation):**
Implement a Next.js App Router with a real-time notification system using Server-Sent Events:

```ts
// app/api/notifications/stream/route.ts
export async function GET(req: Request) {
  const stream = new ReadableStream({
    start(controller) {
      const send = (data: object) => {
        controller.enqueue(`data: ${JSON.stringify(data)}\n\n`);
      };

      const unsub = notificationService.subscribe(userId, send);
      req.signal.addEventListener('abort', () => {
        unsub();
        controller.close();
      });
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache, no-transform',
      'Connection': 'keep-alive',
    },
  });
}
```

Show: the client-side `EventSource` hook, reconnection logic with `EventSource`, SSE vs WebSocket trade-offs (SSE is unidirectional, HTTP/2 multiplexed), and handling backpressure in high-volume scenarios.""",

"""**Task (Code Generation):**
Build a Next.js App Router with database migrations managed by Drizzle ORM:

```ts
// drizzle/schema.ts
export const users = pgTable('users', {
  id:        uuid('id').primaryKey().defaultRandom(),
  email:     text('email').notNull().unique(),
  name:      text('name').notNull(),
  role:      text('role', { enum: ['admin', 'user'] }).notNull().default('user'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
});

// drizzle.config.ts
export default defineConfig({
  schema: './drizzle/schema.ts',
  out:    './drizzle/migrations',
  driver: 'pg',
  dbCredentials: { connectionString: process.env.DATABASE_URL! },
});
```

Show: running `drizzle-kit generate:pg` to create migration files, `drizzle-kit push` for development, running migrations at startup in production, typed query builder (`db.select().from(users).where(eq(users.role, 'admin'))`), and the `relations` API for joins.""",

"""**Task (Code Generation):**
Implement a Next.js App Router with file upload to S3 using presigned URLs:

```ts
// app/api/upload/presign/route.ts
export async function POST(req: Request) {
  const { filename, contentType, size } = await req.json();

  if (size > 10 * 1024 * 1024) return Response.json({ error: 'File too large' }, { status: 413 });
  if (!ALLOWED_TYPES.includes(contentType)) return Response.json({ error: 'Invalid type' }, { status: 400 });

  const key = `uploads/${randomUUID()}/${filename}`;
  const command = new PutObjectCommand({ Bucket: process.env.S3_BUCKET, Key: key, ContentType: contentType });
  const presignedUrl = await getSignedUrl(s3Client, command, { expiresIn: 300 });

  return Response.json({ presignedUrl, key, expiresIn: 300 });
}
```

Show: the client-side upload (PUT directly to S3 using the presigned URL), progress tracking with `XMLHttpRequest`, saving the S3 key in the database after successful upload, and post-upload image processing (trigger a Lambda or Server Action to resize the image).""",

"""**Task (Code Generation):**
Build a Next.js App Router with role-based access control (RBAC) middleware:

```ts
// middleware.ts
const ROUTE_PERMISSIONS: Record<string, Role[]> = {
  '/admin':    ['admin'],
  '/manager':  ['admin', 'manager'],
  '/api/admin': ['admin'],
};

export async function middleware(req: NextRequest) {
  const session = await auth();
  const pathname = req.nextUrl.pathname;

  const matchedRoute = Object.entries(ROUTE_PERMISSIONS)
    .find(([route]) => pathname.startsWith(route));

  if (matchedRoute && !matchedRoute[1].includes(session?.user?.role as Role)) {
    return NextResponse.redirect(new URL('/unauthorized', req.url));
  }
  return NextResponse.next();
}
```

Show: the `auth()` function from Auth.js in middleware, caching the session to avoid repeated JWT decoding, the glob pattern alternative for route matching, and a `hasPermission(session, action, resource)` utility for fine-grained permissions within Server Components.""",

"""**Task (Code Generation):**
Implement a Next.js App Router with background jobs using Queue (BullMQ + Redis):

```ts
// lib/queue.ts
export const emailQueue = new Queue('emails', { connection });

export const emailWorker = new Worker('emails', async (job) => {
  const { to, subject, html } = job.data;
  await resend.emails.send({ from: 'noreply@example.com', to, subject, html });
}, { connection, concurrency: 5 });

// In a Server Action:
await emailQueue.add('welcome', { to: user.email, subject: 'Welcome!', html: welcomeHtml }, {
  attempts: 3,
  backoff: { type: 'exponential', delay: 5_000 },
  removeOnComplete: { count: 1000 },
});
```

Show: the BullMQ `Queue` setup, `Worker` with concurrency, retry with exponential backoff, `removeOnFail: { count: 100 }` to keep failed job logs, a Bull Board dashboard route for monitoring (`app/admin/queues/route.ts`), and using `jobId` for deduplication.""",

# ── Debugging ─────────────────────────────────────────────────────────────────

"""**Debug Scenario:**
A Next.js App Router page throws "Error: Async Server Component used in Client Component" in production but not locally:

```tsx
// parent.tsx (Client Component! has 'use client'):
'use client';
import { DataDisplay } from './data-display'; // DataDisplay is an async Server Component

export function Parent() {
  return <DataDisplay />; // Error in production
}
```

Client Components cannot render async Server Components directly — they'd need to be hydrated on the client, but Server Components with async are server-only. Show: passing the Server Component's output as `children` prop to the Client Component (`<Parent><DataDisplay /></Parent>`), the "interleaving" pattern, and why this works (the Server Component renders to RSC payload before the Client Component hydrates).""",

"""**Debug Scenario:**
A Next.js App Router route that reads from a database returns stale data after an update:

```ts
// Server Component:
const posts = await db.posts.findMany(); // Returns stale data after create!

// Server Action that creates a post:
'use server';
async function createPost(data) {
  await db.posts.create({ data });
  // Forgot to revalidate!
}
```

Next.js App Router caches Server Component data. Without revalidation, updated data doesn't appear. Show: adding `revalidatePath('/posts')` after the create in the Server Action, using `revalidateTag('posts')` for finer control, `noStore()` to opt the component out of caching entirely for always-fresh data, and the caching layer difference between `fetch` caching and the Router Cache.""",

"""**Debug Scenario:**
A Next.js API route using the `edge` runtime throws "crypto is not defined":

```ts
export const runtime = 'edge';

import crypto from 'node:crypto'; // Works in Node.js runtime, not Edge!
export async function GET() {
  const hash = crypto.createHash('sha256').update('data').digest('hex');
}
```

The Edge Runtime doesn't support Node.js built-ins like `node:crypto`. Show: using the Web Crypto API instead (`crypto.subtle.digest('SHA-256', ...)` — globally available in Edge), the list of what's available in Edge Runtime (Fetch, TextEncoder, Streams, Web Crypto), switching to the Node.js runtime for routes that need Node APIs, and the performance trade-off (Edge: lower latency globally, Node: full API access).""",

"""**Debug Scenario:**
A Next.js `getServerSideProps` fetches user data but throws "Headers already sent" after a redirect:

```ts
export async function getServerSideProps({ req, res }) {
  const session = await getSession({ req });
  if (!session) {
    res.redirect(302, '/login'); // Direct res.redirect usage
    return { props: {} };       // BUG: still returns props AFTER redirect!
  }
  const user = await fetchUser(session.userId);
  return { props: { user } };
}
```

`res.redirect()` sends the redirect response immediately, but the code continues executing and returns `{ props: {} }`, attempting to write additional response data. Show: using the Next.js redirect pattern (`return { redirect: { destination: '/login', permanent: false } }`) instead of `res.redirect()`, which prevents double-write.""",

"""**Debug Scenario:**
A Next.js App Router Server Component reads `cookies()` but throws "cookies() should not be called outside a request scope":

```ts
// lib/auth.ts — module-level, runs at import time!
const session = cookies().get('session'); // Error!

export async function getUser() {
  return db.users.find(session?.value);
}
```

Dynamic functions like `cookies()`, `headers()`, and `searchParams` must be called inside a Server Component or Server Action — not at module level (which runs during build). Show: moving `cookies()` inside the `getUser()` function body, understanding that module-level code runs once at build time (for static pages), and the `unstable_noStore()` call that opts a component into dynamic rendering.""",

"""**Debug Scenario:**
A Next.js app deployed to Vercel has Client Components that reference `process.env.MY_SECRET` — the secret is exposed in the browser bundle:

```tsx
'use client';
// BUG: Client Components are bundled for the browser!
const apiKey = process.env.MY_API_KEY; // bundled into client JS!
```

Any `process.env` variable referenced in a Client Component is inlined into the browser bundle at build time. Show: moving sensitive API calls to Server Components, Server Actions, or API routes, only using `NEXT_PUBLIC_` prefixed variables in Client Components, and the `server-only` package that throws at build time if a server module is imported client-side.""",

"""**Debug Scenario:**
A Next.js App Router layout with a `Suspense` boundary around a slow Server Component causes the entire layout to delay before streaming:

```tsx
// app/layout.tsx
export default function Layout({ children }) {
  const slowData = await getSlowData(); // 2s — blocks entire layout stream!
  return <html><body><Header data={slowData} />{children}</body></html>;
}
```

`await` in the root layout blocks all streaming — no content is sent until `getSlowData` resolves. Show: moving the slow data fetch into a separate Server Component inside a `Suspense` boundary, ensuring the layout itself returns HTML immediately (without awaiting), and the `Promise` + read pattern for parallel data loading in Server Components.""",

"""**Debug Scenario:**
A Next.js App Router build fails with "Dynamic server usage: Page couldn't be rendered statically" for a page that dynamically reads `headers()`:

```ts
// app/analytics/page.tsx
export default async function Page() {
  const userAgent = (await headers()).get('user-agent'); // forces dynamic
  return <Analytics ua={userAgent} />;
}
```

Reading `headers()` makes the page dynamic (opts out of SSG). If the build attempts to statically generate the page, it fails. Show: adding `export const dynamic = 'force-dynamic'` to the page, or moving the User-Agent read to a Server Action / API route, using `Suspense` to defer the dynamic portion while the static shell renders, and the `generateStaticParams` interaction with dynamic pages.""",

"""**Debug Scenario:**
A Next.js App Router API route returns `response.json()` parsed output rather than the raw `Response.json()` output, causing a "body used already" error on retry:

```ts
export async function GET() {
  const data = await fetch('https://api.third-party.com/data');
  return Response.json(await data.json()); // Works once, but...
}
```

The `Response` body is a `ReadableStream` and can only be consumed once. If the route retries or the response is read twice (logging + return), it fails. Show: storing the parsed JSON (`const json = await data.json()`), returning `Response.json(json)`, and using `data.clone()` if the body must be read twice.""",

"""**Debug Scenario:**
A Next.js App Router page with `generateStaticParams` builds successfully but clicking a dynamic route in production returns a 404:

```ts
export async function generateStaticParams() {
  return [{ slug: 'hello-world' }, { slug: 'getting-started' }];
}

// User navigates to /blog/new-post (not in generateStaticParams) → 404
```

`generateStaticParams` only pre-generates listed slugs. Unknown slugs return 404 by default. Show: setting `export const dynamicParams = true` in the page to allow on-demand ISR for unknown slugs, using `revalidate` for ISR timing, and the different behaviors: `dynamicParams = true` (ISR fallback), `dynamicParams = false` (404 for unknown slugs).""",

"""**Debug Scenario:**
A developer wraps every `fetch()` call in Next.js API routes with `try/catch` but HTTP errors (404, 500 from external API) are not being caught:

```ts
try {
  const res = await fetch('https://api.example.com/data');
  const data = await res.json(); // Doesn't throw for 404!
  return Response.json(data);
} catch (err) {
  return Response.json({ error: 'Failed' }, { status: 500 });
}
```

`fetch()` only rejects `Promise` for network errors (no internet, DNS failure). HTTP error status codes (4xx, 5xx) resolve successfully. Show: checking `res.ok` or `res.status` after fetch: `if (!res.ok) throw new Error(`HTTP ${res.status}`)`, and a `fetchWithThrow` utility wrapper that throws for non-OK responses.""",

"""**Debug Scenario:**
A Next.js middleware modifies the response headers but the modifications don't appear in the browser:

```ts
export function middleware(req: NextRequest) {
  const response = NextResponse.next();
  response.headers.set('X-Custom-Header', 'my-value');
  return response;
}
```

`NextResponse.next()` creates a new response object. Headers set on it ARE forwarded to the origin response, but the origin response (from the page) may overwrite them. Show: using `NextResponse.next({ headers: { 'X-Custom-Header': 'my-value' } })` (sets request headers forwarded to the origin), using `response.headers.set` on the response from the origin, and the difference between request headers (forwarded to origin) and response headers (sent to browser).""",

"""**Debug Scenario:**
A Next.js App Router page using `React.cache` for request deduplication doesn't deduplicate calls across different Server Components:

```ts
// lib/data.ts
export const getUser = React.cache(async (id: string) => db.users.findUnique({ where: { id } }));

// layout.tsx → calls getUser('u1')
// page.tsx   → calls getUser('u1') again
// Both calls hit the DB!
```

`React.cache` deduplicates within the same request scope — but the layout and page may run in different React server rendering passes. Show: verifying `React.cache` works within the same Server Component tree branch (not across independent trees), using `unstable_cache` as an alternative that caches across requests (with tag-based invalidation), and logging the number of DB calls with Prisma query events.""",

"""**Debug Scenario:**
A Next.js app's static export (`next export`) fails because the app uses `getServerSideProps`:

```ts
export async function getServerSideProps(ctx) {
  const data = await fetchData();
  return { props: { data } };
}
// Error: "getServerSideProps" is not compatible with "next export"
```

`next export` generates a fully static HTML/CSS/JS app — it can't run server-side code. `getServerSideProps` requires a server at runtime. Show: replacing with `getStaticProps` for data available at build time, using `getStaticProps` + `revalidate` for ISR (not compatible with pure static export), client-side fetching with SWR as the export-compatible alternative, and the `output: 'export'` config in Next.js 13+.""",

"""**Debug Scenario:**
A developer uses `next/link` with `prefetch={false}` to prevent prefetching, but navigation to the route is still slow after the first visit:

```tsx
<Link href="/heavy-page" prefetch={false}>Heavy Page</Link>
```

Disabling `prefetch` prevents the page's JS from being pre-downloaded on hover/viewport entry. But slow navigation after the first visit suggests the data fetch on the page is slow, not the JS download. Show: distinguishing between navigation speed (JS chunk download) and data loading speed (Server Component fetch), using `loading.tsx` to show a skeleton immediately on navigation, and investigating the Server Component data fetch with server-side logs.""",

"""**Debug Scenario:**
A Next.js App Router Server Action mutates the database but the page doesn't reflect the change after redirect:

```ts
'use server';
async function createComment(formData: FormData) {
  await db.comments.create({ data: { content: formData.get('content'), postId } });
  redirect('/posts/' + postId); // Redirects, but page shows stale data!
}
```

`redirect()` navigates to the route, but the Router Cache holds the previous version of that page. Without revalidation, the cache is served. Show: calling `revalidatePath('/posts/' + postId)` BEFORE `redirect()`, using `revalidateTag('comments')` for tagged invalidation, and `redirect()` throwing a special `NEXT_REDIRECT` error (should not be inside `try/catch`).""",

"""**Debug Scenario:**
A Next.js `_app.tsx` wrapping components with a custom layout loses its layout on page transitions because `Component` changes:

```tsx
// pages/_app.tsx
export default function App({ Component, pageProps }) {
  return (
    <Layout>  {/* re-mounts on every page change! */}
      <Component {...pageProps} />
    </Layout>
  );
}
```

`<Layout>` itself doesn't re-mount (same JSX) but any state inside `<Layout>` (like scroll position or sidebar open state) resets because React reconciles by position — actually the Layout doesn't re-mount if it has a stable identity. The real bug: sidebar state in `Layout` uses `useState` keyed to `Component`. Show: lifting sidebar state above `_app.tsx` using Zustand / Jotai for persistent layout state, and the App Router `layout.tsx` which truly persists layout state across navigations.""",

"""**Debug Scenario:**
A Next.js app using `next/font` in a CSS Module has the font class correctly applied but the font still doesn't change:

```ts
// app/layout.tsx
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'] });

<html className={inter.className}>
```

The font loads, but another global CSS rule `* { font-family: Arial !important }` overrides it with `!important`. Show: removing the `!important` override, using CSS custom properties as the font variable (`inter.variable`), and the `variable` vs `className` usage (`className` directly applies, `variable` exposes a CSS custom property `--font-inter` for use in CSS files).""",

"""**Debug Scenario:**
A Next.js App Router component that reads `searchParams` on a Server Component is making the entire page dynamic and slower than expected:

```tsx
// app/products/page.tsx
export default function Page({ searchParams }: { searchParams: { sort?: string } }) {
  const sort = searchParams.sort ?? 'asc'; // reading searchParams = dynamic!
  // ...
}
```

Accessing `searchParams` in a Server Component opts the entire page out of static rendering (it becomes dynamic on every request). Show: using `Suspense` to isolate the dynamic portion, wrapping only the sort-dependent component in Suspense with its own `searchParams` read, `generateStaticParams` for static paths with a dynamic shell, and `use(searchParams)` in React 19 for deferred reads.""",

"""**Debug Scenario:**
A Next.js App Router app running on Vercel shows high costs because every user request is a new Serverless Function invocation even for cached pages:

```ts
export const revalidate = 3600; // should cache for 1 hour
export default async function ProductPage({ params }) {
  const product = await fetchProduct(params.id);
  return <Product {...product} />;
}
```

`revalidate` tells Next.js to ISR-cache the page, but cache headers from `fetchProduct` include `Cache-Control: no-store` (probably from a dev-mode fetch), preventing Vercel's CDN from caching. Show: checking `Response` headers from the upstream API, overriding with `fetch(url, { next: { revalidate: 3600 } })`, using `unstable_cache` to cache the data regardless of upstream headers, and Vercel's Fluid Compute vs Functions cost model.""",

"""**Debug Scenario:**
A Next.js Pages Router app with `getStaticPaths` returns `fallback: true` but navigating to a new path shows a full-page loader for 3 seconds before rendering:

```ts
export async function getStaticPaths() {
  return { paths: [], fallback: true }; // no paths pre-generated
}
```

With `fallback: true`, the first request to an ungenerated path shows the fallback UI (spinner) while the page generates. Show: using `fallback: 'blocking'` to server-side render new paths before sending HTML (no spinner, but 3s delay is still there), on-demand ISR with `res.revalidate()` to pre-generate popular paths when content is published, and the Pages Router vs App Router ISR behavior comparison.""",

"""**Debug Scenario:**
A Next.js API route that calls an external GraphQL API always returns a fresh response instead of using the cached data, even though `revalidate` is set:

```ts
// app/api/data/route.ts
export const revalidate = 300;

export async function GET() {
  const response = await fetch('https://graphql.example.com/api', {
    method: 'POST',
    body: JSON.stringify({ query: '{ products { id name } }' }),
  });
  return Response.json(await response.json());
}
```

Next.js only caches `GET` fetch requests. The GraphQL request is a `POST` — which Next.js never caches. Show: caching the GraphQL response using `unstable_cache` wrapped around the fetch call, or memoizing with `React.cache` for per-request deduplication, and the `init.cache` option on `fetch` (`{ cache: 'force-cache', next: { revalidate: 300 } }`) for cacheable GET requests.""",

"""**Debug Scenario:**
A Next.js App Router Client Component using `useRouter().push()` doesn't preserve scroll position when navigating back:

```tsx
'use client';
function ProductCard({ product }) {
  const router = useRouter();
  return <div onClick={() => router.push(`/products/${product.id}`)}>...</div>;
}
```

`router.push()` does NOT save/restore scroll position by default in App Router when navigating programmatically. Show: the `scroll: false` option in `router.push('/path', { scroll: false })`, implementing manual scroll restoration with `sessionStorage` (save `scrollY` before navigate, restore in `useLayoutEffect` on destination), and `<Link>` vs `router.push()` scroll behavior differences.""",

"""**Debug Scenario:**
A Next.js app is showing a CORS error when calling its own API routes from the browser, despite being on the same domain:

```
Access to fetch at 'https://app.example.com/api/data' 
from origin 'https://app.example.com' has been blocked by CORS policy.
```

The app is actually not calling its own domain — the Vercel deployment is on `app.example.com` but the request goes to a slightly different URL (the preview URL `app-xyz.vercel.app`). The browser sees a cross-origin request. Show: always calling API routes as relative URLs (`/api/data` instead of `https://app.example.com/api/data`) in Client Components, the `next.config.js` CORS headers configuration for explicitly allowed origins, and `NextResponse` with `Access-Control-Allow-Origin` headers for external client access.""",

"""**Debug Scenario:**
A Next.js `middleware.ts` that sets cookies causes a loop — the middleware keeps redirecting because the cookie it just set isn't seen on the next check:

```ts
export function middleware(req: NextRequest) {
  const hasCookie = req.cookies.get('initialized');
  if (!hasCookie) {
    const res = NextResponse.redirect(new URL('/welcome', req.url));
    res.cookies.set('initialized', 'true');
    return res; // Redirects to /welcome, then middleware runs AGAIN without the cookie!
  }
}
```

The `Set-Cookie` header is in the response, but the browser hasn't received it yet — the redirect sends the response and the next request from the browser starts fresh. But `/welcome` also hits the middleware — the cookie IS sent in the redirect response, so the browser SHOULD have it on the next request. The real bug: `matcher` doesn't exclude `/welcome`, causing infinite redirect. Show: adding `/welcome` to the matcher exclusion list, and using `NextResponse.next({ headers: { 'Set-Cookie': ... } })` to set cookies without redirecting.""",

"""**Debug Scenario:**
A Next.js App Router app has a `loading.tsx` file but the loading skeleton sometimes flickers and shows even for cached navigations that complete nearly instantly:

```tsx
// app/products/loading.tsx
export default function Loading() {
  return <ProductSkeleton />;  // flickers on fast cached navigations
}
```

`loading.tsx` shows the skeleton on the INSTANT the navigation starts (before the destination page is ready). For cached pages that resolve in 50ms, the skeleton flickers briefly. Show: using `startTransition` to defer navigating (React waits up to the `transition` timeout before showing the fallback), the `useDeferredValue` pattern for hiding loading states under a threshold, and the recommendation to use skeleton screens that match the destination layout to reduce perceived flicker.""",

]
