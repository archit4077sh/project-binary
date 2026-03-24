"""
snippets/q_typescript.py — BATCH 6: 56 brand-new TypeScript questions
Zero overlap with batches 1-5 archives.
"""

Q_TYPESCRIPT = [

"""**Task (Code Generation):**
Implement a `ParseJSON<S extends string>` type that extracts TypeScript types from a JSON string literal:

```ts
type Data = ParseJSON<'{"name":"Alice","age":30,"active":true}'>;
// Result: { name: string; age: number; active: boolean }

type Arr = ParseJSON<'[1,2,3]'>;
// Result: number[]
```

Show: template literal types recursively matching JSON value patterns (string literals, number literals, boolean), the `Trim` helper type (removes whitespace), `SplitPairs<S>` for parsing `key:value` pairs, and why this only works for literal types (not runtime values).""",

"""**Task (Code Generation):**
Build a `TypedEventBus<Events>` with strict event name and payload type checking:

```ts
type AppEvents = {
  'user:login':  { userId: string; timestamp: number };
  'cart:update': { itemCount: number; total: number };
  'error':       { code: string; message: string };
};

const bus = createEventBus<AppEvents>();

bus.emit('user:login', { userId: 'u1', timestamp: Date.now() });   // OK
bus.emit('user:login', { userId: 'u1' });                          // Error: missing timestamp
bus.emit('unknown:event', {});                                     // Error: unknown event

bus.on('cart:update', (payload) => {
  console.log(payload.itemCount); // TypeScript: number
});
```

Show: the generic `emit<K extends keyof Events>(event: K, payload: Events[K])` signature, typed `on` listener with strongly-typed payload, `off` for listener removal with the same type constraints, and a wildcard `on('*', handler)` overload that receives all events.""",

"""**Task (Code Generation):**
Implement a `DeepReadonly<T>` type that recursively makes all properties readonly:

```ts
type Config = {
  server: { host: string; port: number; ssl: { enabled: boolean; cert: string } };
  features: { darkMode: boolean; analytics: Analytics };
};

type FrozenConfig = DeepReadonly<Config>;
// server.ssl.cert and all nested props become readonly
```

Show: the base case (primitive types → unchanged), the recursive case (objects → map all values through `DeepReadonly`), handling arrays (`readonly T[]` vs `ReadonlyArray<T>`), handling functions (leave unchanged), and handling `Map`/`Set` (convert to `ReadonlyMap`/`ReadonlySet`).""",

"""**Task (Code Generation):**
Build a `createTypeSafeReducer<State, Actions>` factory:

```ts
type CounterState = { count: number; step: number };
type CounterActions =
  | { type: 'INCREMENT' }
  | { type: 'DECREMENT' }
  | { type: 'SET_STEP'; step: number }
  | { type: 'RESET' };

const counterReducer = createTypeSafeReducer<CounterState, CounterActions>({
  INCREMENT: (state) => ({ ...state, count: state.count + state.step }),
  DECREMENT: (state) => ({ ...state, count: state.count - state.step }),
  SET_STEP:  (state, action) => ({ ...state, step: action.step }),
  RESET:     () => ({ count: 0, step: 1 }),
});
```

Show: the handler map type (`{ [K in Actions['type']]: (state: State, action: Extract<Actions, { type: K }>) => State }`), TypeScript exhaustiveness checking (compile error if a `type` is missing from the map), and the curried reducer function returned by the factory.""",

"""**Task (Code Generation):**
Implement a `Paths<T>` type that generates all valid property path strings of a nested object:

```ts
type User = {
  name: string;
  address: { city: string; zip: string };
  settings: { theme: 'light' | 'dark'; notifications: { email: boolean } };
};

type UserPaths = Paths<User>;
// 'name' | 'address' | 'address.city' | 'address.zip' | 'settings' | 'settings.theme' | 'settings.notifications' | 'settings.notifications.email'

type PathValue = PathValueAt<User, 'settings.notifications.email'>; // boolean
```

Show: the recursive template literal type building paths, the `PathValueAt<T, P>` companion type that resolves the value type at a given path, and limiting depth to prevent infinite recursion on circular types (`MaxDepth = 5` constraint).""",

"""**Task (Code Generation):**
Build a `createMachine<Schema>` for a fully type-safe XState-style state machine:

```ts
const trafficLight = createMachine({
  id: 'traffic',
  initial: 'red',
  states: {
    red:    { on: { TIMER: 'green' } },
    green:  { on: { TIMER: 'yellow' } },
    yellow: { on: { TIMER: 'red' } },
  },
} as const);

const service = interpret(trafficLight);
service.send('TIMER');  // OK
service.send('INVALID'); // TypeScript Error: 'INVALID' is not a valid event
```

Show: inferring `States` and `Events` from the schema using `typeof ... as const`, the `interpret` function typing `send` to only accept valid events for the current state, transition validation at compile time, and `createMachine` with context for machines that carry data alongside state.""",

"""**Task (Code Generation):**
Implement a `Pipeline<Input, Output>` type for a fluent data transformation chain:

```ts
const transform = pipeline<RawUser>()
  .pipe((u) => ({ ...u, fullName: `${u.firstName} ${u.lastName}` }))
  .pipe((u) => ({ ...u, initials: u.fullName.split(' ').map(w => w[0]).join('') }))
  .pipe(async (u) => ({ ...u, avatar: await fetchAvatar(u.id) }))
  .build();

const result = await transform(rawUser);
// Type: RawUser & { fullName: string, initials: string, avatar: string }
```

Show: the `pipe` method type signature that accumulates the return types (`PipeResult<A, B> = A & B`), async step handling (if any step returns `Promise<T>`, the final result is `Promise<FinalType>`), TypeScript's conditional types for async detection, and compile-time validation that each step's input type is compatible with the previous step's output.""",

"""**Task (Code Generation):**
Build a `StrictOmit<T, K>` type where `K` must be keys that actually exist in `T`:

```ts
type User = { id: string; email: string; password: string; role: string };

type PublicUser = StrictOmit<User, 'password'>;   // OK
type BadOmit    = StrictOmit<User, 'nonExistent'>; // TypeScript Error: 'nonExistent' not in User
```

Also build `StrictPick<T, K>`, `StrictRequired<T, K>`, and `StrictPartial<T, K>` (only specific fields optional/required).

Show: the constraint `K extends keyof T`, the full utility types, and how `StrictRequired` works (`Required<Pick<T, K>> & Omit<T, K>`).""",

"""**Task (Code Generation):**
Implement a `createQueryString<Schema>` builder with typed parameters:

```ts
type SearchSchema = {
  q: string;
  page?: number;
  limit?: number;
  sort?: 'asc' | 'desc';
  tags?: string[];
};

const buildURL = createQueryString<SearchSchema>(new URL('https://example.com/api/search'));

const url = buildURL({ q: 'typescript', page: 2, tags: ['react', 'nextjs'] });
// https://example.com/api/search?q=typescript&page=2&tags=react&tags=nextjs

buildURL({ q: 'hello', sort: 'invalid' }); // TypeScript Error: type '"invalid"' not assignable
```

Show: the generic type constraint ensuring all keys match `Schema`, array handling (multiple `key=value` pairs), omitting `undefined` values, and the `parseQueryString<Schema>(url)` inverse function that validates and parses.""",

"""**Task (Code Generation):**
Build a `createDI<Container>` for a lightweight dependency injection container:

```ts
const container = createDI({
  db:         () => new DatabasePool(process.env.DATABASE_URL!),
  cache:      () => new RedisCache(process.env.REDIS_URL!),
  userRepo:   (deps) => new UserRepository(deps.db),
  authService:(deps) => new AuthService(deps.userRepo, deps.cache),
  emailService:() => new EmailService(process.env.SMTP_HOST!),
});

// TypeScript infers the resolved type:
const auth = container.resolve('authService'); // AuthService
const db   = container.resolve('unknownDep'); // TypeScript Error!
```

Show: the `Container` type where each factory's `deps` arg is typed as the resolved values of other registered services, circular dependency detection at the type level, lazy initialization (instantiated on first `resolve`), and scoped containers (`container.createScope()`) where scoped instances are shared within a scope.""",

"""**Task (Code Generation):**
Implement a `Schema<T>` runtime validation type that generates TypeScript types AND runtime validators from a single definition:

```ts
const UserSchema = Schema.object({
  id:    Schema.string().uuid(),
  email: Schema.string().email(),
  age:   Schema.number().int().min(0).max(150).optional(),
  role:  Schema.enum(['admin', 'user', 'guest'] as const),
});

type User = Schema.infer<typeof UserSchema>;
// { id: string; email: string; age?: number; role: 'admin' | 'user' | 'guest' }

const result = UserSchema.parse(unknownInput);
// result.success: boolean, result.data: User | result.errors: ValidationError[]
```

Show: the fluent builder pattern, `Schema.infer<T>` extracting the TypeScript type from the schema, runtime validation with detailed error paths, and `Schema.array(UserSchema)` for array schemas.""",

"""**Task (Code Generation):**
Build a `useTypedLocalStorage<T>` hook with schema validation on read:

```ts
const [session, setSession] = useTypedLocalStorage('user-session', {
  schema: SessionSchema,           // Zod or custom validator
  defaultValue: null,
  serialize: (v) => JSON.stringify(v) + '_v2',  // versioned format
  deserialize: (raw) => {
    const str = raw.replace('_v2', '');
    return JSON.parse(str);
  },
});

setSession({ userId: 'u1', token: 'abc123', expiresAt: Date.now() + 3600_000 });
```

Show: the read path: deserialize → validate with schema → fallback to `defaultValue` on parse error, the `storage` event listener for cross-tab sync, `useSyncExternalStore` for React-safe reads, and TypeScript inferring `T` from the `schema`'s output type.""",

"""**Task (Code Generation):**
Implement a `Flatten<T>` type that deeply flattens nested arrays:

```ts
type Nested = [1, [2, 3], [[4, 5]], [[[[6]]]]];
type Flat = Flatten<Nested>; // [1, 2, 3, 4, 5, 6]

type Mixed = [string, [number, [boolean, string[]]]];
type FlatMixed = Flatten<Mixed>; // [string, number, boolean, ...string[]]
```

Show: the recursive conditional type (`T extends Array<infer Item>` → `Flatten<Item>` : `T`), the `infer` usage for tuple element extraction, handling empty arrays and `never`, and the depth limit with `Depth extends number[]` accumulator to avoid TypeScript's recursion limit.""",

"""**Task (Code Generation):**
Build a `createAPIClient<Routes>` with end-to-end type safety between client and server:

```ts
// Shared type (used by both client and server):
type AppAPI = {
  '/users':          { GET: { query: { limit?: number }; response: User[] } };
  '/users/:id':      { GET: { params: { id: string }; response: User }; DELETE: { params: { id: string }; response: void } };
  '/users/:id/posts':{ GET: { params: { id: string }; response: Post[] }; POST: { params: { id: string }; body: CreatePost; response: Post } };
};

const client = createAPIClient<AppAPI>('https://api.example.com');

const users  = await client.get('/users', { query: { limit: 10 } });   // User[]
const user   = await client.get('/users/:id', { params: { id: 'u1' } }); // User
const post   = await client.post('/users/:id/posts', {                   // Post
  params: { id: 'u1' },
  body: { title: 'Hello World' },
});
```

Show: path parameter replacement at runtime (`/users/:id` → `/users/u1`), the TypeScript overloads for `get`, `post`, `put`, `delete` methods, automatic response type inference, and validation with Zod on both client (response) and server (request body/params).""",

"""**Task (Code Generation):**
Implement a `Mutable<T>` type hierarchy that toggles mutability at each level:

```ts
type Immutable = {
  readonly id: string;
  readonly config: { readonly host: string; readonly port: number };
};

type MutableVersion  = Mutable<Immutable>;
// { id: string; config: { host: string; port: number } }

// Also implement ShallowMutable (only removes readonly at top level):
type ShallowMutable = ShallowMutable<Immutable>;
// { id: string; config: { readonly host: string; readonly port: number } }
```

Show: the `-readonly` mapped type modifier, the `DeepMutable` recursive variant, and utility application: `Mutable<ReturnType<typeof createConfig>>` for making config objects modifiable in tests.""",

"""**Task (Code Generation):**
Build a `PermissionGuard<Role, Permission>` type system for RBAC:

```ts
type Roles = 'admin' | 'manager' | 'user' | 'guest';

type RolePermissions = {
  admin:   'read' | 'write' | 'delete' | 'admin';
  manager: 'read' | 'write' | 'delete';
  user:    'read' | 'write';
  guest:   'read';
};

// TypeScript enforces that only valid permissions for the role are passed:
function requirePermission<R extends Roles>(role: R, permission: RolePermissions[R]): void;

requirePermission('admin', 'admin');       // OK
requirePermission('user', 'delete');       // TypeScript Error!
requirePermission('guest', 'read');        // OK
requirePermission('manager', 'admin');     // TypeScript Error!
```

Show: the discriminated union for access control, the `HasPermission<Role, Permission>` type returning `true | false`, and `WithRole<R extends Roles>` generic that constrains function arguments to role-specific permissions.""",

# ── Debugging ─────────────────────────────────────────────────────────────────

"""**Debug Scenario:**
TypeScript infers `any` for a generic function when the type parameter should be inferred from a deeply nested argument:

```ts
function extractField<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const result = extractField({ name: 'Alice', age: 30 }, 'name');
// result: string  ✓ — works for direct object

type Wrapper<T> = { value: T };
function extractWrapped<T, K extends keyof T>(wrapped: Wrapper<T>, key: K): T[K] {
  return wrapped.value[key];
}

const res2 = extractWrapped({ value: { name: 'Alice' } }, 'name');
// res2: any  ✗ — T isn't inferred from nested .value
```

TypeScript can't always infer type parameters from nested generics. Show: explicitly providing the type parameter `extractWrapped<{ name: string }, 'name'>(...)`, or restructuring using `infer` in a conditional type, and the `satisfies` operator to constrain types without losing inference.""",

"""**Debug Scenario:**
A TypeScript `type` alias for a discriminated union stops narrowing correctly after being spread:

```ts
type Result<T> = { success: true; data: T } | { success: false; error: string };

function spreadBug(result: Result<User>) {
  const { success, ...rest } = result;
  if (success) {
    rest.data; // Error: Property 'data' does not exist on type '{ error: string; }'
    // TypeScript doesn't narrow 'rest' based on 'success'!
  }
}
```

Destructuring breaks discriminated union narrowing — TypeScript can't correlate `success` with the spread `rest`. Show: keeping the original `result` object for narrowing (`if (result.success) result.data`), the `if (success)` narrowing only applies to the `success` variable (not correlated with `rest`), and TypeScript 5.4's narrowing improvements for correlated union types.""",

"""**Debug Scenario:**
`Object.keys()` returns `string[]` instead of `(keyof T)[]`, causing TypeScript errors when iterating an object:

```ts
type Config = { host: string; port: number; ssl: boolean };
const config: Config = { host: 'localhost', port: 3000, ssl: false };

for (const key of Object.keys(config)) {
  console.log(config[key]); // Error: Element implicitly has an 'any' type
  // because key is 'string', not keyof Config
}
```

`Object.keys()` is typed to return `string[]` intentionally — objects can have extra keys at runtime beyond what TypeScript knows. Show: using `(Object.keys(config) as Array<keyof Config>)` as a cast, implementing a `typedKeys<T>(obj: T): (keyof T)[]` helper with the cast inside, and the subtle reason why string[] is correct (structural typing — `config` might actually have extra keys).""",

"""**Debug Scenario:**
A TypeScript `interface` augmentation for a third-party library throws "Duplicate identifier" in production builds but not in development:

```ts
// types/express.d.ts:
import 'express';
declare module 'express' {
  interface Request {
    user?: User;
  }
}

// server.ts:
// Also has a local augmentation! (copy-pasted from a tutorial):
declare module 'express' {
  interface Request {
    user?: User; // Duplicate!
  }
}
```

Two files both augment `express.Request`. In development, one file might not be picked up by the TypeScript language server, masking the duplicate. Show: consolidating all augmentations into a single `types/` folder entry, ensuring `tsconfig.json` `typeRoots` and `types` are properly set, and the correct pattern for augmenting third-party module types.""",

"""**Debug Scenario:**
TypeScript throws "Type 'string' is not assignable to type 'never'" in a switch-case that should be exhaustive:

```ts
type Color = 'red' | 'green' | 'blue';

function getHex(color: Color): string {
  switch (color) {
    case 'red':   return '#ff0000';
    case 'green': return '#00ff00';
    // Missing: 'blue'!
  }
  // TypeScript: 'color' is type 'blue' here (unhandled), not 'never'!
  const _exhaustive: never = color; // Error: Type 'blue' is not assignable to type 'never'
}
```

Show: completing the switch with `case 'blue': return '#0000ff'`, the `assertNever` pattern (`function assertNever(x: never): never { throw new Error(...) }`), and using it as a default case instead of a post-switch assertion.""",

"""**Debug Scenario:**
A TypeScript generic function has an unexpected `any` when using a conditional type with `infer`:

```ts
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;

function unwrap<T>(value: T): UnwrapPromise<T> {
  return value instanceof Promise ? value.then(v => v) : value;
  // Error: Type 'T | Promise<any>' is not assignable to type 'UnwrapPromise<T>'
}
```

TypeScript can't verify the function body satisfies `UnwrapPromise<T>` because `T` is generic — the conditional type isn't resolved until `T` is known. Show: using function overloads (`function unwrap(v: Promise<T>): T; function unwrap<T>(v: T): T; function unwrap(v: any)`) as the implementation signature, and the `as UnwrapPromise<T>` cast as a pragmatic workaround.""",

"""**Debug Scenario:**
TypeScript intersection types produce an unexpected `never` when intersecting incompatible primitive types:

```ts
type A = { kind: 'circle'; radius: number };
type B = { kind: 'square'; side: number };
type AB = A & B;
// AB.kind is: 'circle' & 'square' = never!
// AB itself is technically valid but unusable — kind can never be assigned

const x: AB = { kind: ???, radius: 5, side: 10 }; // impossible!
```

Show: using discriminated unions instead of intersections for this pattern (`type Shape = A | B`), the legitimate use cases for intersections (mixing capabilities: `type Editor = TextFeatures & FormattingFeatures`), and `IsNever<T>` helper type (`T extends never ? true : false`).""",

"""**Debug Scenario:**
A TypeScript `class` implements two interfaces but one has a method with the same name and different signature — TypeScript accepts the class but the method is ambiguously typed:

```ts
interface Serializable {
  serialize(): string;
}
interface Saveable {
  serialize(): Promise<string>; // DIFFERENT return type!
}

class Document implements Serializable, Saveable {
  serialize(): string | Promise<string> { // TypeScript accepts this...
    return JSON.stringify(this.data);     // but the overloaded sig is confusing
  }
}
```

Show: explicitly overloading `serialize` to handle both cases, using a separate method for `Saveable.serialize`, and the design recommendation against using the same method name with different semantics in interfaces meant to be combined.""",

"""**Debug Scenario:**
A TypeScript function that accepts an object with default parameters loses type narrowing:

```ts
function processUser({ role = 'user', permissions = [] }: Partial<UserOptions> = {}) {
  if (role === 'admin') {
    // TypeScript: role is 'admin' here ✓
    permissions; // TypeScript: string[] | undefined — but it should be string[]!
  }
}
```

Narrowing `role === 'admin'` doesn't narrow `permissions` — TypeScript doesn't model multi-property narrowing for destructured parameters. Show: explicitly narrowing `permissions` with `permissions ?? []`, typing with discriminated unions (`AdminOptions | UserOptions`), and the `satisfies` operator to verify type compatibility without widening.""",

"""**Debug Scenario:**
TypeScript reports "Property 'X' does not exist on type 'Y'" for a type guard that should have narrowed the type:

```ts
function isAdmin(user: User): user is AdminUser {
  return user.role === 'admin';
}

function handleUser(user: User) {
  if (isAdmin(user)) {
    user.adminSecret; // Error: Property 'adminSecret' does not exist on type 'User'
  }
}
```

Investigation: `AdminUser` is not imported in the file where `handleUser` is defined, causing silent resolution failure. The `is AdminUser` predicate is ignored because TypeScript can't resolve the type. Show: ensuring `AdminUser` is imported in the consuming file, using inline type predicates (`user is User & { adminSecret: string }`) as an alternative, and verifying type guard effectiveness with `// @ts-expect-error` tests.""",

"""**Debug Scenario:**
A TypeScript mapped type over a union produces incorrect results:

```ts
type Stringify<T> = { [K in keyof T]: string };

type Unioned = Stringify<{ a: number } | { b: boolean }>;
// Expected: { a: string } | { b: string }
// Actual:   { a: string; b: string } — merged, not unioned!
```

Mapped types distribute over unions when applied to a bare type parameter. `Stringify<T>` with `T = A | B` maps EACH member separately only if `T` is a bare type parameter in the mapping. Show: using a distributive mapped type (`type Stringify<T> = T extends object ? { [K in keyof T]: string } : T`) to force distribution, the difference between distributive and non-distributive conditional types, and `[T] extends [U]` to prevent distribution.""",

"""**Debug Scenario:**
TypeScript doesn't narrow a type correctly when checking an enum value:

```ts
enum Status { Active = 'active', Inactive = 'inactive', Pending = 'pending' }

function handle(status: Status) {
  if (status !== Status.Inactive && status !== Status.Pending) {
    status; // TypeScript: still 'Status', not narrowed to 'Status.Active'!
  }
}
```

TypeScript doesn't narrow out-of-enum values from enum types in the way it does with string literal unions. Show: using a string literal union `type Status = 'active' | 'inactive' | 'pending'` instead of `enum` for better narrowing, using `if (status === Status.Active)` positive narrowing, and the `const enum` vs `enum` difference.""",

"""**Debug Scenario:**
A TypeScript project's `paths` alias in `tsconfig.json` works in the IDE but fails at runtime:

```json
// tsconfig.json:
{ "paths": { "@utils/*": ["./src/utils/*"] } }
```

```ts
import { formatDate } from '@utils/date'; // Works in TypeScript!
// At runtime: Cannot find module '@utils/date'
```

TypeScript `paths` are compile-time only — they don't transform actual import paths in the output JS (except when using `tsc`'s path rewriting in certain configs). Show: configuring the bundler (Vite: `resolve.alias`, Webpack: `resolve.alias`) to handle the same aliases, using `tsconfig-paths` for Node.js runtime resolution (`ts-node -r tsconfig-paths/register`), and Jest's `moduleNameMapper` for tests.""",

"""**Debug Scenario:**
A TypeScript `readonly` array causes an error when passing to a function expecting a mutable array:

```ts
const items = ['a', 'b', 'c'] as const; // readonly ['a', 'b', 'c']

function reverse(arr: string[]): string[] {
  return arr.reverse(); // arr.reverse() is fine
}

reverse(items); // Error: Argument of type 'readonly ["a","b","c"]' not assignable to parameter of type 'string[]'
```

`readonly` arrays aren't assignable to mutable arrays because the function could mutate. Show: typing `reverse` to accept `readonly string[]` (safe, function doesn't mutate), using `[...items]` to create a mutable copy before passing, `ReadonlyArray<string>` vs `readonly string[]` (same type, different syntax), and the `Readonly<T[]>` utility type.""",

"""**Debug Scenario:**
TypeScript complains about a `null` assertion (`!`) but the code is clearly safe:

```ts
const element = document.getElementById('app');
element!.addEventListener('click', handler); // Non-null assertion works

// But later:
const { style } = element!; // Error in strict mode: still complains!
function updateElement() {
  element!.style.color = 'red'; // TypeScript: Not safe — element! in different scope
}
```

`!` is a per-expression assertion — TypeScript doesn't remember the assertion across expressions or function boundaries. Show: declaring a separate narrowed variable (`const el = element!`), checking once and throwing (`if (!element) throw new Error('...')`), and using `??` with `document.createElement` as a fallback instead of asserting non-null.""",

"""**Debug Scenario:**
TypeScript `noUncheckedIndexedAccess` is enabled and code breaks in unexpected places:

```ts
// tsconfig.json: "noUncheckedIndexedAccess": true

const items = ['a', 'b', 'c'];
const first = items[0]; // Type: string | undefined  (was: string)
first.toUpperCase();    // Error: 'first' is possibly 'undefined'

// Expected: items[0] is definitely 'a', why is it undefined?
```

`noUncheckedIndexedAccess` adds `| undefined` to ALL index accesses, even when the index is statically known to be in-bounds. Show: checking before use (`if (first) first.toUpperCase()`), using destructuring with a default (`const [first = ''] = items`), using `items.at(0)` (still returns `string | undefined` with the flag), and when `noUncheckedIndexedAccess` is worth the verbosity (public APIs with unknown inputs).""",

"""**Debug Scenario:**
A TypeScript function using `ReturnType<typeof fn>` breaks when the function is overloaded:

```ts
function fetch(url: string): Promise<string>;
function fetch(url: string, options: Options): Promise<Response>;
function fetch(url: string, options?: Options): Promise<string | Response> {
  ...
}

type FetchReturn = ReturnType<typeof fetch>;
// Expected: Promise<string> | Promise<Response>
// Actual:   Promise<string | Response>  — picks the LAST overload!
```

`ReturnType<>` picks the last overload signature for overloaded functions. Show: defining separate typed functions and a union type manually (`type FetchReturn = Promise<string> | Promise<Response>`), using conditional types to simulate overloads without actual overloads, and the `OverloadUnion` utility type from the `type-fest` library.""",

"""**Debug Scenario:**
TypeScript's `strictFunctionTypes` causes a regression when passing a callback typing:

```ts
type Handler = (event: MouseEvent) => void;
type AnyHandler = (event: Event) => void;  // Event is broader

declare function addListener(handler: AnyHandler): void;

const mouseHandler: Handler = (e: MouseEvent) => console.log(e.button);
addListener(mouseHandler); // Error with strictFunctionTypes!
// Type 'Handler' is not assignable to type 'AnyHandler'
```

`strictFunctionTypes` enforces function type parameter contravariance — you can't use a `MouseEvent`-specific handler where an `Event` handler is expected (the function might be called with a `KeyboardEvent`). Show: widening the handler type (`(event: Event | MouseEvent) => void`), using `(event: Parameters<AnyHandler>[0]) => void` to properly type the parameter, and why contravariance is correct (callers of `AnyHandler` might pass non-MouseEvent events).""",

"""**Debug Scenario:**
A TypeScript project has circular type imports that cause "Type alias 'X' circularly references itself":

```ts
// user.ts:
import { Post } from './post';
export type User = { id: string; posts: Post[] };

// post.ts:
import { User } from './user';
export type Author = User; // Circular!
export type Post = { id: string; author: Author; content: string };
```

TypeScript usually handles circular type imports well, but the error appears when the types use `type` aliases that resolve through each other in a way the compiler can't fully evaluate. Show: using `interface` instead of `type` for object types (interfaces handle circular references better), forward declaring with `type Post = { ... }; type User = { posts: Post[] }` in a single file, and using `id: string` instead of the full type for back-references to break the cycle.""",

"""**Debug Scenario:**
TypeScript's template literal types don't match at runtime even though they compile correctly:

```ts
type EventName = `on${Capitalize<string>}`;
declare function on<E extends EventName>(event: E, handler: () => void): void;

on('onClick', () => {});  // OK
on('onSubmit', () => {}); // OK
on('click', () => {});    // TypeScript Error: 'click' doesn't match `on${string}` ✓

// But at runtime:
const event = 'onClick';
on(event as EventName, handler); // Works but runtime value not enforced
```

Template literal types are compile-time only — they don't validate runtime strings. Show: using Zod's `z.string().startsWith('on')` for runtime validation, a registry pattern where valid event names are tracked in a `Map`, and `satisfies EventName` to verify a string literal meets the template pattern at compile time.""",

"""**Debug Scenario:**
TypeScript `typeof` in a conditional type narrows to `never` unexpectedly:

```ts
type IsString<T> = T extends string ? 'yes' : 'no';

type Test1 = IsString<string>;  // 'yes' ✓
type Test2 = IsString<number>;  // 'no' ✓
type Test3 = IsString<string | number>; // 'yes' | 'no' ✓ (distributive)
type Test4 = IsString<never>;   // never — NOT 'no'!
```

When `T = never`, the conditional type short-circuits to `never` (distributing over an empty union produces an empty union = `never`). Show: wrapping in `[T] extends [string]` to prevent distribution (`[never] extends [string]` → `false` → `'no'`), the `IsNever<T>` helper, and common uses of this pattern (e.g., checking if a mapped type produced any members).""",

"""**Debug Scenario:**
A TypeScript generic class with default type parameters fails to infer when the default is used:

```ts
class ApiClient<TResponse = unknown, TError = Error> {
  async request(url: string): Promise<TResponse> { ... }
}

const client = new ApiClient<User>(); // TResponse=User, TError=Error (default)
const result = await client.request('/api/user');
// result: User ✓ — but:

// Can't partially apply type params in some contexts:
function makeClient<T>(): ApiClient<T> {
  return new ApiClient<T>(); // TError reverts to 'unknown' instead of 'Error'!
}
```

When explicitly providing type parameters, skipping middle parameters doesn't apply defaults — you must provide all or none. Show: using a factory function to apply defaults (`function makeClient<T, E = Error>(): ApiClient<T, E>`), the limitation of TypeScript's partial type arg application, and the `type-fest` library's `FixedLengthArray` pattern for working around this.""",

"""**Debug Scenario:**
TypeScript's `as const` doesn't make nested objects fully readonly in a `satisfies` expression:

```ts
const config = {
  server: { port: 3000, host: 'localhost' },
  features: ['auth', 'payments'],
} as const satisfies ServerConfig;

config.server.port = 4000; // Error: readonly ✓
config.features.push('analytics'); // Error: readonly ✓

// But:
const copy = { ...config }; // Mutable shallow copy!
copy.server.port = 4000; // No error — copy.server is not readonly!
```

`as const` makes the original binding readonly, but a spread copy creates a mutable shallow copy. Show: `structuredClone` creating a mutable deep copy (different semantics), `Object.freeze` for runtime immutability, and the `DeepReadonly<typeof config>` type to keep the spread copy typed as readonly (`const copy: DeepReadonly<typeof config> = { ...config }`).""",

"""**Debug Scenario:**
A developer uses `Parameters<typeof fn>` to type a wrapper function, but when `fn` is overloaded, the wrapper only accepts the parameters of the last overload:

```ts
function parse(input: string): number;
function parse(input: string, radix: number): number;
function parse(input: string, radix?: number): number { ... }

function safeParseWrapper(...args: Parameters<typeof parse>) {
  // args: [input: string, radix?: number] — only last overload!
  return parse(...args);
}

safeParseWrapper('42');         // OK
safeParseWrapper('42', 10);     // OK — both happen to work here
```

Show: the `OverloadUnion<typeof parse>` approach to unify all overload parameter sets, using function overloads on the wrapper itself (matching all overloads of `fn`), and when `Parameters<>` is safe to use (non-overloaded functions, or when you intentionally want only the last overload).""",

"""**Debug Scenario:**
A TypeScript file with `export {}` at the bottom breaks module augmentation in another file:

```ts
// global.d.ts (intended as ambient module augmentation)
declare global {
  interface Window {
    myPlugin: MyPlugin;
  }
}
export {}; // Makes this a module — required to use 'declare global'
```

```ts
// component.ts
window.myPlugin; // Works fine!
```

But adding `import { something } from 'nowhere'` to `global.d.ts` breaks it — it's now both a module AND has global augmentation, requiring the `/// <reference types="..." />` directive. Show: the correct structure for type augmentation files, the `declare global { }` requirement in module files (files with `import/export`), and `typeRoots` configuration for global type files.""",

"""**Debug Scenario:**
A TypeScript `Record<string, unknown>` causes issues when trying to iterate with `Object.entries`:

```ts
function processConfig(config: Record<string, unknown>) {
  for (const [key, value] of Object.entries(config)) {
    // value: unknown — need to narrow
    if (typeof value === 'string') {
      console.log(key + ': ' + value.toUpperCase()); // OK
    }
    if (typeof value === 'object' && value !== null) {
      processConfig(value); // Error: 'unknown' not assignable to Record<string, unknown>
    }
  }
}
```

After narrowing `value` to `object`, TypeScript still sees it as `object`, not `Record<string, unknown>`. Show: using `as Record<string, unknown>` cast after the `typeof` narrowing check, the `isRecord(v: unknown): v is Record<string, unknown>` type guard, and avoiding this pattern with discriminated unions or specific interfaces for known config shapes.""",

"""**Debug Scenario:**
TypeScript's `exactOptionalPropertyTypes` flag causes compilation errors in code that previously worked:

```ts
// tsconfig.json: "exactOptionalPropertyTypes": true

type Options = { debug?: boolean };

const opts1: Options = { debug: undefined }; // Error! With exactOptional, optional != undefined-assignable
const opts2: Options = {};                   // OK
const opts3: Options = { debug: true };      // OK

function setDebug(opts: Options, val: boolean | undefined) {
  opts.debug = val; // Error: 'undefined' not assignable to 'boolean'!
}
```

`exactOptionalPropertyTypes` means `debug?: boolean` = property may be absent, but NOT `debug: undefined`. Show: explicitly widening the type (`debug?: boolean | undefined`), using `delete opts.debug` to remove the property instead of assigning `undefined`, and the use case for `exactOptionalPropertyTypes` (stricter contracts — prevents accidental `undefined` assignments).""",

]
