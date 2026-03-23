"""
snippets/q_typescript.py — BATCH 5: 28 brand-new TypeScript questions
Zero overlap with batch1, batch2, batch3, or batch4 archives.
"""

Q_TYPESCRIPT = [

"""**Task (Code Generation):**
Implement a `Opaque<T, Brand>` type for preventing value misuse:

```ts
type UserId    = Opaque<string, 'UserId'>;
type ProductId = Opaque<string, 'ProductId'>;
type OrderId   = Opaque<number, 'OrderId'>;

function getUser(id: UserId): User { ... }
function getProduct(id: ProductId): Product { ... }

const userId:    UserId    = createId<UserId>('user-123');
const productId: ProductId = createId<ProductId>('prod-456');

getUser(productId);  // TypeScript Error: Argument of type 'ProductId' is not assignable to 'UserId'
getUser(userId);     // OK
```

Show: the `Opaque<T, Brand>` type using intersection with a brand type (`T & { readonly __brand: Brand }`), the `createId` factory that returns a branded type, `unwrap<T extends Opaque<...>>` to get the underlying value, and real-world benefits (prevents passing a userId where a productId is expected even though both are strings).""",

"""**Debug Scenario:**
A TypeScript function returns different types based on an overload, but the runtime behavior doesn't match:

```ts
function parse(input: string): number;
function parse(input: number): string;
function parse(input: any): any {
  return input; // Bug! Should convert, but just returns as-is
}

const result = parse('42'); // TypeScript thinks: number
console.log(typeof result); // 'string' at runtime — mismatch!
```

TypeScript trusts the implementation signature's return type annotation. The caller sees `number` but gets a `string`. Show: implementing the function body correctly, adding a `type: 'overload-mistake'` guard to detect mismatch, using a generic single-signature approach instead of overloads when the type relationship is simple, and runtime validation with Zod to catch the mismatch if it slips through.""",

"""**Task (Code Generation):**
Build a `DeepReadonly<T>` recursive type and `freeze` utility:

```ts
type Config = {
  api: { url: string; timeout: number };
  features: { darkMode: boolean; beta: string[] };
};

type ReadonlyConfig = DeepReadonly<Config>;
// ReadonlyConfig: {
//   readonly api: { readonly url: string; readonly timeout: number };
//   readonly features: { readonly darkMode: boolean; readonly beta: readonly string[] };
// }

const config = freeze<Config>({ api: { url: 'https://api.com', timeout: 5000 }, features: { darkMode: true, beta: [] } });
config.api.url = 'foo'; // TypeScript Error: Cannot assign to 'url' because it is a read-only property.
```

Show: the recursive `DeepReadonly<T>` type that handles objects, arrays, and primitives, the `freeze` function using `Object.freeze` recursively at runtime, and why `Object.freeze` is only shallow (the type system helps document the contract even when runtime enforcement is impractical for deep objects).""",

"""**Debug Scenario:**
A TypeScript enum is used for string comparison and produces unexpected behavior:

```ts
enum Status {
  Active = 'ACTIVE',
  Inactive = 'INACTIVE',
}

const statusFromApi = 'ACTIVE'; // string from API response
if (statusFromApi === Status.Active) {
  // Works! But...
}

// Bug: Comparing enum to string value:
const enumValue = Status.Active;
const statusKey = 'Active'; // key, not value
if (enumValue === statusKey) {
  // Always false — enum VALUE is 'ACTIVE', not 'Active'
}
```

Show: why TypeScript doesn't catch this comparison (both are strings at type level), using a type guard `(value: string): value is Status => Object.values(Status).includes(value as Status)`, the `const` assertion alternative (`const Status = { Active: 'ACTIVE' } as const; type Status = typeof Status[keyof typeof Status]`), and why union types of string literals are often preferable to string enums.""",

"""**Task (Code Generation):**
Implement a `createStateMachine<States, Events>` with TypeScript transitions:

```ts
const machine = createStateMachine({
  initial: 'idle' as const,
  states: {
    idle:     { on: { START: 'loading' } },
    loading:  { on: { SUCCESS: 'ready', ERROR: 'failed' } },
    ready:    { on: { RESET: 'idle', REFRESH: 'loading' } },
    failed:   { on: { RETRY: 'loading', RESET: 'idle' } },
  },
});

machine.send('START');    // OK: idle → loading
machine.send('SUCCESS');  // OK: loading → ready
machine.send('START');    // TypeScript Error: 'START' is not valid in state 'ready'
```

Show: the TypeScript type that computes valid events per state, the generic constraints, the `StateOf<typeof machine>` and `EventOf<typeof machine>` utility types, and a React hook `useStateMachine` that integrates the machine with React state.""",

"""**Debug Scenario:**
A TypeScript project uses path aliases (`@/components/Button`) but the aliases work in TypeScript (IDE, `tsc`) but fail at runtime in Jest:

```ts
// tsconfig.json paths:
{ "@/*": ["src/*"] }

// Jest test file:
import Button from '@/components/Button';
// Error: Cannot find module '@/components/Button'
```

TypeScript path aliases are compile-time only — they don't affect how Node.js resolves modules at runtime. Jest uses its own module resolver. Show: configuring `moduleNameMapper` in Jest config (`{ '@/(.*)': '<rootDir>/src/$1' }`), using `ts-jest` with `pathsToModuleNameMapper` helper that reads aliases from `tsconfig.json` automatically, and the Babel approach using `babel-plugin-module-resolver`.""",

"""**Task (Code Generation):**
Build a `EventEmitter<Events>` with strongly-typed events:

```ts
type ServerEvents = {
  connection: { clientId: string; ip: string };
  disconnect: { clientId: string; reason: string };
  message:    { clientId: string; data: unknown; timestamp: number };
  error:      { code: number; message: string };
};

const emitter = new TypedEventEmitter<ServerEvents>();

emitter.on('connection', ({ clientId, ip }) => {
  console.log(`Client ${clientId} connected from ${ip}`);
});

emitter.on('disconnect', ({ clientId, reason }) => { ... });

// TypeScript Error: 'data' is missing in message payload
emitter.emit('message', { clientId: '1', timestamp: Date.now() });
```

Show: the typed `on`, `off`, `emit`, and `once` methods, the TypeScript inference ensuring the payload type flows from the event name, and extending Node.js's `EventEmitter` vs building from scratch.""",

"""**Debug Scenario:**
A TypeScript generic function has an unexpected type widening:

```ts
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

const nums = [1, 2, 3];
const x = first(nums); // TypeScript infers: number | undefined ✓

const mixed = [1, 'two', true];
const y = first(mixed); // TypeScript infers: string | number | boolean | undefined ✓

// Bug scenario:
function processFirst<T extends string | number>(arr: T[]): T {
  return arr[0]!; // Non-null assertion — but what if array is empty?
}

processFirst(['hello']); // OK
processFirst([]);         // Runtime error: undefined, but TypeScript says string
```

Show: replacing `!` with an explicit check (`if (!arr[0]) throw new Error('Empty array')`), or returning `T | undefined` and letting the caller handle it, and the `[T, ...T[]]` non-empty array type to enforce at compile time that the array has at least one element.""",

"""**Task (Code Generation):**
Implement `ParseQueryString<S extends string>` as a pure type-level parser:

```ts
type Parsed = ParseQueryString<'name=Alice&age=30&tags=a,b,c'>;
// Result:
// {
//   name: 'Alice';
//   age: '30';
//   tags: 'a,b,c';
// }

type Params = ParseQueryString<typeof window.location.search>; // typed!
```

Show: the template literal type that splits on `&`, then splits each pair on `=`, builds an object from the key-value pairs using recursive mapped types, `infer` to extract keys and values, and a `ParseQueryStringValues<S>` variant that attempts to parse number and boolean values to their proper types.""",

"""**Debug Scenario:**
A TypeScript project uses `@ts-ignore` in 47 places. A new team member asks why, and explains that `@ts-expect-error` is safer. What's the difference and how to migrate?

`@ts-ignore` suppresses the NEXT LINE unconditionally — if the error goes away (e.g., library update fixes the type), the comment stays silently. `@ts-expect-error` REQUIRES an error on the next line — if no error exists, TypeScript reports an "Unused '@ts-expect-error' directive" error, making it self-cleaning.

Show: the ESLint rule `@typescript-eslint/prefer-ts-expect-error` that automatically flags `@ts-ignore` usages, a codemod to replace all `@ts-ignore` with `@ts-expect-error`, and the cases where `@ts-ignore` is still appropriate (e.g., in `.d.ts` declaration files where `@ts-expect-error` behavior differs).""",

"""**Task (Code Generation):**
Build a `Serializable<T>` type that validates at compile-time that a type can be safely JSON serialized:

```ts
type SafeToSerialize<T> =
  T extends undefined | Function | symbol ? never :
  T extends Date ? never :          // Dates serialize to strings, losing type
  T extends object ? { [K in keyof T]: SafeToSerialize<T[K]> } :
  T;

type IsSerializable<T> = T extends SafeToSerialize<T> ? true : false;

type A = IsSerializable<{ name: string; age: number }>;    // true
type B = IsSerializable<{ fn: () => void }>;               // false
type C = IsSerializable<{ date: Date }>;                    // false
type D = IsSerializable<{ nested: { id: number } }>;       // true
```

Show: the recursive conditional type, using it to constrain API response types (`serialize<T extends SafeToSerialize<T>>(data: T): string`), and the `Branded<T, 'Serialized'>` type for tracking which values have been validated.""",

"""**Debug Scenario:**
A TypeScript interface uses `readonly` arrays but the runtime code modifies them:

```ts
interface AppState {
  readonly users: readonly User[];
}

function addUser(state: AppState, user: User): AppState {
  (state.users as User[]).push(user); // TypeScript allows with cast!
  return state;
}
```

Type assertions (`as`) bypass TypeScript checks. The `readonly` modifier is erased at runtime — `push` succeeds. Show: the correct immutable update pattern (return a new array `[...state.users, user]` instead of mutating), why `readonly` is only a TypeScript compile-time check (not runtime enforcement), using `Object.freeze()` for actual runtime immutability, and a custom ESLint rule `@typescript-eslint/prefer-readonly` to catch function parameters that could be declared `readonly` but aren't.""",

"""**Task (Code Generation):**
Implement a `ReturnTypeDeep<T>` type that unwraps async functions:

```ts
type ReturnTypeDeep<T extends (...args: any) => any> =
  ReturnType<T> extends Promise<infer Inner> ? Inner : ReturnType<T>;

async function fetchUser(id: string): Promise<User> { ... }
function getCount(): number { ... }
async function getItems(): Promise<Item[]> { ... }

type A = ReturnTypeDeep<typeof fetchUser>; // User (not Promise<User>)
type B = ReturnTypeDeep<typeof getCount>;  // number
type C = ReturnTypeDeep<typeof getItems>; // Item[]
```

Extend this to also handle `AsyncGenerator<T>`:

```ts
async function* streamData(): AsyncGenerator<Chunk> { ... }
type D = ReturnTypeDeep<typeof streamData>; // Chunk
```

Show: extending `ReturnTypeDeep` to unwrap `AsyncGenerator<T>`, `Generator<T>`, and nested Promises (`Promise<Promise<T>>`).""",

"""**Debug Scenario:**
A TypeScript class uses a decorator that modifies the class constructor, but after compilation the decorator's mutations aren't reflected in the TypeScript types:

```ts
@withLogger  // adds `logger: Logger` property at runtime
class UserService {
  getUser(id: string) {
    this.logger.log(`Getting user ${id}`); // TypeScript Error: Property 'logger' does not exist
  }
}
```

Decorators in TypeScript stage 3 can't automatically augment the class type. Show: declaring the `logger` property on the class with a type assertion (`declare logger: Logger`), using module augmentation to add `logger` to the class interface, the newer `using` keyword (TypeScript 5.2) as an alternative for resource management patterns, and why class decorators in TypeScript must use the `declare` workaround for added properties until the ECMAScript decorator spec finalizes.""",

"""**Task (Code Generation):**
Build a `createValidator<T>` that generates runtime validators from TypeScript types using Zod:

```ts
const UserValidator = createValidator<User>(); // generates Zod schema at compile time
const parsed = UserValidator.parse(apiResponse);
// parsed is typed as User, with runtime validation

// If TypeScript type changes, the validator automatically updates:
type User = { id: number; email: string; role: 'admin' | 'user' };
// No need to manually update a Zod schema!
```

Show: using `ts-to-zod` or a custom TypeScript transformer plugin that reads type definitions and generates Zod schemas at compile time, the transformer configuration in `tsconfig.json`, and why this approach (type-first) differs from Zod's schema-first approach (`z.infer<typeof UserSchema>`).""",

"""**Debug Scenario:**
A TypeScript discriminated union with exhaustiveness checking fails to catch a missing case:

```ts
type Shape = { kind: 'circle'; radius: number } | { kind: 'square'; side: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case 'circle': return Math.PI * shape.radius ** 2;
    case 'square': return shape.side ** 2;
    // if 'triangle' is added to Shape, no TypeScript error here!
  }
  // implicitly returns undefined — TypeScript infers: number | undefined
}
```

Adding `'triangle'` to `Shape` should cause a compile error in `area`. Show: the `never` exhaustiveness check pattern:

```ts
default:
  const _exhaustive: never = shape; // Error when new Shape variant added
  throw new Error(`Unhandled: ${_exhaustive}`);
```

And a utility type `assertNever(x: never): never` that provides the same guarantee with a better error message.""",

"""**Task (Code Generation):**
Implement a `createHttpClient<Routes>` with type-safe URLs and request/response types:

```ts
type ApiRoutes = {
  'GET /users':              { response: User[]; query: { role?: string } };
  'GET /users/:id':          { response: User; params: { id: string } };
  'POST /users':             { response: User; body: CreateUserDto };
  'PUT /users/:id':          { response: User; params: { id: string }; body: UpdateUserDto };
  'DELETE /users/:id':       { response: void; params: { id: string } };
};

const client = createHttpClient<ApiRoutes>({ baseUrl: 'https://api.example.com' });

// Fully typed:
const users = await client.get('/users', { query: { role: 'admin' } });
// users: User[]

const user = await client.post('/users', { body: { name: 'Alice', email: '...' } });
// user: User
```

Show: TypeScript inference of params, query, body, and response types from the route string, URL param interpolation, and a Zod-validated response deserializer.""",

"""**Debug Scenario:**
A TypeScript type guard is not narrowing correctly inside a callback:

```ts
function isUser(obj: unknown): obj is User {
  return typeof obj === 'object' && obj !== null && 'id' in obj;
}

const items: unknown[] = fetchData();
items.filter(isUser).forEach(item => {
  console.log(item.id); // TypeScript Error: 'id' does not exist on 'unknown'
});
```

`Array.filter` with a type guard SHOULD narrow the type of the array, but the TypeScript inference for `filter` requires that the type guard be used as a predicate in the generic signature.

Show: why this failure occurs in older TypeScript versions (the `filter` overload without generic inference), the corrected pattern for TypeScript 5.5+ which has improved `filter` narrowing, and the explicit type assertion workaround `items.filter(isUser) as User[]` for older TypeScript.""",

"""**Task (Code Generation):**
Build a `FormSchema` type that derives TypeScript types from an HTML form structure:

```ts
const loginForm = defineForm({
  fields: {
    email:    { type: 'email',    required: true  },
    password: { type: 'password', required: true, minLength: 8 },
    remember: { type: 'checkbox', required: false },
  },
});

type LoginFormData = InferFormData<typeof loginForm>;
// { email: string; password: string; remember: boolean | undefined }

const result: LoginFormData = loginForm.parse(formEvent.target);
// Runtime validation + type narrowing in one step
```

Show: the `defineForm` factory, `InferFormData` mapped type that derives field types from `type` strings (`email | text | password → string`, `checkbox → boolean`, `number → number`), required fields (always present) vs optional (union with undefined), and runtime parsing from `FormData`.""",

"""**Debug Scenario:**
A TypeScript project's `tsc --build` produces incorrect output after renaming a file. Old compiled files persist in the `dist/` directory and are imported by other modules:

```
src/helpers.ts  → renamed to src/utils.ts
dist/helpers.js → still exists! (orphan file)
dist/utils.js   → new file
```

`tsc` doesn't clean deleted source files from `dist/`. Any code that imports `../dist/helpers.js` directly still works but uses old code. Show: adding a `prebuild` script that runs `rimraf dist` before `tsc`, configuring `tsconfig.json` with `"noEmitOnError": true` to prevent partial builds, using `tsc --build --clean` (project references only), and `ts-node` / `tsx` for running TypeScript directly without a dist directory.""",

"""**Task (Code Generation):**
Implement `Flatten<T>` and `DeepFlatten<T>` types for nested array types:

```ts
type A = Flatten<number[][]>;     // number[]
type B = Flatten<string[][][]>;   // string[][]
type C = DeepFlatten<number[][][]>;  // number[]
type D = DeepFlatten<Array<Array<Array<{ id: number }>>>>;  // { id: number }[]

function flatten<T>(arr: T[][]): T[] { return arr.flat(); }
function deepFlatten<T>(arr: DeepArray<T>): T[] { return arr.flat(Infinity) as T[]; }

type DeepArray<T> = Array<T | DeepArray<T>>;
```

Show: `Flatten<T>` using conditional type (`T extends Array<infer U> ? U extends Array<infer V> ? ...`), `DeepFlatten<T>` using recursive conditional type, the `DeepArray<T>` recursive type alias, and TypeScript's recursion depth limit and how to work around it with `[...T[]]` spreads.""",

"""**Debug Scenario:**
A TypeScript app uses namespace imports and hits circular dependency issues:

```ts
// user.ts:
import * as Order from './order';
export type User = { orders: Order.Order[] };

// order.ts:
import * as User from './user';
export type Order = { user: User.User; items: Item[] };
```

Both modules import each other at the type level. TypeScript resolves type-only circular dependencies, but the JavaScript module runtime may evaluate them in the wrong order if they have value exports too.

Show: using `import type` for type-only imports (zero cost at runtime, no circular initialization), a shared `types.ts` file that both modules import from (breaking the cycle), and the `@typescript-eslint/no-import-type-side-effects` rule.""",

"""**Task (Code Generation):**
Build a `createAsyncQueue<T>` with TypeScript generics and priority support:

```ts
const queue = createAsyncQueue<ProcessingJob>({
  concurrency: 3,
  timeout: 30_000,
  onError: (job, error) => logger.error({ job, error }),
});

// Job with priority (lower number = higher priority):
queue.enqueue({ id: '1', data: heavyTask, priority: 1 });
queue.enqueue({ id: '2', data: lightTask, priority: 10 });

// TypeScript knows the job type:
queue.onComplete((job: ProcessingJob) => { ... });
queue.stats(); // { running: 2, pending: 8, completed: 143, failed: 2 }
```

Show: the generic `T` constraint, the priority queue implementation (sorted insert using binary search), concurrency semaphore, timeout using `Promise.race`, and the `stats()` return type inferred from the internal counters.""",

"""**Debug Scenario:**
A TypeScript function has a conditional return type but `strictFunctionTypes` causes unexpected errors:

```ts
function getValue<T extends boolean>(flag: T): T extends true ? string : number {
  return flag ? 'hello' : 42; // TypeScript Error: Type 'string | number' is not assignable to T extends true ? string : number
}
```

TypeScript can't verify the relationship between the runtime `flag` value and the conditional type — it sees the return as `string | number`, not the conditional. Show: using function overloads as the idiomatic solution, a type assertion as a temporary fix (`return (flag ? 'hello' : 42) as any`), and why conditional return types with generic arguments require overloads or type assertions (TypeScript doesn't "execute" conditional types based on runtime values).""",

"""**Task (Code Generation):**
Implement a `NetworkRequest<T>` discriminated union for exhaustive response handling:

```ts
type NetworkRequest<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T; timestamp: number }
  | { status: 'error'; error: Error; retryCount: number };

function renderUser(request: NetworkRequest<User>): JSX.Element {
  switch (request.status) {
    case 'idle':    return <Placeholder />;
    case 'loading': return <Spinner />;
    case 'success': return <UserCard user={request.data} />;
    case 'error':   return <ErrorMessage error={request.error} onRetry={...} />;
  }
}
```

Show: TypeScript's exhaustiveness check enforcing all cases are handled, a `createNetworkRequest<T>` factory, transition functions (`toLoading`, `toSuccess`, `toError`) that enforce valid state transitions, and a React hook `useNetworkRequest<T>` that wraps `fetch` and returns the discriminated union.""",

"""**Debug Scenario:**
A TypeScript class method `bind`s `this` but loses TypeScript type inference:

```ts
class EventHandler {
  private handler = 'click-handler';
  
  handleClick(event: MouseEvent): void {
    console.log(this.handler, event.type);
  }
}

const h = new EventHandler();
document.addEventListener('click', h.handleClick.bind(h));
// Works, but TypeScript sometimes infers bind(h) as Function, losing the type
```

`.bind()` returns `Function` in some older TypeScript internal typings (< TS 3.2). Show: using an arrow function property instead (`handleClick = (event: MouseEvent) => { ... }`) which captures `this` at class construction, the `Parameters<typeof h.handleClick>` utility when you need the argument types, and ESLint `@typescript-eslint/unbound-method` that warns about unbound method references.""",

"""**Task (Code Generation):**
Build a `createI18nType<Translations>` that generates fully-typed translation accessor:

```ts
const translations = {
  en: {
    greeting: 'Hello, {{name}}!',
    'errors.notFound': 'Page not found',
    'items.count': '{{count}} items',
  },
} as const;

const { t } = createI18nType(translations, 'en');

t('greeting', { name: 'Alice' });        // OK: 'Hello, Alice!'
t('errors.notFound');                    // OK: no variables needed
t('items.count', { count: 5 });         // OK: requires 'count'
t('greeting');                           // TypeScript Error: missing 'name'
t('unknown.key');                        // TypeScript Error: not a valid key
```

Show: extracting variable names from the string literal type using `infer` and template literals, deriving `Variables<S>` type from the translation string, and the `t` function signature that requires `Variables` to be passed when they exist.""",

"""**Task (Code Generation):**
Implement a `createTypedRouter<Routes>` for Express with full request/response type safety:

```ts
type AppRoutes = {
  'GET /users':           { query: { limit?: number }; response: User[] };
  'GET /users/:id':       { params: { id: string }; response: User };
  'POST /users':          { body: CreateUserInput; response: User };
  'DELETE /users/:id':    { params: { id: string }; response: { deleted: boolean } };
};

const router = createTypedRouter<AppRoutes>(express.Router());

router.get('/users', async (req, res) => {
  const limit = req.query.limit; // TypeScript: number | undefined
  const users = await getUsers(limit);
  res.json(users); // TypeScript validates: User[]
});

router.post('/users', async (req, res) => {
  const input = req.body; // TypeScript: CreateUserInput
  const user = await createUser(input);
  res.status(201).json(user); // TypeScript: User
});
```

Show: the TypeScript overloads that match the method + path literal to the route definition, typed request and response objects, and Zod middleware for runtime validation of `params`, `query`, and `body` against schemas derived from the TypeScript types.""",

]
