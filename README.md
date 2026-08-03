# SentinelQA 🛡️ 

**Autonomous AI Software Testing Engineer**

SentinelQA is an Agentic AI platform capable of testing any software project without manual intervention. Built as a production-ready SaaS product, it leverages LangGraph, React, FastAPI, and Docker to provide a seamless QA experience.

## 🚀 Features
- **Zero-Config Testing**: Automatically detects languages, frameworks, and testing tools.
- **AI Agents**: LangGraph-powered agents (Planner, Analyzer, Executors).
- **Isolated Execution**: Runs tests in secure Docker containers using the Docker SDK.
- **Real-time Engine**: WebSockets stream live execution logs and progress to the dashboard.
- **Root Cause Analysis**: Explains test failures instead of just dumping stack traces.

## 🏗️ Architecture

- **Frontend**: React, Vite, TailwindCSS, Shadcn UI, Framer Motion
- **Backend**: FastAPI (Python), PostgreSQL, SQLAlchemy, Redis, WebSockets, JWT Auth
- **AI Engine**: LangChain, LangGraph, ChromaDB, OpenAI/Anthropic
- **Execution**: Celery background jobs, Docker Engine API for sandboxing

## 📦 Installation

To run the full stack locally:

```bash
# Clone the repository
git clone https://github.com/your-username/SentinelQA.git
cd SentinelQA

# Copy environment variables
cp .env.example .env

# Start all services
docker compose up --build
```

The services will be available at:
- **Frontend Dashboard**: `http://localhost:3000`
- **Backend API**: `http://localhost:8080/api/v1`
- **API Documentation (Swagger)**: `http://localhost:8080/api/v1/openapi.json`

## 🐳 Docker Setup
SentinelQA requires access to the host's Docker socket to spawn isolated test environments. Ensure your host system permits this mapping (`/var/run/docker.sock`).

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License
This project is licensed under the MIT License.
