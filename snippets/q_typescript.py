"""
snippets/q_typescript.py - 28 TypeScript Advanced questions
"""

Q_TYPESCRIPT = [

"""**Context:**
We have a generic fetchResource function. TypeScript correctly infers the return type in most cases but fails in a specific composition.

**Code:**
```ts
async function fetchResource<T>(url: string): Promise<T> {
  const res = await fetch(url);
  return res.json() as T;
}

// works:
const user = await fetchResource<User>('/api/user');

// fails to infer -- T becomes unknown:
const pipeline = (url: string) => fetchResource(url);
```

**Observed Issue:**
When wrapped in another function, TypeScript loses the generic -- T is inferred as unknown instead of being propagated.

**Specific Ask:**
How do you write a wrapper function that preserves the generic of the inner function, allowing callers of pipeline<User>(url) to get the correct inferred type? Is there a way to make pipeline itself generic in a way TypeScript can infer from the call site?""",

"""**Context:**
Our design system components accept a polymorphic as prop to render as different HTML elements.

**Code:**
```ts
type PolymorphicProps<C extends React.ElementType> = {
  as?: C;
} & React.ComponentPropsWithoutRef<C>;
```

**Observed Issue:**
When we compose PolymorphicProps with our own props via intersection, TypeScript fails to narrow the allowed HTML attributes correctly. Passing href to a component renders as a div, and TypeScript doesn't complain.

**Specific Ask:**
What's the correct pattern for a fully type-safe polymorphic component where the allowed HTML props are determined by the as prop value? How do major libraries (Radix, Ariakit) implement this without losing type safety, and does it work with generic forwarded refs?""",

"""**Context:**
We have an API response handler that uses a discriminated union.

**Code:**
```ts
type ApiResponse<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };

function handle<T>(res: ApiResponse<T>) {
  if (res.status === 'success') {
    console.log(res.data); // TS: 'data' does not exist on type 'ApiResponse<T>'
  }
}
```

**Observed Issue:**
TypeScript fails to narrow the discriminated union inside a generic function even though the narrowing works perfectly in a non-generic context.

**Specific Ask:**
Why does TypeScript fail to narrow discriminated unions inside generic functions, and is this a fundamental limitation or a known bug? What's the workaround -- assertion functions, type predicates, or restructuring the generic? Is this fixed in newer TypeScript versions?""",

"""**Context:**
We wrote a recursive conditional type to unwrap nested Promises.

**Code:**
```ts
type UnwrapPromise<T> = T extends Promise<infer U> ? UnwrapPromise<U> : T;
type Unwrapped = UnwrapPromise<Promise<Promise<string>>>; // should be 'string'
```

**Observed Issue:**
For simple cases it works, but when used inside a mapped type or combined with another conditional type, TypeScript returns the error: "Type instantiation is excessively deep and possibly infinite."

**Specific Ask:**
What's the recursion depth limit for TypeScript conditional types? What's the recommended pattern for recursive types that need to work in production code without hitting the depth error? Does the Awaited<T> built-in utility perform better than a custom recursive type?""",

"""**Context:**
We have a large form type and need to extract all keys whose value type is string for a utility function.

**Code:**
```ts
type StringKeys<T> = {
  [K in keyof T]: T[K] extends string ? K : never;
}[keyof T];

type UserStringFields = StringKeys<UserForm>; // expected: 'firstName' | 'lastName' | 'email'
```

**Observed Issue:**
When T has optional fields (key?: string), the mapped type distributes never for those fields because T[K] becomes string | undefined which doesn't extend string.

**Specific Ask:**
How do you write a conditional type that handles optional properties correctly -- where key?: string should still be included in StringKeys? Is NonNullable<T[K]> the right tool, or does this cause other issues with the type distribution?""",

"""**Context:**
We're using template literal types to generate strongly-typed event names for our analytics system.

**Code:**
```ts
type EventName = `${Screen}_${Action}`;
type Screen = 'dashboard' | 'report' | 'settings';
type Action = 'viewed' | 'clicked' | 'submitted';
// produces: 'dashboard_viewed' | 'dashboard_clicked' | ... (9 combinations)
```

**Observed Issue:**
When Screen and Action union members grow large (~20 each), TypeScript starts taking 10+ seconds to type-check files that use EventName due to the combinatorial explosion (400+ combinations).

**Specific Ask:**
At what union size does template literal type distribution become a performance problem? What's the recommended alternative for large event name schemas -- a plain string enum, a const object, or a Zod schema? Is there a way to keep template literal types without paying the full combinatorial type-checking cost?""",

"""**Context:**
We have a callback-based API where covariance/contravariance causes unexpected type errors.

**Code:**
```ts
type Handler<T> = (event: T) => void;

const mouseHandler: Handler<MouseEvent> = (e) => console.log(e.clientX);
const eventHandler: Handler<Event> = mouseHandler; // Error: MouseEvent is not assignable to Event
```

**Observed Issue:**
We expected a MouseEvent handler to be assignable to an Event handler (since MouseEvent extends Event), but TypeScript rejects it. The function parameter position is contravariant.

**Specific Ask:**
Explain why function parameters are contravariant in TypeScript and what this means practically for callback types. When building an event system where handlers need to be stored in a generic Map<string, Handler<Event>>, what's the correct type design that satisfies TypeScript without using any?""",

"""**Context:**
We have a set of overloaded parse functions that TypeScript fails to infer correctly when called from a generic context.

**Code:**
```ts
function parse(input: string): ParsedString;
function parse(input: number): ParsedNumber;
function parse(input: unknown): unknown { ... }

function wrap<T extends string | number>(val: T): ReturnType<typeof parse> {
  return parse(val); // Error: no overload matches T
}
```

**Observed Issue:**
TypeScript can't match T extends string | number to either overload because T is a type variable, not a concrete type.

**Specific Ask:**
Why can't TypeScript match type variables against function overloads? What's the idiomatic fix -- conditional return types on wrap, separate overloads for wrap itself, or restructuring parse to use a conditional type instead of overloads?""",

"""**Context:**
We have a utility type that composes Partial and Required to create a "required-core, optional-extras" object shape.

**Code:**
```ts
type CoreRequired<T, K extends keyof T> = Required<Pick<T, K>> & Partial<Omit<T, K>>;

type Config = CoreRequired<DashboardConfig, 'apiUrl' | 'userId'>;
```

**Observed Issue:**
When passing a Config object to a function expecting DashboardConfig, TypeScript complains even though Config should be assignable -- it has all required fields plus optionals.

**Specific Ask:**
Does intersection of Required<Pick<...>> & Partial<Omit<...>> produce a type that TypeScript considers structurally assignable to the original type? Or does the intersection create a type that looks correct but has different structural semantics? Is there a simpler built-in utility type composition that achieves this?""",

"""**Context:**
We need to augment a third-party Express-like framework's Request type to add our custom session property without modifying its source.

**Code:**
```ts
// types/express.d.ts
declare module 'express' {
  interface Request {
    session: UserSession;
  }
}
```

**Observed Issue:**
The augmentation works in some files but not all. In files where we import from 'express' indirectly (through a wrapper module), the session property isn't recognized.

**Specific Ask:**
What are the rules for module augmentation scope in TypeScript? Why would an augmentation apply in some files but not others? Does the .d.ts file need to be included in tsconfig.json's include array, or referenced via triple-slash directives in every file?""",

"""**Context:**
We want to create a type that extracts only the async function properties from an interface.

**Code:**
```ts
type AsyncMethods<T> = {
  [K in keyof T]: T[K] extends (...args: any[]) => Promise<any> ? K : never;
}[keyof T];

type RepoAsync = AsyncMethods<UserRepository>; // should be only the async method names
```

**Observed Issue:**
Methods that return Promise<void> are excluded because Promise<void> doesn't extend Promise<any> in TypeScript's structural check.

**Specific Ask:**
Why doesn't Promise<void> extend Promise<any> in TypeScript's conditional type check? Should the constraint be (...args: any[]) => Promise<unknown> instead? And does this intersect correctly with methods that have overloads?""",

"""**Context:**
We need a type-safe async function wrapper that preserves the exact return type of any async function it wraps.

**Code:**
```ts
async function withRetry<T>(fn: () => Promise<T>, retries: number): Promise<T> {
  // ... retry logic
}

const result = await withRetry(() => fetchUser(id), 3);
// result should be inferred as User, not Promise<User>
```

**Observed Issue:**
When the passed function returns Promise<User>, the inferred T is User (correct). But when the function has a conditional return type, T is inferred as never.

**Specific Ask:**
How do you write a higher-order async function that correctly infers T from a function with a conditional return type? Is Awaited<ReturnType<F>> the right approach for generic function wrappers? What are the limitations of this approach?""",

"""**Context:**
We're building a component prop type that extracts props from an existing HTML element, overriding some.

**Code:**
```ts
type ButtonProps = Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, 'onClick'> & {
  onClick: (event: MouseEvent, metadata: TrackingData) => void;
};
```

**Observed Issue:**
The Omit + intersection approach loses the correct JSX autocomplete for standard button attributes. TypeScript no longer suggests aria-* or data-* attributes.

**Specific Ask:**
Is there a better pattern than Omit for extending HTML element props while overriding specific ones? Does React.ComponentPropsWithoutRef<'button'> behave differently from React.ButtonHTMLAttributes? How do design system libraries like Radix preserve full HTML attribute suggestions while adding their own?""",

"""**Context:**
We want to create "branded" or "opaque" types for user IDs to prevent mixing up different ID types.

**Code:**
```ts
type UserId = string & { readonly __brand: 'UserId' };
type ReportId = string & { readonly __brand: 'ReportId' };

function getUser(id: UserId) { ... }
getUser('abc' as UserId); // works but requires cast everywhere
```

**Observed Issue:**
Creating branded types requires casting everywhere with as UserId, which is error-prone. Also, branded types don't survive JSON serialization/deserialization.

**Specific Ask:**
What's the idiomatic TypeScript branded type pattern that minimizes the ergonomic overhead of casting? Is there a way to have TypeScript verify branding at boundaries (API responses, form inputs) without a runtime cost? How do zod schemas help -- does z.string().brand<'UserId'>() solve the serialization problem?""",

"""**Context:**
We use const assertions throughout our codebase to create narrowly-typed config objects.

**Code:**
```ts
const ROUTES = {
  dashboard: '/dashboard',
  reports: '/reports',
} as const;

type RoutePath = typeof ROUTES[keyof typeof ROUTES]; // '/dashboard' | '/reports'
```

**Observed Issue:**
When the const object is imported from a module and used in another module's type, the narrow literal types are sometimes widened back to string. This breaks the discriminated union based on route paths.

**Specific Ask:**
What causes TypeScript to widen literal types after const assertion when values cross module boundaries? Is there a specific re-export pattern that triggers widening? And what's the difference between as const and satisfies for preserving narrow types?""",

"""**Context:**
We have an object where we want TypeScript to both infer the type AND validate it against an interface without widening.

**Code:**
```ts
const config = {
  theme: 'dark',
  locale: 'en-US',
  features: { beta: true },
}; // inferred as { theme: string; locale: string; features: { beta: boolean } }
```

**Observed Issue:**
Using `as const` narrows too aggressively (everything becomes readonly literals). Using a type annotation widens the values. We want to validate structure without losing narrowed inferences on the values.

**Specific Ask:**
Is the satisfies operator (TypeScript 4.9+) the correct tool here? Does config satisfies DashboardConfig preserve narrow literal types while validating structure? What are the cases where satisfies falls short and you still need as const + type annotation?""",

"""**Context:**
We're using TypeScript 5's NoInfer utility to prevent TypeScript from inferring a type parameter from a specific argument.

**Code:**
```ts
function createSlice<T>(initial: T, handlers: Record<string, (s: NoInfer<T>) => T>) { ... }
```

**Observed Issue:**
Without NoInfer, TypeScript infers T from both initial and the handler signatures, sometimes inferring a wider type from a handler's cast. With NoInfer, we're seeing unexpected "type X is not assignable to NoInfer<T>" errors in handlers.

**Specific Ask:**
How does TypeScript 5's NoInfer<T> work -- does it create a new opaque wrapper type at the type level? What are the common pitfalls of NoInfer in handler patterns? Is this the right tool, or should we constrain the handlers using a separate generic bounded by T?""",

"""**Context:**
We have a function that accepts a tuple of functions and returns a tuple of their return types.

**Code:**
```ts
function runAll<T extends ((...args: any[]) => any)[]>(
  fns: [...T]
): { [K in keyof T]: ReturnType<T[K]> } {
  return fns.map(fn => fn()) as any;
}
```

**Observed Issue:**
The return type is correctly inferred as a tuple for simple cases. But when fns contains async functions, the return type is Promise<X>[] instead of [Promise<A>, Promise<B>].

**Specific Ask:**
Why does TypeScript lose tuple structure when mapping over variadic tuple types with ReturnType? Is there a way to make the mapped type preserve tuple positional types instead of widening to an array? Does Awaited<ReturnType<T[K]>> work correctly across variadic positions?""",

"""**Context:**
We have a type predicate function that narrows inside an if-block but TypeScript doesn't narrow in a filter call.

**Code:**
```ts
function isUser(item: User | null): item is User {
  return item !== null;
}

const items: (User | null)[] = getItems();
const users = items.filter(isUser); // TypeScript infers User[] -- correct
const firstUser = users.find(u => u.id === targetId); // correct
```

**Observed Issue:**
When the type predicate is used inside a more complex conditional with generics, TypeScript stops narrowing and the narrowed type reverts to the union.

**Specific Ask:**
Under what conditions does TypeScript's type predicate narrowing break down? Is there a known limitation with type predicates inside generic functions or higher-order combinators? Is the asserts keyword an alternative and what are the differences?""",

"""**Context:**
We have an abstract base class that dashboard panels extend. We need TypeScript to enforce that all subclasses implement a specific static factory method.

**Code:**
```ts
abstract class DashboardPanel {
  abstract render(): React.ReactNode;
  // How to enforce: static create(config: PanelConfig): DashboardPanel
}
```

**Observed Issue:**
TypeScript doesn't allow abstract static methods. Our panels are registered in a factory and instantiated by type, so we need a compile-time guarantee that each subclass has a static create method.

**Specific Ask:**
What's the TypeScript pattern to enforce static methods on subclasses? Can a generic type constraint enforce that a class constructor has a specific static method signature? Or is the solution an interface + constructor type (new (...args: any[]) => T) approach?""",

"""**Context:**
We have a module with several types exported from a namespace, and a global utility namespace that's conflicting with a local import.

**Code:**
```ts
import * as Utils from './utils';
// Later:
namespace Utils { // Error: duplicate identifier (merged? or error?)
  export function localHelper() {}
}
```

**Observed Issue:**
TypeScript treats the imported binding and the local namespace declaration as a conflict in some configurations but merges them in others. The behavior changes with isolatedModules.

**Specific Ask:**
When does TypeScript merge a namespace with an import vs. treat them as a conflict? How does isolatedModules change namespace declaration merging? What's the modern TypeScript recommendation -- avoid namespaces entirely in favor of ES modules, or are there valid use cases?""",

"""**Context:**
We use TypeScript path aliases in tsconfig.json for cleaner imports (@/components, @/lib). These work in the TypeScript compiler but break in Jest and sometimes in production builds.

**Code:**
```json
// tsconfig.json
{ "compilerOptions": { "paths": { "@/*": ["./src/*"] } } }
```

**Observed Issue:**
TypeScript path aliases are a compile-time feature only. Jest uses Node.js module resolution which doesn't read tsconfig paths. Production builds that use webpack work fine but esbuild-based tools ignore paths.

**Specific Ask:**
What's the correct layered approach to make TypeScript path aliases work across tsc, Jest, webpack, esbuild, and Vitest without maintaining the same aliases in 4 different config files? Is there a single source-of-truth approach with tooling-specific adapters?""",

"""**Context:**
We're migrating a large JavaScript codebase to TypeScript and enabling strict mode incrementally. We start with "strict": false and enable flags one at a time.

**Observed Issue:**
Enabling strictNullChecks causes 2,000+ type errors scattered across the codebase. Most are missing null checks on values that were always non-null in practice, but TypeScript can't prove it.

**Specific Ask:**
What's the most pragmatic incremental strategy for enabling strictNullChecks in a large codebase? Is the // @ts-expect-error approach to suppress errors temporarily better than as NonNullable<T> casts? How do you prioritize which files to fix first to maximize safety gains with minimum churn?""",

"""**Context:**
We maintain an internal npm package and need to author its .d.ts declaration files correctly. The package has ESM and CJS builds with different entry points.

**Code:**
```json
// package.json
{
  "exports": {
    ".": { "import": "./dist/esm/index.js", "require": "./dist/cjs/index.js" }
  },
  "types": "./dist/types/index.d.ts"
}
```

**Observed Issue:**
Consumers using moduleResolution: "bundler" pick up types correctly, but those using "node16" or "nodenext" get module not found errors when importing from sub-paths like @company/pkg/utils.

**Specific Ask:**
How do you correctly structure package.json exports and tsconfig for a dual ESM+CJS package that supports all TypeScript moduleResolution modes? Do you need separate .d.ts files for each export entry, and what's the typesVersions field for?""",

"""**Context:**
We enabled exactOptionalPropertyTypes in tsconfig after upgrading to TypeScript 4.9. Build broke with 400+ new errors.

**Code:**
```ts
type Config = { timeout?: number };
const config: Config = { timeout: undefined }; // Error with exactOptionalPropertyTypes
```

**Observed Issue:**
With exactOptionalPropertyTypes, { timeout: undefined } is no longer assignable to { timeout?: number } because optional means "may be absent" not "may be undefined". Our codebase frequently sets optional props to undefined explicitly.

**Specific Ask:**
What's the semantic difference between key?: T and key?: T | undefined with exactOptionalPropertyTypes enabled? Is there a codemod or ESLint rule to automatically fix the explicit-undefined-on-optional pattern? And is this flag worth the migration pain for a large codebase?""",

"""**Context:**
We're importing types from a third-party library in our component files. The linter flags that we should use type-only imports.

**Code:**
```ts
import { User, fetchUser } from '@company/api';
// ESLint: 'User' is a type and should be imported using 'import type'
```

**Observed Issue:**
We have hundreds of import statements that mix value and type imports. Splitting them into import type { User } and import { fetchUser } is tedious. We need to understand the actual runtime impact.

**Specific Ask:**
What's the runtime and bundle impact of importing types as values (not using import type)? Does TypeScript erase them at compile time anyway, making the lint rule cosmetic? Or are there cases where not using import type causes actual bundle bloat -- e.g., with bundlers that don't tree-shake type-only imports?""",


"""**Context:**
We need to extract the element type from an array type using the infer keyword inside a conditional type.

**Code:**
```ts
type ElementOf<T> = T extends (infer U)[] ? U : never;
type Str = ElementOf<string[]>; // string
type Num = ElementOf<number[]>; // number
```

**Observed Issue:**
The basic pattern works. But when we try to extract the element type from a nested Promise<Array<T>>, combining two infer keywords causes TypeScript to infer never.

**Code:**
```ts
type AsyncArrayElement<T> =
  T extends Promise<infer A>
    ? A extends (infer U)[]
      ? U
      : never
    : never;

type Test = AsyncArrayElement<Promise<User[]>>; // should be User, gets never
```

**Specific Ask:**
Why does chaining two separate conditional types with infer produce never here? Is there a single conditional type using both infer positions simultaneously (T extends Promise<(infer U)[]>) that works? And what's the difference between infer in a union-distributed context vs. a simple structural position?""",

"""**Context:**
We need to merge a class implementation with additional methods declared in an interface -- the classic declaration merging pattern for extending third-party classes.

**Code:**
```ts
class EventEmitter {
  on(event: string, handler: () => void) { ... }
}

// Attempt to add methods via declaration merging:
interface EventEmitter {
  once(event: string, handler: () => void): void;
}
```

**Observed Issue:**
TypeScript allows this pattern (class + interface declaration merging), but the runtime implementation of once is missing. The type says it exists but calling it throws at runtime.

**Specific Ask:**
What is class + interface declaration merging in TypeScript -- does it merge only types or also implementations? What's the correct pattern to both declare and implement additional methods on a class that already exists (possibly from a third-party)? Is module augmentation with prototype assignment the runtime complement to declaration merging?""",

]
