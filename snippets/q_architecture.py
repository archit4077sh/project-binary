"""
snippets/q_architecture.py — 28 FRESH Architecture questions (mix of debugging + code generation)
Zero overlap with archived set.
"""

Q_ARCHITECTURE = [

"""**Task (Code Generation):**
Design and implement a plugin architecture for a dashboard builder where third-party developers can register new widget types:

```ts
WidgetRegistry.register('custom-chart', {
  component: CustomChartWidget,
  schema: z.object({ dataSource: z.string(), chartType: z.enum(['bar','pie']) }),
  defaultConfig: { chartType: 'bar' },
});
```

Show the `WidgetRegistry` implementation, how the dashboard renderer discovers registered widgets, how config validation works, and TypeScript types that ensure type safety between the schema and the component props.""",

"""**Debug Scenario:**
A Turborepo monorepo has four packages: `@app/web`, `@app/mobile`, `@app/api`, `@app/shared`. The build cache is consistently missed even for packages with no changes. Team has `TURBO_REMOTE_CACHE_TOKEN` set correctly.

Investigation shows the `@app/shared` package includes a `src/generated/` folder with files that change on every build (timestamp-based generated code). Diagnose why this causes cache misses for all dependent packages, and fix the Turborepo config to exclude the generated folder from the cache hash.""",

"""**Task (Code Generation):**
Implement a feature-flag-driven A/B testing system for a React app with server-side assignment:

```tsx
// Server component:
const variant = await getABVariant(userId, 'checkout-redesign');

// Client component:
<ABTest variant={variant} 
  A={<OriginalCheckout />} 
  B={<NewCheckout />} 
/>
```

Requirements:
- Variant assigned server-side (consistent per user, not per request)
- No layout shift from client-side variant switching
- Tracks impression and conversion events
- TypeScript types enforce that A and B receive the same props

Show the complete implementation.""",

"""**Debug Scenario:**
A design system's `Button` component has a `variant` prop with 5 values. After adding 2 new variants, consumer applications started showing TypeScript errors about the `variant` prop being incorrect — even though consumers haven't changed their code.

The design system publishes types with the package. Investigation shows the `variant` type in the published `.d.ts` file includes the old 5 variants but not the new 7. The `package.json` `types` field points to a stale build.

Design a CI-enforced process to: catch type drift between source and published types, auto-generate changelogs for breaking type changes, and version the type-only exports independently.""",

"""**Task (Code Generation):**
Build a micro-frontend shell application using Module Federation that:
- Loads a `ProductsApp` remote lazily when the user navigates to `/products`
- Shares React, React-DOM, and React-Query as singletons (one version across all MFEs)
- Falls back to an error boundary if the remote fails to load
- Shows a loading skeleton during remote chunk fetch

Show `webpack.config.js` for both shell and remote, the React lazy loading code, and the shared dependency configuration.""",

"""**Debug Scenario:**
A company's design system has grown to 180 components. Tree-shaking works, but importing any single component adds 45KB to the bundle because the DSN's `index.ts` barrel file causes Webpack to include the entire theme system.

```ts
// consumer code:
import { Button } from '@company/design-system'; // pulls in 45KB minimum
```

Design a solution that enables deep imports (`@company/design-system/button`) as a tree-shaking-friendly alternative, while preserving the barrel import for convenience. Show the `package.json` exports config and the build tooling to support both.""",

"""**Task (Code Generation):**
Design an error monitoring architecture for a Next.js 14 app with App Router that captures:
- Server Component render errors
- Client Component errors (ErrorBoundary)
- Server Action failures
- Unhandled promise rejections
- Web Vitals degradation events

Show the implementation for each capture point, how they all funnel to a single `ErrorService`, and how the `ErrorService` enriches errors with user context, session ID, and request ID before sending to Sentry.""",

"""**Debug Scenario:**
A team implements a "shared state" pattern using a global Zustand store accessed by both the Next.js App Router's Client Components and a WebSocket handler. After a server restart, the WebSocket handler has the old store state because the store was initialized before the restart's new module version loaded.

Explain why module-level singletons are problematic in hot-reloading environments (Next.js dev mode, Nodemon), and design a store initialization pattern that correctly handles hot module replacement without losing state.""",

"""**Task (Code Generation):**
Implement a `CommandPalette` component (like VS Code's Ctrl+K) with:
- Fuzzy search across registered commands
- Keyboard navigation (up/down arrows, enter to execute)
- Commands registered from any component via a `useRegisterCommand` hook
- Command grouping and priorities
- Recent commands history (localStorage)

Show the Context-based command registry, the fuzzy search implementation (no library), and the keyboard handler. Explain the architectural decision between context vs. singleton for the command registry.""",

"""**Debug Scenario:**
An app uses CSS Modules with Next.js. After adding a new page that imports a component from `@company/ui`, the server-side render throws:

```
SyntaxError: Cannot use import statement in a module
```

The `@company/ui` package ships ESM-only with CSS imports. Next.js's server-side rendering transpiles the app code but not `node_modules` by default.

Fix the issue by configuring `transpilePackages` in `next.config.js`. Explain why CSS Modules in `node_modules` packages require special handling and show the general rule for which packages need `transpilePackages`.""",

"""**Task (Code Generation):**
Design a multi-region data architecture for a Next.js app deployed on Vercel Edge:
- User writes go to a primary write region
- Reads served from the nearest read replica
- Conflict resolution for concurrent writes
- Optimistic updates on the client that reconcile with the eventual-consistent backend

Show the architecture diagram (as text/ASCII), the Vercel Edge Middleware for read routing, and the React Query setup for optimistic updates with background reconciliation.""",

"""**Debug Scenario:**
A monorepo uses pnpm workspaces. After updating `@company/utils` from `v1.2.0` to `v1.3.0`, the app silently continues using `v1.2.0` in production. The `package.json` shows `^1.2.0`.

Investigation reveals a phantom dependency: another package in the workspace also depends on `@company/utils@^1.2.0` and pnpm hoisted the older version. The app resolves to the hoisted version, not the workspace's updated one.

Explain pnpm's hoisting strategy, how to use `pnpm.overrides` to force a version, and how to detect phantom dependency version conflicts with `pnpm why`.""",

"""**Task (Code Generation):**
Build an internationalization (i18n) system for a Next.js 14 App Router app that:
- Supports en, fr, de locales detected from `Accept-Language` header in Middleware
- Stores translations in JSON files per locale and namespace
- Provides a typesafe `t` function where missing keys are TypeScript errors
- Supports plurals and interpolation
- Works in Server Components, Client Components, and Route Handlers

Show the Middleware locale detection, the `t` function implementation, and TypeScript inference for translation keys.""",

"""**Debug Scenario:**
A large React app has 40 lazy-loaded route chunks. After a new deployment, users on the old version get `ChunkLoadError: Loading chunk X failed` when navigating between routes because the old chunk hashes are gone.

Design a complete solution:
1. Detect `ChunkLoadError` in an Error Boundary
2. Automatically reload the page once (not infinite loop) to get the new version
3. Show the user a toast: "App updated — refreshing..."
4. Track how many users see this error to measure deployment smoothness""",

"""**Task (Code Generation):**
Implement a `DataFetcher` abstraction that works uniformly across Client Components, Server Components, and Server Actions — preventing duplicate fetch logic:

```ts
// Works in all contexts:
const { data: user } = await DataFetcher.get<User>('/users/:id', { id });
```

Show how to use `React.cache()` for Server Component deduplication, `react-query` for Client Component caching, and a shared `fetcher` function for Server Actions. The `DataFetcher` should detect its context and use the appropriate strategy.""",

"""**Debug Scenario:**
A team uses `react-query` with a global `queryClient` imported across the app. After adding server-side tests, tests occasionally fail with data from previous test cases because the `queryClient` retains cached data between tests.

Design a test setup that:
1. Creates a fresh `queryClient` per test
2. Wraps components with a test-local `QueryClientProvider`
3. Clears all caches after each test
4. Works with both RTL `render` and MSW server mocking

Show the test utilities, the custom `renderWithProviders` helper, and the Jest setup file.""",

"""**Task (Code Generation):**
Design and implement a client-side permissions system for a multi-tenant SaaS dashboard:

```ts
const { can, cannot } = usePermissions();
can('reports:read'); // boolean
can('users:write', { department: 'engineering' }); // context-aware
```

Requirements:
- Permissions defined server-side, passed to client via JWT claims or API
- Hierarchical permissions (admin > manager > viewer)
- Context-aware rules (can edit own reports, not others')
- `<PermissionGate action="reports:write">` component for conditional rendering
- TypeScript: action strings must be valid permission literals (no typos)""",

"""**Debug Scenario:**
A Next.js monorepo has three apps sharing a `@shared/auth` package. After upgrading Next.js from 13 to 14 in one app, the other two apps start failing to compile because `@shared/auth` imports from `'next/server'` — which now has a breaking change.

Explain the architectural problem with shared packages that import from host framework APIs (next/server, expo, react-native), and design a dependency injection or adapter pattern that decouples shared auth logic from the specific Next.js version.""",

"""**Task (Code Generation):**
Build a `useExperiment` hook for multivariate testing:

```ts
const { variant, trackConversion } = useExperiment('pricing-page', {
  variants: ['control', 'variant-a', 'variant-b'],
  weights: [0.5, 0.25, 0.25], // traffic distribution
});
```

Requirements:
- Variant assignment uses a deterministic hash of `userId + experimentId` (consistent per user)
- Assignment stored in localStorage for non-authenticated users
- Server-side assignment for authenticated users (avoids flash of wrong variant)
- `trackConversion` sends an analytics event with the variant context""",

"""**Debug Scenario:**
A dashboard uses WebSockets for real-time data. When deployed to multiple Kubernetes pods, WebSocket connections are load-balanced across pods without sticky sessions. A client connected to Pod A sends a message; Pod B handles the next request and doesn't have the WebSocket connection.

Design a Redis Pub/Sub-based solution for broadcasting WebSocket events across pods, show the server-side WebSocket subscription/publish code, and explain the tradeoffs of Redis Pub/Sub vs. a message queue (Kafka) for this use case.""",

"""**Task (Code Generation):**
Implement a `FormBuilder` that generates React forms from a JSON schema:

```ts
const config: FormSchema = {
  fields: [
    { name: 'email', type: 'email', label: 'Email', required: true },
    { name: 'role', type: 'select', options: ['admin', 'user'], default: 'user' },
    { name: 'notes', type: 'textarea', maxLength: 500 },
  ],
  onSubmit: async (data) => saveUser(data),
};

<FormBuilder schema={config} />
```

Show the `FormSchema` TypeScript type, the dynamic field renderer, validation integration (react-hook-form + zod), and how to add custom field renderers via a registry.""",

"""**Debug Scenario:**
A React Native app (Expo) and a Next.js web app share a `@shared/components` package. The package uses CSS Modules which work in Next.js but break in React Native (no CSS module support).

Design a platform-specific styling pattern using `Platform.select()` for React Native and CSS Modules for web, without duplicating component logic. Show how to configure the shared package's `package.json` with `react-native` export condition to automatically use the RN-compatible variant.""",

"""**Task (Code Generation):**
Build a content security policy (CSP) management system for Next.js 14:

```ts
// next.config.js
const csp = buildCSP({
  defaultSrc: ["'self'"],
  scriptSrc: ["'self'", "'nonce'", 'https://analytics.google.com'],
  imgSrc: ["'self'", 'data:', 'https:'],
  upgradeInsecureRequests: true,
});
```

Show:
1. The `buildCSP` function that generates the CSP header string
2. Nonce generation in middleware (new nonce per request)
3. Injecting the nonce into `<script>` tags via the `nonce` prop
4. Testing that CSP blocks XSS in a Playwright test""",

"""**Debug Scenario:**
A company measures that their React app has a "Time to Interactive" of 8.2 seconds on mobile. The app loads a 1.2MB initial JavaScript bundle. The top contributors from bundle analysis are: React + ReactDOM (140KB), a date picker library (280KB), a rich text editor (320KB, always loaded), and icon set (180KB, 500 icons but only 20 used).

For each bundle contributor, design the specific optimization: CDN UNPKG for React, dynamic import for date picker, lazy load with `next/dynamic` for editor, and a custom icon bundler that only includes used icons.""",

"""**Task (Code Generation):**
Implement a `GraphQLClient` with type-safe query execution:

```ts
const client = new GraphQLClient('https://api.example.com/graphql', { headers });

const { data } = await client.query(gql`
  query GetUser($id: ID!) {
    user(id: $id) { id name email }
  }
`, { variables: { id: '1' } });
// data.user.name is TypeScript string ✓
```

Show the client implementation using `graphql-tag`, response type inference from the query document, error handling for GraphQL errors vs network errors, and request batching support.""",

"""**Debug Scenario:**
A Next.js app's API routes are generating sequential numeric IDs visible in URLs (`/reports/156`). Security audits flag this as Insecure Direct Object Reference (IDOR) because users can enumerate other reports by incrementing the ID.

Design the fix:
1. Switch to UUID or NanoID for all new resources
2. Add authorization middleware that verifies the requesting user owns the resource
3. Add rate limiting to prevent brute-force enumeration
4. Database migration strategy for existing sequential IDs

Show the authorization middleware and the ID generation utility.""",

"""**Task (Code Generation):**
Design a zero-downtime database migration strategy for a Next.js app that renames `user.username` to `user.displayName` — a breaking schema change with active users 24/7.

Show the three-phase expand/migrate/contract pattern:
1. **Expand** — add `displayName` column, write to both columns, read from `username`
2. **Migrate** — backfill `displayName` for all existing rows in batches
3. **Contract** — read from `displayName`, stop writing `username`, drop column

Include the Prisma migration files for each phase, the feature-flag gating per phase, and how to monitor for errors during the live rollout.""",

"""**Debug Scenario:**
A React app deployed to multiple CDN edge nodes shows inconsistent behavior: some users see a stale version of a critical UI fix for hours after deployment while others see the fix immediately.

The CDN cache invalidation API was called post-deployment, but propagation takes 2–15 minutes per region. Stale HTML files (which reference the old JS bundle filenames) are served from cache.

Design a deployment strategy that guarantees users always receive new code: explain why `Cache-Control: no-cache` on HTML + `Cache-Control: max-age=31536000, immutable` on content-hashed assets is the industry standard solution. Show the Next.js `next.config.js` header configuration and the CDN rules for each path pattern.""",

]
