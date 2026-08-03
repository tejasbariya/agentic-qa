import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { io } from 'socket.io-client';

export function Executions() {
  const [logs, setLogs] = useState<string[]>([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const socket = io("ws://localhost:8080/ws/dashboard", {
      transports: ["websocket"],
      reconnectionAttempts: 5
    });

    socket.on('connect', () => {
      setIsConnected(true);
      setLogs(prev => [...prev, "Connected to Realtime Execution Engine..."]);
    });

    socket.on('disconnect', () => {
      setIsConnected(false);
      setLogs(prev => [...prev, "Disconnected..."]);
    });

    socket.on('message', (data) => {
      setLogs(prev => [...prev, data]);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <div className="p-8 space-y-8 flex flex-col h-full">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold tracking-tight flex items-center gap-2">
          Executions
          <span className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
        </h2>
      </div>

      <div className="flex-1 rounded-xl border border-border bg-black text-green-400 p-4 font-mono text-sm overflow-y-auto shadow-inner min-h-[60vh]">
        {logs.map((log, i) => (
          <motion.div 
            key={i}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
          >
            {log}
          </motion.div>
        ))}
        {logs.length === 0 && <div className="text-muted-foreground">Waiting for execution logs...</div>}
      </div>
    </div>
  );
}
