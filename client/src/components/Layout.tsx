import { Outlet, Link, useNavigate } from 'react-router-dom';

export function Layout() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="flex h-screen bg-background text-foreground">
      <aside className="w-64 bg-card border-r border-border flex flex-col">
        <div className="p-4 text-xl font-bold border-b border-border text-primary">
          SentinelQA
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <Link to="/" className="block px-4 py-2 rounded-md hover:bg-secondary text-foreground transition-colors">Dashboard</Link>
          <Link to="/projects" className="block px-4 py-2 rounded-md hover:bg-secondary text-foreground transition-colors">Projects</Link>
          <Link to="/executions" className="block px-4 py-2 rounded-md hover:bg-secondary text-foreground transition-colors">Executions</Link>
          <Link to="/agents" className="block px-4 py-2 rounded-md hover:bg-secondary text-foreground transition-colors">Agents</Link>
        </nav>
        <div className="p-4 border-t border-border">
          <button 
            onClick={handleLogout}
            className="w-full px-4 py-2 text-left rounded-md hover:bg-destructive hover:text-destructive-foreground transition-colors"
          >
            Logout
          </button>
        </div>
      </aside>
      <main className="flex-1 overflow-auto bg-background">
        <Outlet />
      </main>
    </div>
  );
}
