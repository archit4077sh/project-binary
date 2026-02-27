"""
snippets/q_typescript.py — 28 FRESH TypeScript questions (mix of debugging + code generation)
Zero overlap with archived set.
"""

Q_TYPESCRIPT = [

"""**Task (Code Generation):**
Implement a type-safe `pipe` function that composes up to 5 functions left-to-right with correct TypeScript inference:

```ts
const result = pipe(
  (s: string) => s.split(','),
  (arr: string[]) => arr.map(Number),
  (nums: number[]) => nums.filter(Boolean),
  (nums: number[]) => nums.reduce((a, b) => a + b, 0)
); // inferred as (s: string) => number
```

Use function overloads for arities 1-5. Explain why a single generic signature with rest params doesn't work for this use case and what variadic tuple types offer.""",

"""**Debug Scenario:**
A generic `Repository<T>` class has a method `findById` that should return `T | null`. TypeScript infers it as `T | null` correctly at the class level, but when used through an interface, TypeScript widens the return type to `object | null`.

```ts
interface IRepository<T> {
  findById(id: string): Promise<T | null>;
}
class UserRepo implements IRepository<User> {
  async findById(id: string) {
    return db.user.findUnique({ where: { id } }); // returns User | null
  }
}
const repo: IRepository<User> = new UserRepo();
const user = await repo.findById('1'); // typed as object | null ??
```

Diagnose why the return type widens through the interface and fix it.""",

"""**Task (Code Generation):**
Build a type-safe event emitter class with full TypeScript inference:

```ts
const emitter = new TypedEmitter<{
  'user:login': { userId: string; timestamp: number };
  'user:logout': { userId: string };
  'data:update': { rows: Row[]; total: number };
}>();

emitter.on('user:login', (payload) => {
  payload.userId; // correctly typed as string
  payload.timestamp; // number
});
```

The `on`, `off`, `emit` methods must all be fully typed from the event map. Show the implementation using mapped types and template literal keys.""",

"""**Debug Scenario:**
A utility type `DeepPartial<T>` is used to allow partial updates to nested config objects. It works for plain objects but fails for `Date`, `Map`, `Set`, and array types.

```ts
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};
// Problem: Date extends object → DeepPartial<Date> makes all Date methods optional
// Problem: Array extends object → DeepPartial<string[]> = { [n: number]?: ... }
```

Fix `DeepPartial` to correctly handle built-in types (Date, Map, Set, Arrays) that should be preserved as-is rather than recursed into.""",

"""**Task (Code Generation):**
Implement a `Result<T, E>` type (Railway-oriented programming) with a full API:

```ts
const result = await Result.tryAsync(() => fetchUser(id));
result
  .map(user => user.name)
  .mapError(err => new AppError(err))
  .getOrElse('Unknown');
```

Requirements:
- `Result.ok(value)`, `Result.err(error)`, `Result.tryAsync(fn)`
- `map`, `mapError`, `flatMap`, `match`, `getOrElse`, `getOrThrow`
- Full TypeScript generics preserving types through the chain
- No runtime dependency — pure TypeScript class""",

"""**Debug Scenario:**
A TypeScript project uses `as const` on a large configuration object. Several functions accept keys from this config as parameters. TypeScript correctly narrows the types at the call site but loses the narrowing inside the function body.

```ts
const CONFIG = { timeout: 3000, retries: 3, endpoint: '/api' } as const;
type ConfigKey = keyof typeof CONFIG;

function getConfig<K extends ConfigKey>(key: K): typeof CONFIG[K] {
  return CONFIG[key]; // Error: Type 'number | string' is not assignable to type 'typeof CONFIG[K]'
}
```

Explain why TypeScript loses the indexed access type inside the generic function and provide the correct fix.""",

"""**Task (Code Generation):**
Create a `Schema` builder DSL for runtime validation that also produces TypeScript types:

```ts
const UserSchema = Schema.object({
  id: Schema.string().uuid(),
  age: Schema.number().min(0).max(150),
  role: Schema.enum(['admin', 'user', 'viewer'] as const),
  tags: Schema.array(Schema.string()),
});

type User = InferSchema<typeof UserSchema>; // { id: string; age: number; role: 'admin'|'user'|'viewer'; tags: string[] }
const user = UserSchema.parse(rawData); // throws if invalid
```

Implement the schema builder without using Zod (for learning purposes). Show `object`, `string`, `number`, `enum`, `array`.""",

"""**Debug Scenario:**
A function overload is set up for a common utility, but TypeScript always picks the wrong overload in a specific pattern:

```ts
function format(value: string): string;
function format(value: number): string;
function format(value: string | number): string {
  return String(value);
}

function formatMany<T extends string | number>(values: T[]): string[] {
  return values.map(v => format(v)); // Error: Argument of type 'T' is not assignable
}
```

Explain why overloads fail to resolve in generic contexts, and provide two correct alternatives: one using conditional types, one restructuring to avoid overloads.""",

"""**Task (Code Generation):**
Implement a `Middleware<Context>` pattern for building composable request processing pipelines:

```ts
type Next<C> = (ctx: C) => Promise<void>;
type Middleware<C> = (ctx: C, next: Next<C>) => Promise<void>;

const app = compose<RequestContext>([
  withAuth,
  withLogging,
  withErrorHandler,
  handler,
]);
```

Show the `compose` function, three sample middleware implementations, and proper TypeScript types that ensure the context is passed correctly through the chain.""",

"""**Debug Scenario:**
TypeScript's `strictFunctionTypes` causes surprising errors when assigning callback types in a React-like framework:

```ts
type EventHandler<E extends Event> = (event: E) => void;

const handlers: EventHandler<Event>[] = [];
const clickHandler: EventHandler<MouseEvent> = (e) => console.log(e.clientX);

handlers.push(clickHandler); // Error: MouseEvent is not assignable to Event
```

This error blocks storing heterogeneous event handlers in an array. Explain the variance issue, show why `Function` or `any` are bad fixes, and design a correct type that allows storing handlers for different event types in the same array.""",

"""**Task (Code Generation):**
Build a `DeepReadonly<T>` utility type that makes all nested properties immutable, correctly handling edge cases:
- Arrays → `ReadonlyArray`
- Functions → unchanged (don't freeze functions)
- `Map<K, V>` → `ReadonlyMap<K, V>`
- `Set<T>` → `ReadonlySet<T>`
- Primitive types → unchanged
- Circular references → handled without infinite recursion

Show the implementation and test cases for each edge case.""",

"""**Debug Scenario:**
A team uses declaration merging to extend a third-party `Config` interface. After upgrading the library, the merged interface has duplicate property conflicts.

```ts
// lib types:
interface Config { timeout: number; }
// local augmentation:
declare module 'some-lib' {
  interface Config { timeout: string; } // conflicts with number!
}
```

TypeScript silently takes the local `timeout: string` definition, causing runtime errors because the library sends `timeout` as a number. Explain how TypeScript resolves interface merge conflicts, and propose a versioning strategy to detect these conflicts during upgrades.""",

"""**Task (Code Generation):**
Implement a `StateMachine<States, Events>` type-safe class:

```ts
const machine = new StateMachine({
  initial: 'idle',
  states: {
    idle: { on: { START: 'loading' } },
    loading: { on: { SUCCESS: 'done', FAILURE: 'error' } },
    done: { on: { RESET: 'idle' } },
    error: { on: { RETRY: 'loading', RESET: 'idle' } },
  }
});

machine.send('START'); // ok — transitions to 'loading'
machine.send('SUCCESS'); // ok
machine.send('START'); // TypeScript error: 'START' not valid in 'done' state
```

Make invalid transitions a compile-time error using template literal types and mapped types.""",

"""**Debug Scenario:**
A project uses `tsconfig.json` path aliases widely (`@/components`, `@/utils`). After setting up a monorepo with workspaces, the aliases break in cross-package imports — TypeScript can find types but the runtime module resolution fails.

```json
// packages/app/tsconfig.json
{ "paths": { "@/*": ["./src/*"] } }
// packages/ui/index.ts imports from '@/components' ← breaks
```

Explain the difference between TypeScript's `paths` (type resolution) and runtime module resolution (Node.js, Webpack, Jest), and show the correct tsconfig `references` + runtime alias setup for each tool.""",

"""**Task (Code Generation):**
Implement a `useTypedReducer<S, A>` hook that wraps `useReducer` with exhaustive action type checking:

```ts
type Action =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_DATA'; payload: User[] }
  | { type: 'SET_ERROR'; payload: string };

const [state, dispatch] = useTypedReducer<State, Action>(reducer, initialState);

dispatch({ type: 'SET_LOADING', payload: true }); // OK
dispatch({ type: 'TYPO' }); // TypeScript Error
```

Show the hook implementation and a `createReducer` helper that ensures all action types in the union are handled (exhaustive switch).""",

"""**Debug Scenario:**
A TypeScript codebase has a utility function `assertNever(x: never): never` for exhaustive checks. After adding a new variant to a discriminated union, the compiler fails to error at the `assertNever` call as expected.

```ts
type Shape = Circle | Square | Triangle; // Triangle just added
function area(s: Shape): number {
  switch (s.kind) {
    case 'circle': return Math.PI * s.r ** 2;
    case 'square': return s.side ** 2;
    default: return assertNever(s); // Should error but doesn't
  }
}
```

TypeScript reports no error even though `Triangle` isn't handled. Diagnose why (hint: check the TypeScript version and `useUnknownInCatchVariables`) and fix the `assertNever` pattern to be reliable.""",

"""**Task (Code Generation):**
Build a `createStore<S>` function (like a tiny Zustand) with full TypeScript types:

```ts
const useStore = createStore<{ count: number; name: string }>((set) => ({
  count: 0,
  name: 'user',
  increment: () => set(s => ({ count: s.count + 1 })),
  setName: (name: string) => set({ name }),
}));

const count = useStore(s => s.count); // number
const name = useStore(s => s.name);   // string
```

The selector must be typed correctly. Actions must be part of the store state type. Show a minimal but fully-typed implementation.""",

"""**Debug Scenario:**
A team migrated from CommonJS to ESM. After the migration, `typeof require` checks that used to work break at type-checking time:

```ts
if (typeof require !== 'undefined') {
  // CJS environment
  const fs = require('fs');
}
```

TypeScript reports `'require' is not defined` because the tsconfig targets ESM. But the code needs to work in both CJS and ESM at runtime. Show how to correctly type-check dual-mode code and whether `import.meta.url` vs `__dirname` vs `createRequire` is the right cross-environment solution.""",

"""**Task (Code Generation):**
Implement `Prettify<T>`, `Exact<T, U>`, and `StrictOmit<T, K>` utility types:

1. `Prettify<T>` — flattens intersections to show final shape in hover tooltips
2. `Exact<T, U>` — ensures `T` has exactly the same keys as `U` (no extra, no missing)
3. `StrictOmit<T, K>` — like `Omit` but `K` must be `keyof T` (unlike built-in Omit which allows non-existent keys)

Show each implementation with examples demonstrating where the built-in utilities fall short.""",

"""**Debug Scenario:**
A TypeScript generic class uses `this` type for fluent method chaining. When the class is extended, the `this` type works but the constructor type inference breaks.

```ts
class QueryBuilder<T> {
  where(condition: Partial<T>): this { return this; }
  limit(n: number): this { return this; }
}
class UserQuery extends QueryBuilder<User> {
  withActive(): this { return this.where({ active: true }); }
}
const q = new UserQuery().withActive().where({ name: 'Alice' }).limit(10);
// q is typed as UserQuery ✓ (this typing works)

// But:
function buildQuery<T, Q extends QueryBuilder<T>>(Builder: new() => Q): Q {
  return new Builder(); // Error: Cannot assign 'QueryBuilder<T>' to 'Q'
}
```

Explain the constructor type inference limitation and fix `buildQuery` to correctly infer the specific subclass type.""",

"""**Task (Code Generation):**
Implement a type-safe HTTP client builder:

```ts
const client = createHttpClient('https://api.example.com')
  .withAuth(token)
  .withTimeout(5000)
  .withRetry({ attempts: 3, backoff: 'exponential' });

// Fully typed response:
const { data } = await client.get<User[]>('/users');
const { data: report } = await client.post<Report>('/reports', { title: 'Q1' });
```

Show the builder pattern implementation with TypeScript generics for the response type, and the `RequestConfig` type with all options.""",

"""**Debug Scenario:**
TypeScript's `keyof` produces a surprising union when applied to an interface with both string and number index signatures:

```ts
interface Dict {
  [key: string]: unknown;
  [key: number]: unknown;
  name: string;
}
type K = keyof Dict; // string | number — NOT 'name' | string | number
```

Callers expected to use `'name'` as an autocomplete-able key, but it's swallowed by the index signature. Explain how index signatures affect `keyof`, and show how to design `Dict` so named properties remain discoverable while still supporting dynamic keys.""",

"""**Task (Code Generation):**
Implement a `zodToFormik` adapter that converts a Zod schema into a Formik initial values object and validation function:

```ts
const schema = z.object({
  email: z.string().email(),
  age: z.number().min(18),
  role: z.enum(['admin', 'user']),
});

const { initialValues, validate } = zodToFormik(schema);
// initialValues: { email: '', age: 0, role: 'admin' }
// validate: (values) => errors object compatible with Formik
```

Show the recursive `getDefaultValue` for each Zod type and the `validate` adapter that converts Zod errors to Formik's nested error format.""",

"""**Debug Scenario:**
A codebase applies `readonly` to function parameters to prevent mutation. After enabling `strictFunctionTypes`, functions that accept `readonly` arrays can't be passed where mutable arrays are expected and vice versa.

```ts
function sum(nums: readonly number[]): number { ... }
const data: number[] = [1, 2, 3];
const result = sum(data); // OK ✓

function mutate(nums: number[]): void { nums.push(4); }
const frozen: readonly number[] = [1, 2, 3];
mutate(frozen); // Error ✓ (correctly blocked)

// But:
type Transform = (nums: number[]) => number[];
const safeTransform: (nums: readonly number[]) => readonly number[] = ...;
const t: Transform = safeTransform; // Error? Or allowed?
```

Explain the covariance/contravariance rules that govern `readonly` array assignability.""",

"""**Task (Code Generation):**
Build a `createQueryKey` factory for React Query that generates type-safe, structured query keys:

```ts
const keys = createQueryKey('reports', {
  list: (filter: ReportFilter) => [filter],
  detail: (id: string) => [id],
  comments: (reportId: string, page: number) => [reportId, page],
});

keys.list({ status: 'active' }); // ['reports', 'list', { status: 'active' }]
keys.detail('123');               // ['reports', 'detail', '123']
keys.all;                         // ['reports'] — invalidates everything
```

The return types must match what React Query expects for `queryKey`. Show the factory implementation with full TypeScript types.""",

"""**Debug Scenario:**
A Next.js project uses `ts-morph` to generate TypeScript types from a database schema at build time. The generated types are correct but `tsc` takes 45 seconds to type-check — up from 8 seconds before the generators were added.

Investigation with `tsc --diagnostics` shows `checkTime` dominated by a single 8,000-line generated file with deeply nested conditional types.

Explain TypeScript's type-checking complexity for conditional types (exponential in the worst case), and show how to restructure the generated types using interfaces + module augmentation instead of deeply nested conditionals to bring check time back to acceptable levels.""",

"""**Task (Code Generation):**
Implement a `parseCsv<T>` function using TypeScript template literal types to validate CSV headers at compile time:

```ts
const rows = parseCsv<{ name: string; age: number; email: string }>(
  csvString,
  { name: 'Name', age: 'Age (years)', email: 'Email Address' }
); // rows: { name: string; age: number; email: string }[]
```

The column mapping must be checked: every key of `T` must appear in the mapping, and no extra keys allowed. The parser converts string columns to the appropriate TypeScript type (`string` → as-is, `number` → `parseFloat`).""",

"""**Task (Code Generation):**
Implement a `useZodForm` hook that bridges Zod schema inference with React state, providing type-safe form validation without a dedicated form library:

```ts
const { values, errors, handleChange, handleSubmit, isValid } = useZodForm(
  z.object({
    username: z.string().min(3).max(20),
    email: z.string().email(),
    age: z.number().min(18),
  }),
  { username: '', email: '', age: 0 }
);
// values.username is typed as string ✓
// errors.email is typed as string | undefined ✓
```

Show: the hook implementation, how Zod's `safeParse` drives validation on submit, how to convert `ZodError.flatten()` into a flat `{[field]: string}` errors object, and the TypeScript generics that infer field names and types from the schema.""",

]
