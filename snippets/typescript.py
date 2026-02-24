"""
snippets/typescript.py — Advanced TypeScript snippets for question injection.
"""

TYPESCRIPT_SNIPPETS = [
    # 1. Conditional type with infer
    """\
type UnwrapPromise<T> = T extends Promise<infer U> ? UnwrapPromise<U> : T;

type A = UnwrapPromise<Promise<Promise<string>>>;  // string — works
type B = UnwrapPromise<string[]>;                  // string[] — works

// But:
type ApiReturn<T extends (...args: any) => any> =
  UnwrapPromise<ReturnType<T>>;

// Error: Type instantiation is excessively deep and possibly infinite.
type C = ApiReturn<typeof fetchNestedResource>;""",

    # 2. Discriminated union narrowing failure
    """\
type ApiResponse<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: string }
  | { status: 'loading' };

function handleResponse<T>(res: ApiResponse<T>) {
  if (res.status === 'success') {
    console.log(res.data); // ✅
  }
  // But when passed through a generic handler:
  const process = <T>(r: ApiResponse<T>) => {
    const isSuccess = r.status === 'success';
    if (isSuccess) {
      console.log(r.data); // ❌ Property 'data' does not exist
    }
  };
}""",

    # 3. Mapped type with template literals
    """\
type EventMap = {
  click: MouseEvent;
  keydown: KeyboardEvent;
  resize: UIEvent;
};

type EventHandlers = {
  [K in keyof EventMap as `on${Capitalize<K>}`]: (event: EventMap[K]) => void;
};
// Produces: { onClick: (e: MouseEvent) => void; onKeydown: ...; onResize: ... }

// But extending this with optional:
type PartialHandlers = Partial<EventHandlers>;
// Now component prop types blow up — conditional spreading breaks inference""",

    # 4. Deep readonly
    """\
type DeepReadonly<T> = T extends (infer U)[]
  ? ReadonlyArray<DeepReadonly<U>>
  : T extends object
  ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
  : T;

type Config = DeepReadonly<{
  api: { baseUrl: string; timeout: number };
  features: { darkMode: boolean; beta: string[] };
}>;

// Problem: when passing Config into a function expecting Readonly<{ api: { baseUrl: string } }>
// TS fails to unify the nested readonly wrappers""",

    # 5. Generic constraint inference failure
    """\
function createStore<S, A extends { type: string }>(
  reducer: (state: S, action: A) => S,
  initialState: S
) {
  let state = initialState;
  return {
    dispatch: (action: A) => { state = reducer(state, action); },
    getState: () => state,
  };
}

// This fails to infer A from the reducer literal:
const store = createStore(
  (state: { count: number }, action) => { // action is `never` inferred
    if (action.type === 'INC') return { count: state.count + 1 };
    return state;
  },
  { count: 0 }
);""",

    # 6. Overloaded function with generics
    """\
function parse(input: string): string;
function parse(input: number): number;
function parse<T>(input: T): T;
function parse(input: unknown): unknown {
  return input;
}

// Works fine for concrete calls, but:
function wrapper<T extends string | number>(val: T): T {
  return parse(val); // ❌ No overload matches — T doesn't narrow to string or number
}""",
]
