import { motion } from 'framer-motion';

export function Dashboard() {
  return (
    <div className="p-8 space-y-8">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <button className="bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90 transition-colors">
          Analyze New Repository
        </button>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {[
          { title: "Total Scans", value: "14" },
          { title: "Active Agents", value: "3" },
          { title: "Issues Found", value: "24" },
          { title: "Avg. Coverage", value: "89%" }
        ].map((stat, i) => (
          <motion.div 
            key={stat.title}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.1 }}
            className="rounded-xl border border-border bg-card text-card-foreground shadow-sm p-6"
          >
            <div className="flex flex-row items-center justify-between space-y-0 pb-2">
              <h3 className="tracking-tight text-sm font-medium">{stat.title}</h3>
            </div>
            <div className="text-2xl font-bold">{stat.value}</div>
          </motion.div>
        ))}
      </div>

      <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
        <h3 className="text-lg font-semibold mb-4">Recent Executions</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between border-b border-border pb-4">
            <div>
              <p className="font-medium">sentinel-core / #123</p>
              <p className="text-sm text-muted-foreground">Running API tests...</p>
            </div>
            <div className="text-sm px-2 py-1 bg-secondary text-secondary-foreground rounded-full">
              In Progress
            </div>
          </div>
          <div className="flex items-center justify-between border-b border-border pb-4">
            <div>
              <p className="font-medium">frontend-app / #89</p>
              <p className="text-sm text-muted-foreground">Passed all checks</p>
            </div>
            <div className="text-sm px-2 py-1 bg-green-900/50 text-green-400 rounded-full">
              Success
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
