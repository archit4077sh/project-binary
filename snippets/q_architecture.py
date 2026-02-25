"""
snippets/q_architecture.py - 28 Frontend Architecture questions
"""

Q_ARCHITECTURE = [

"""**Context:**
Our Next.js dashboard is a monorepo with packages: @company/ui (design system), @company/api-client (fetch wrappers), @company/utils. The UI package imports from api-client for a few convenience hooks.

**Observed Issue:**
api-client now wants to import a shared type from ui. This creates a circular dependency: ui → api-client → ui. The build doesn't break (Webpack handles it) but TypeScript type-checking occasionally produces stale types.

**Specific Ask:**
How do you resolve circular dependencies in a monorepo without restructuring everything? Is the correct fix to extract the shared types into a @company/types package that neither ui nor api-client depends on circularly? What tooling (dependency-cruiser, Nx enforce-module-boundaries) catches circular deps in CI before they become stale-type problems?""",

"""**Context:**
We're using Module Federation to split our dashboard into a host and two remotes (AnalyticsMFE, ReportsMFE). We share React and Zustand between host and remotes as singleton: true.

**Observed Issue:**
After a deploy where the host updates to React 18.3.1 but ReportsMFE is still on 18.2.0, two React instances are loaded. State updates in ReportsMFE no longer propagate to the host's context, and hooks start violating rules-of-hooks because of the dual React instance.

**Specific Ask:**
How do you enforce that Module Federation shared singletons always resolve to the same version across host and all remotes, especially when remotes are deployed independently? Is semantic versioning range in shared config the right tool (requiredVersion: "^18"), and what happens when a remote's range is incompatible with the host?""",

"""**Context:**
We maintain a design system component library used by 6 internal dashboard apps. We need to make a breaking change: rename the variant prop on Button from type to variant to align with industry conventions.

**Observed Issue:**
6 apps have 200+ usages of <Button type="primary">. We can't coordinate a big-bang migration. We need backward compatibility for at least 2 quarters.

**Specific Ask:**
What's the API design strategy for a breaking prop rename in a shared component library? Is a deprecation shim (accept both type and variant, warn on type) the right approach? How do you communicate deprecations effectively across teams -- TypeScript @deprecated JSDoc, eslint rules, or Storybook deprecation badges?""",

"""**Context:**
We're implementing feature flags for a new AI-powered summarization feature. The feature should be enabled only for enterprise users in specific regions, with a 10% gradual rollout, and the ability to kill-switch instantly.

**Observed Issue:**
Our current feature flag approach is a simple boolean per flag checked client-side after auth. It doesn't support percentage rollouts, user segment targeting, or kill-switches without a deploy.

**Specific Ask:**
How do you architect a feature flag system that supports: (1) user segment targeting, (2) percentage rollouts seeded by user ID, (3) instant kill-switch without deploy, and (4) zero added UI latency? Should flag evaluation happen in Next.js Middleware (edge), an RSC, or client-side? What's the tradeoff of each?""",

"""**Context:**
Our dashboard has ~40 route segments, each importing their own data fetching logic, components, and local state. We want to implement route-level code splitting so /reports only loads what /reports needs.

**Observed Issue:**
We use Next.js App Router, so route-level splitting is automatic. But our shared component library (@company/ui) is a single 280KB chunk imported on every route, even for routes that only use 3 components from it.

**Specific Ask:**
How do you tree-shake a component library in a Next.js App Router environment where RSC and Client Components coexist? Is barrel file elimination (no index.ts re-exports) the primary fix? And if the library must have a barrel for DX, is there a Webpack plugin that handles barrel file tree-shaking transparently?""",

"""**Context:**
We need to design a polymorphic notification card component that renders differently for 8 notification types (NewComment, Mention, StatusChange, etc.), each with different actions and layouts.

**Observed Issue:**
Currently we have one NotificationCard component with 8 if-else branches and 25 conditional props. It's 400 lines, untestable in isolation, and every new type touches the same file.

**Specific Ask:**
What's the component API design pattern for a family of related but heterogeneous UI elements? Is the compound component pattern (NotificationCard.Comment, NotificationCard.Mention) appropriate here, or a discriminated union of fully separate components? How do you balance co-location (all card logic together) with extensibility (adding type 9 later)?""",

"""**Context:**
We have a data grid component where the parent needs to control column visibility, row selection, sorting, filters, and pagination. Currently everything is passed as props, but the prop surface is 25+ props.

**Observed Issue:**
The DataGrid component re-renders on every Dashboard render because 25 props always include object literals. Memoization is nearly impossible when the prop surface is this large.

**Specific Ask:**
What patterns reduce prop surface on a complex component while maintaining parent control? Is a headless component (useDataGrid hook returns state + handlers, parent renders as it likes) better than a compound component with render slots? When do you use Context to thread state through a compound hierarchy instead of prop drilling?""",

"""**Context:**
We have several components originally built as render props. We're migrating them to hooks per the modern React idiom, but some consumers rely on the render prop's access to the component's internal DOM ref.

**Observed Issue:**
The hook version returns a ref that consumers assign to their own elements. But some consumers are function components that can't receive a ref directly on their custom wrapper -- they'd need forwardRef.

**Specific Ask:**
Is there a clean migration path from render props (which had direct DOM access via the component) to hooks (where the consumer must manage the ref themselves)? Should we emit both a hook and a render-prop component during the transition period? What's the timeline for removing render props from a component library used by 6 teams?""",

"""**Context:**
Our Next.js dashboard has a deeply nested component tree: App → DashboardLayout → PageLayout → Section → Widget → Chart. The Chart component needs access to the user's time zone preference set at the App level.

**Observed Issue:**
We're passing timezone as a prop through 5 layers of components that don't use it themselves. Adding any new cross-cutting concern requires touching every intermediate layer.

**Specific Ask:**
At what depth does prop drilling become unacceptable and Context the right solution? What's the performance cost of adding a new Context for every cross-cutting concern (timezone, theme, locale, permissions)? Is there a pattern to combine many cross-cutting values into fewer contexts without causing over-rendering?""",

"""**Context:**
Our dashboard has two data fetching patterns in use simultaneously: RSC server-side fetches (for initial data) and React Query client-side fetches (for real-time updates). Data sometimes gets out of sync between the two layers.

**Observed Issue:**
After a Server Action mutates data, the RSC re-renders with fresh data but the React Query cache still has the old value. Components reading from React Query show stale data alongside fresh RSC data.

**Specific Ask:**
What's the architectural pattern for coordinating between RSC-fetched server state and React Query client-side cache? Should we hydrate React Query from RSC data at the page boundary (dehydrate/hydrate pattern), or is the correct approach to use React Query for everything and not rely on RSC for data that also needs client-side updates?""",

"""**Context:**
Our dashboard has no consistent error handling strategy. Some components throw and are caught by the nearest Error Boundary. Others display inline error states. API errors sometimes surface as toast notifications and sometimes as blank panels.

**Observed Issue:**
Users experience inconsistent UX: some errors are recoverable (retry button), some are fatal (full page error), and some are silent (component renders empty). No pattern for which errors should be which.

**Specific Ask:**
How do you design a global error handling architecture for a large dashboard? What's the decision tree for: (1) Error Boundary + fallback UI, (2) inline error state within the component, (3) toast notification, (4) global error page? Should network errors always be toasts? How do you ensure Server Action errors and RSC fetch errors follow the same UX pattern?""",

"""**Context:**
We're adding structured frontend logging to send error context to our observability platform (DataDog). We need to capture component tree context, user ID, session ID, and the specific action the user was performing when an error occurred.

**Observed Issue:**
Currently we log raw Error objects with window.onerror. We have no context about which dashboard panel errored, what the user was doing, or what data was loaded at the time.

**Specific Ask:**
What's the architecture for structured frontend error logging that captures rich context? Should a logging Context provider intercept ErrorBoundary callbacks and enrich them with user/session info? How do you capture the "last user action" breadcrumb without adding logging code to every click handler?""",

"""**Context:**
We're running an A/B test: Treatment A shows the new AI Summary panel by default, Treatment B shows the classic detail view. We need test assignment to be stable (same user always gets the same variant), work for logged-in and anonymous users, and not add UI latency.

**Observed Issue:**
Our current A/B test assigns variants client-side in a useEffect, causing a layout shift when the variant renders differently from the SSR default. Users see the default for 200ms then the variant pops in.

**Specific Ask:**
How do you architect zero-flicker A/B testing in a Next.js 14 SSR app? Should variant assignment happen in Middleware (edge, seeded by user ID), in an RSC, or in a cookie set on the first visit? What's the tradeoff between edge-assignment (fast, no personalization data) and server-assignment (slow, full user data)?""",

"""**Context:**
Our dashboard implements RBAC. The API enforces permissions server-side, but we also need to conditionally render UI elements based on permissions (hide the Delete button for read-only users).

**Observed Issue:**
Permission checks are scattered: some in RSC (server-side, authoritative), some in context hooks (client-side, potentially stale), and some duplicated in both. After a permission change (user upgraded to editor), the UI doesn't reflect the new permissions without a full page reload.

**Specific Ask:**
What's the correct layer for RBAC UI enforcement in a Next.js 14 RSC + Client Component app? Should client-side permission checks be treated as pure UX hints (not security) while RSC provides the authoritative check? How do you invalidate permission caches across the full stack when a user's role changes mid-session?""",

"""**Context:**
Our design system needs to support three themes: light, dark, and "high contrast." Themes are defined as design tokens (CSS custom properties) and must be switchable at runtime without a page reload.

**Observed Issue:**
Our current implementation puts theme tokens in separate CSS files (light.css, dark.css) and switches by toggling a class on <html>. But users on slow connections get a flash of the wrong theme on initial load if the class is applied by JavaScript after hydration.

**Specific Ask:**
What's the correct implementation for a runtime-switchable theme system that avoids FOIC (Flash Of Incorrect Colors) on initial load? Is the solution an inline <script> to read localStorage before React hydrates? How does next/themes solve this, and what are its limitations in the App Router RSC context?""",

"""**Context:**
Our dashboard serves users in 15 locales. We use a runtime i18n library (react-i18next) that loads translation JSON files on demand per locale.

**Observed Issue:**
The translation JSON files are loaded client-side after React hydrates, causing a second render when translations populate. This adds to CLS and creates a brief flash of translation keys.

**Specific Ask:**
What's the architecture for server-side i18n in a Next.js 14 App Router + RSC codebase? Should RSC render translated text directly (server-side translation lookup) while Client Components load translations as needed? How do you handle dynamic content (user-generated) that also needs localization?""",

"""**Context:**
We're adding product analytics tracking to every user interaction in the dashboard. The events need to include page context, user ID, session ID, feature flags active, and component-specific metadata.

**Observed Issue:**
We've added onClick/onFocus/onBlur handlers to ~200 components individually. The tracking code is duplicated, inconsistent, and tightly coupled to component implementation details.

**Specific Ask:**
What's the architectural pattern for non-intrusive analytics tracking in a React component tree? Is an event delegation pattern at the root (single listener that reads data-track attributes) better than individual handlers? How do you capture component-specific metadata (e.g., which chart was clicked) without coupling the analytics to component implementation?""",

"""**Context:**
We're evaluating form libraries for our dashboard, which has 15 complex forms (report builder, filter configurator, user settings). We have React Hook Form (RHF) today but are having issues with deeply nested field arrays.

**Observed Issue:**
FieldArray performance in RHF degrades with 100+ rows. Each row has 5 fields, and adding/removing rows triggers re-renders of all sibling rows. We're considering Formik or a lighter custom solution.

**Specific Ask:**
Is React Hook Form's performance problem with large FieldArrays a fundamental limitation or a usage pattern issue? Does the uncontrolled input approach (register()) actually help at 100+ row FieldArrays? How does Tanstack Form compare to RHF for this use case, and what's the migration cost?""",

"""**Context:**
Our dashboard displays relative and absolute dates across many components. We've had bugs where dates are displayed in the wrong timezone -- the server's timezone instead of the user's.

**Observed Issue:**
new Date() on the server returns UTC. When this date is serialized and rendered on the client, components format it using the server's locale instead of the user's browser locale.

**Specific Ask:**
What's the architectural approach to timezone-correct date rendering in an RSC + client component app? Should all date formatting happen client-side (to use the browser's locale), and if so, how do you avoid hydration mismatches between server-rendered dates and client-formatted ones? Does Intl.DateTimeFormat have the right APIs for user-timezone formatting?""",

"""**Context:**
Our dashboard allows users to upload large files (PDF reports, CSV imports up to 200MB). We currently upload via a multipart POST to our Next.js API route, which proxies to S3.

**Observed Issue:**
The Next.js server acts as an unnecessary middleman for binary data. 200MB files double-traverse the network (client → Next.js → S3) and frequently timeout on the App Router's default body size limits.

**Specific Ask:**
What's the correct architecture for large file uploads in a Next.js 14 app? Is a direct S3 presigned URL approach (client gets presigned URL from a lightweight API route, uploads directly to S3) the right design? How do you handle upload progress, resumable uploads, and virus scanning in this model?""",

"""**Context:**
Our dashboard displays live trade data. We're using WebSockets for real-time updates, but on slow connections, the client falls behind the server and receives updates out of order or with gaps.

**Observed Issue:**
When the WebSocket reconnects after a drop, we replay the buffer from the last-seen event ID. But the buffer has a 5-minute retention window -- gaps longer than 5 minutes result in incorrect data.

**Specific Ask:**
How do you design a client-side real-time update system that degrades gracefully for gaps longer than the buffer window? Should the client fall back to a full state snapshot fetch (REST endpoint) after a large gap, treating the WebSocket as an incremental update layer on top of a base snapshot? How do you design the shared WebSocket + REST API contract for this?""",

"""**Context:**
Our dashboard needs to work offline for field users who lose connectivity. We need: (1) read-only access to the last cached data, (2) queued writes that sync when connectivity returns, and (3) a clear indicator of connectivity status.

**Observed Issue:**
We have no Service Worker or offline strategy. When connectivity drops, the entire dashboard shows API errors.

**Specific Ask:**
What's the architecture for an offline-first read layer in a Next.js + RSC dashboard? Is a Service Worker with cache-first strategy for GET requests sufficient for (1)? For queued writes (2), should we use Background Sync API or IndexedDB with a manual sync-on-reconnect trigger? How does the RSC model interact with Service Worker caching?""",

"""**Context:**
Our design system doesn't have formal accessibility (a11y) contracts for its components. A recent audit found 23 WCAG AA violations -- mostly missing ARIA roles, incorrect focus management, and insufficient color contrast.

**Observed Issue:**
Fixes are applied per-component reactively after audits. There's no systemic guarantee that new components meet a11y requirements before they ship.

**Specific Ask:**
How do you build accessibility requirements into the component development lifecycle rather than treating them as post-hoc fixes? Can automated tools (axe-core in Storybook, jest-axe in unit tests) catch the majority of violations, or do WCAG AA requirements need manual testing? What's the component API design pattern that makes correct ARIA usage the path of least resistance for consumers?""",

"""**Context:**
Our design system has 80 components documented in Storybook. But adoption is inconsistent -- product engineers still create ad-hoc components because they don't know what the system offers, can't find examples quickly, or find the Storybook docs too minimal.

**Observed Issue:**
We have a design system library that's under-utilized. The result is 15 ad-hoc Button variants scattered across the codebase.

**Specific Ask:**
How do you drive component library adoption beyond just building good components? Is an ESLint rule that warns "prefer @company/ui Button over native <button>" a good enforcement mechanism? What information does a story need to contain for engineers to trust it -- do-and-don't examples, copy-paste code, design token context, or something else?""",

"""**Context:**
We're preparing our @company/ui design system for public npm publish. Currently it bundles its own dependencies (React, styled-components) which conflict with consumers' versions.

**Observed Issue:**
Previous beta versions bundled React, causing "two React instances" errors in consuming apps. We need to declare peer dependencies correctly and generate both ESM and CJS builds.

**Specific Ask:**
What's the correct package.json setup for a React component library published to npm that needs to support both ESM (for bundlers that tree-shake) and CJS (for Node.js testing environments)? How do you configure the exports map, sideEffects, and types fields? And what build tool (tsup, Rollup, Vite lib mode) gives the cleanest dual-format output with minimal config?""",

"""**Context:**
We maintain 3 dashboard products sharing the monorepo. Each has different versioning cadences. Currently, all packages in the monorepo use a single unified version number managed by Lerna.

**Observed Issue:**
A bug fix in @company/api-client (used by all 3 products) forces a version bump that triggers a re-publish of all other packages, even ones unchanged. Dependabot updates become massive PRs.

**Specific Ask:**
What's the tradeoff between a fixed/unified versioning strategy (Lerna fixed mode) vs. independent versioning (Lerna independent) for a monorepo with shared packages and multiple product consumers? How does Changesets differ from Lerna for managing this, and does it handle independent versioning better?""",

"""**Context:**
Our monorepo uses Nx for task orchestration. Build times for CI have grown to 22 minutes because every PR rebuilds all 9 packages even when only one changed.

**Observed Issue:**
Nx's affected detection is configured but not working correctly for our setup. Changes to a shared @company/types package trigger rebuilds of all consumers, which is correct, but changes to @company/ui docs don't affect downstream packages and should be skipped.

**Specific Ask:**
How do you tune Nx's affected graph for a monorepo where documentation changes (Storybook stories, README) should not trigger downstream rebuilds? Is the implicitDependencies configuration the right lever? And what's the tradeoff of using Nx Cloud remote caching vs. GitHub Actions artifact caching for build performance?""",

"""**Context:**
Our GitHub Actions CI pipeline for the Next.js dashboard takes 18 minutes end-to-end: type-check (3m), lint (2m), unit tests (6m), build (5m), e2e tests (2m).

**Observed Issue:**
These steps run sequentially. Most could be parallelized but we haven't invested in the CI configuration. Our Playwright e2e tests also run against a locally-started Next.js dev server, which misses production-build-specific bugs.

**Specific Ask:**
What's the optimal GitHub Actions pipeline structure for a Next.js + TypeScript + Playwright app? Which steps can safely run in parallel? Should e2e tests run against the production build (next build + next start) rather than next dev? And how do you cache node_modules, Next.js build output, and Playwright browsers effectively to minimize cache miss rebuild time?""",

]
