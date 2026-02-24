"""
snippets/react.py — Realistic React/TypeScript code snippets for question injection.
"""

REACT_SNIPPETS = [
    # 1. Stale closure in useEffect
    """\
const [filter, setFilter] = useState('');
const debouncedFetch = useCallback(
  debounce(() => {
    fetchData(filter); // filter is stale here
  }, 300),
  [] // missing dependency
);

useEffect(() => {
  debouncedFetch();
}, [filter]);""",

    # 2. useMemo with object identity issue
    """\
const columns = useMemo(() => [
  { key: 'name', label: 'Name' },
  { key: 'role', label: 'Role' },
  { key: 'status', label: 'Status' },
], []); // stable — but DataTable still re-renders every time

return <DataTable columns={columns} rows={rows} onSort={handleSort} />;""",

    # 3. Custom hook with race condition
    """\
function useUserData(userId: string) {
  const [data, setData] = useState<User | null>(null);

  useEffect(() => {
    fetchUser(userId).then(setData); // no cleanup — sets state after unmount
  }, [userId]);

  return data;
}""",

    # 4. Context value causing mass re-render
    """\
const AppContext = createContext<AppState>({} as AppState);

export function AppProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [notifications, setNotifications] = useState<Notif[]>([]);

  // Every state change re-renders ALL consumers
  return (
    <AppContext.Provider value={{ user, setUser, theme, setTheme, notifications, setNotifications }}>
      {children}
    </AppContext.Provider>
  );
}""",

    # 5. useReducer with derived state
    """\
type Action =
  | { type: 'SET_ROWS'; payload: Row[] }
  | { type: 'TOGGLE_ROW'; id: string }
  | { type: 'SELECT_ALL' };

function tableReducer(state: TableState, action: Action): TableState {
  switch (action.type) {
    case 'TOGGLE_ROW':
      return {
        ...state,
        selected: state.selected.has(action.id)
          ? new Set([...state.selected].filter(id => id !== action.id))
          : new Set([...state.selected, action.id]),
      };
    case 'SELECT_ALL':
      return { ...state, selected: new Set(state.rows.map(r => r.id)) };
    default:
      return state;
  }
}""",

    # 6. React.memo with inline function prop
    """\
const Row = React.memo(({ row, onDelete }: RowProps) => {
  // still re-renders because onDelete is recreated each parent render
  return (
    <tr>
      <td>{row.name}</td>
      <td><button onClick={() => onDelete(row.id)}>Delete</button></td>
    </tr>
  );
});

// Parent:
<Row row={row} onDelete={(id) => dispatch({ type: 'DELETE', id })} />
// ^ inline arrow = new reference each render, memo is useless""",

    # 7. Suspense with error boundary
    """\
<ErrorBoundary fallback={<ErrorFallback />}>
  <Suspense fallback={<TableSkeleton />}>
    <DataTable resource={resource} />
  </Suspense>
</ErrorBoundary>

// DataTable.tsx
function DataTable({ resource }: { resource: Resource<Row[]> }) {
  const rows = resource.read(); // throws a promise or error
  return <>{rows.map(r => <Row key={r.id} row={r} />)}</>;
}""",

    # 8. forwardRef with generic component
    """\
const Select = forwardRef(
  <T extends { id: string; label: string }>(
    { options, value, onChange }: SelectProps<T>,
    ref: ForwardedRef<HTMLSelectElement>
  ) => (
    <select ref={ref} value={value?.id} onChange={e => onChange(options.find(o => o.id === e.target.value)!)}>
      {options.map(o => <option key={o.id} value={o.id}>{o.label}</option>)}
    </select>
  )
);""",
]
