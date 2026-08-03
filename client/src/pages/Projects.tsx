import { motion } from 'framer-motion';

export function Projects() {
  return (
    <div className="p-8 space-y-8">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold tracking-tight">Projects</h2>
        <button className="bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90 transition-colors">
          Add Project
        </button>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {[
          { name: "sentinel-core", description: "Core AI engine repository", status: "Active" },
          { name: "frontend-app", description: "Main React dashboard", status: "Active" },
          { name: "payment-gateway", description: "Billing service", status: "Inactive" },
        ].map((project, i) => (
          <motion.div 
            key={project.name}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.1 }}
            className="rounded-xl border border-border bg-card text-card-foreground shadow-sm p-6 flex flex-col space-y-2"
          >
            <h3 className="tracking-tight text-lg font-semibold">{project.name}</h3>
            <p className="text-sm text-muted-foreground">{project.description}</p>
            <div className="mt-4 pt-4 border-t border-border flex justify-between items-center">
              <span className={`text-xs px-2 py-1 rounded-full ${project.status === 'Active' ? 'bg-green-900/50 text-green-400' : 'bg-secondary text-secondary-foreground'}`}>
                {project.status}
              </span>
              <button className="text-sm text-primary hover:underline">View Scans</button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
