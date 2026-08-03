import { motion } from 'framer-motion';

export function Agents() {
  return (
    <div className="p-8 space-y-8">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold tracking-tight">Agents Network</h2>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {[
          { name: "Repository Analyzer", role: "Understands structure and tech stack", status: "Idle", icon: "🧠" },
          { name: "Test Planner", role: "Plans execution graph", status: "Busy", icon: "🗺️" },
          { name: "Unit Testing Agent", role: "Writes & runs unit tests", status: "Offline", icon: "🧪" },
        ].map((agent, i) => (
          <motion.div 
            key={agent.name}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.1 }}
            className="rounded-xl border border-border bg-card text-card-foreground shadow-sm p-6 flex flex-col space-y-2 relative overflow-hidden"
          >
            <div className="text-4xl mb-2">{agent.icon}</div>
            <h3 className="tracking-tight text-lg font-semibold">{agent.name}</h3>
            <p className="text-sm text-muted-foreground">{agent.role}</p>
            <div className="mt-4 pt-4 border-t border-border flex items-center gap-2">
               <span className={`w-2 h-2 rounded-full ${
                  agent.status === 'Idle' ? 'bg-blue-500' : 
                  agent.status === 'Busy' ? 'bg-yellow-500 animate-pulse' : 'bg-red-500'
               }`} />
               <span className="text-sm">{agent.status}</span>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
