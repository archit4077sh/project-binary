"""
snippets/nextjs.py — Next.js 14 code snippets for question injection.
"""

NEXTJS_SNIPPETS = [
    # 1. Server Component with async fetch
    """\
// app/dashboard/page.tsx  (Server Component)
export default async function DashboardPage() {
  const data = await fetch('https://api.internal/metrics', {
    next: { revalidate: 60 },
  }).then(r => r.json());

  return <MetricsGrid data={data} />;
}""",

    # 2. Route handler with caching
    """\
// app/api/rows/route.ts
export const revalidate = 30; // segment-level cache

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const page = Number(searchParams.get('page') ?? 1);
  const rows = await db.query.rows.findMany({ limit: 50, offset: (page - 1) * 50 });
  return Response.json(rows);
}""",

    # 3. Middleware with permission check
    """\
// middleware.ts
export function middleware(request: NextRequest) {
  const token = request.cookies.get('session')?.value;
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  const decoded = verifyJWT(token!);
  if (!decoded.permissions.includes('dashboard:read')) {
    return NextResponse.redirect(new URL('/403', request.url));
  }
  return NextResponse.next();
}

export const config = { matcher: ['/dashboard/:path*'] };""",

    # 4. Client component with use client boundary
    """\
// components/FilterBar.tsx
'use client';

import { useState, useTransition } from 'react';
import { useRouter } from 'next/navigation';

export function FilterBar({ initialFilter }: { initialFilter: string }) {
  const [filter, setFilter] = useState(initialFilter);
  const [isPending, startTransition] = useTransition();
  const router = useRouter();

  const apply = () => startTransition(() => {
    router.push(`/dashboard?filter=${filter}`);
  });

  return (
    <input value={filter} onChange={e => setFilter(e.target.value)} onBlur={apply} />
  );
}""",

    # 5. Streaming with Suspense
    """\
// app/dashboard/page.tsx
import { Suspense } from 'react';

export default function Page() {
  return (
    <main>
      <h1>Dashboard</h1>
      <Suspense fallback={<KPISkeleton />}>
        <KPISection /> {/* slow async server component */}
      </Suspense>
      <FilterBar initialFilter="" />
      <Suspense fallback={<TableSkeleton />}>
        <DataTableSection /> {/* also slow */}
      </Suspense>
    </main>
  );
}""",

    # 6. generateStaticParams with dynamic route
    """\
// app/report/[id]/page.tsx
export async function generateStaticParams() {
  const ids = await db.query.reports.findMany({ columns: { id: true } });
  return ids.map(({ id }) => ({ id: String(id) }));
}

export default async function ReportPage({ params }: { params: { id: string } }) {
  const report = await getReport(params.id);
  if (!report) notFound();
  return <ReportView report={report} />;
}""",

    # 7. Edge runtime function
    """\
// app/api/auth/route.ts
export const runtime = 'edge';

export async function POST(req: Request) {
  const { token } = await req.json();
  // edge runtime — no Node.js crypto, no fs, no process.env access in some hosts
  const payload = await verifyWithWebCrypto(token);
  return Response.json({ userId: payload.sub });
}""",
]
