# 🛡️ SentinelQA — Agentic Testing Assistant

> An AI-powered autonomous testing agent that discovers, runs, diagnoses, and reports on unit tests, API tests, and linting — so you don't have to.

![Node](https://img.shields.io/badge/node-20.x-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Stack](https://img.shields.io/badge/stack-MERN-yellow)
![LangChain](https://img.shields.io/badge/LangChain-LangGraph-purple)
![MCP](https://img.shields.io/badge/protocol-MCP-orange)

---

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [MCP Server Setup](#mcp-server-setup)
- [LangChain & LangGraph Agent](#langchain--langgraph-agent)
- [MERN Frontend & API](#mern-frontend--api)
- [Rate Limiting](#rate-limiting)
- [XSS Prevention](#xss-prevention)
- [Running the Project](#running-the-project)
- [GitHub Actions CI](#github-actions-ci)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

SentinelQA is an agentic QA system that combines **LangGraph** orchestration, **MCP (Model Context Protocol)** tool servers, and a **MERN** dashboard to give you intelligent, automated test coverage with real root-cause analysis.

Unlike a regular CI pipeline, SentinelQA:

- Reads your `git diff` to decide *which* tests actually need to run
- Calls modular MCP servers to execute pytest, API checks, and linters
- Feeds failures to an LLM (Groq Llama 3.3 70B — free tier) for root-cause diagnosis
- Posts results to your Streamlit or React dashboard, Slack, and GitHub PR comments

**Everything runs on free-tier infrastructure.**

---

## How It Works

```
git push / cron / Slack trigger
         │
         ▼
  LangGraph Agent reads git diff
         │
         ├──► mcp-pytest   → unit test results
         ├──► mcp-api      → endpoint health results
         └──► mcp-lint     → lint violations
                  │
                  ▼
        LLM diagnosis (Groq Llama 3.3)
                  │
                  ▼
     MongoDB  ←  saves run
                  │
         ┌────────┴────────┐
         ▼                 ▼
  React dashboard    Slack / GitHub PR
```

---

## Tech Stack

### Backend — Python AI Agent

| Tool | Purpose |
|---|---|
| LangGraph | Agent orchestration (state machine) |
| LangChain | LLM tool-calling abstraction |
| MCP (Model Context Protocol) | Modular test runner protocol |
| Groq API | Free LLM inference (Llama 3.3 70B) |
| FastAPI | Python REST API layer |
| pytest + pytest-json-report | Unit test runner |
| httpx | API endpoint health checks |
| Flake8 / ESLint | Python & JS linting |

### MERN Stack — Dashboard & API Gateway

| Tool | Purpose |
|---|---|
| MongoDB | Test run history storage |
| Express.js | REST API gateway (Node.js) |
| React + Vite | Dashboard UI |
| Node.js 20 | Runtime |
| Mongoose | MongoDB ODM |
| Axios | HTTP client |
| Recharts | Pass/fail trend charts |
| TailwindCSS | Styling |

### Security

| Tool | Purpose |
|---|---|
| express-rate-limit | API rate limiting |
| helmet | HTTP security headers |
| DOMPurify | XSS prevention on client |
| xss-clean | XSS sanitization middleware |
| express-mongo-sanitize | NoSQL injection prevention |
| hpp | HTTP parameter pollution protection |
| cors | Controlled CORS policy |

### DevOps

| Tool | Purpose |
|---|---|
| GitHub Actions | CI/CD trigger |
| Docker Compose | Local multi-service orchestration |
| dotenv | Environment config |
| Prettier | Code formatting |

---

## Architecture

```
sentinelqa/
│
├── agent/                        ← Python AI agent (LangGraph)
│   ├── orchestrator.py           ← Main LangGraph state machine
│   ├── tools.py                  ← MCP tool wrappers for LangChain
│   ├── prompts.py                ← LLM prompt templates
│   └── diagnosis.py              ← Root-cause analysis logic
│
├── mcp_servers/                  ← MCP protocol servers
│   ├── pytest_server.py          ← Wraps pytest CLI as MCP tool
│   ├── api_server.py             ← Wraps httpx API checks as MCP tool
│   └── lint_server.py            ← Wraps Flake8/ESLint as MCP tool
│
├── server/                       ← Node.js / Express API (MERN)
│   ├── src/
│   │   ├── app.js                ← Express app entry
│   │   ├── server.js             ← HTTP server bootstrap
│   │   ├── config/
│   │   │   └── db.js             ← MongoDB connection
│   │   ├── middleware/
│   │   │   ├── rateLimiter.js    ← express-rate-limit setup
│   │   │   ├── security.js       ← helmet, xss-clean, hpp, cors
│   │   │   └── errorHandler.js   ← Global error handler
│   │   ├── models/
│   │   │   └── TestRun.js        ← Mongoose schema
│   │   ├── routes/
│   │   │   ├── runs.js           ← GET/POST test runs
│   │   │   └── trigger.js        ← POST /api/trigger — starts agent
│   │   └── controllers/
│   │       ├── runsController.js
│   │       └── triggerController.js
│   ├── package.json
│   └── .env
│
├── client/                       ← React dashboard (MERN)
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── RunsTable.jsx     ← Test run history
│   │   │   ├── DiagnosisCard.jsx ← LLM diagnosis display
│   │   │   ├── TrendChart.jsx    ← Pass/fail over time
│   │   │   └── TriggerButton.jsx ← Manual run trigger
│   │   ├── hooks/
│   │   │   └── useRuns.js        ← Data fetching hook
│   │   └── utils/
│   │       └── sanitize.js       ← DOMPurify XSS helpers
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── reporting/
│   ├── notifier.py               ← Slack & GitHub PR notifications
│   └── dashboard.py             ← Optional Streamlit UI
│
├── storage/
│   └── db.py                     ← SQLite fallback (offline mode)
│
├── .github/
│   └── workflows/
│       └── sentinelqa.yml        ← GitHub Actions CI
│
├── docker-compose.yml            ← Local dev orchestration
├── main.py                       ← Python agent entry point
├── config.yaml                   ← Test targets & settings
├── requirements.txt              ← Python dependencies
├── .env.example                  ← Environment variable template
├── .nvmrc                        ← Node version pin
├── .prettierrc                   ← Code formatting config
└── LICENSE
```

---

## Prerequisites

- **Node.js** 20.x (see `.nvmrc`)
- **Python** 3.11+
- **MongoDB** (local or MongoDB Atlas free tier)
- **Git**
- A free [Groq API key](https://console.groq.com)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/sentinelqa.git
cd sentinelqa
```

### 2. Use the correct Node version

```bash
nvm use        # reads .nvmrc automatically
```

### 3. Install Node dependencies

```bash
# Express API
cd server && npm install

# React client
cd ../client && npm install
```

### 4. Install Python dependencies

```bash
cd ..
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Set up environment variables

```bash
cp .env.example .env
# Fill in your values — see Environment Variables section below
```

### 6. Install Python MCP SDK and test tools

```bash
pip install "mcp[cli]" pytest pytest-json-report httpx flake8
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in all values:

```bash
cp .env.example .env
```

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | Free Groq API key (Llama 3.3 70B) | ✅ |
| `MONGODB_URI` | MongoDB connection string | ✅ |
| `GITHUB_TOKEN` | GitHub personal access token for PR comments | ✅ |
| `SLACK_WEBHOOK_URL` | Slack incoming webhook for notifications | Optional |
| `NODE_ENV` | `development` or `production` | ✅ |
| `PORT` | Express server port (default: 5000) | ✅ |
| `PYTHON_AGENT_URL` | URL of the FastAPI agent service | ✅ |
| `RATE_LIMIT_WINDOW_MS` | Rate limit window in ms (default: 900000) | Optional |
| `RATE_LIMIT_MAX` | Max requests per window (default: 100) | Optional |
| `JWT_SECRET` | Secret for signing tokens (if adding auth) | Optional |
| `CORS_ORIGIN` | Allowed CORS origin (default: http://localhost:5173) | ✅ |

See `.env.example` for the full annotated template.

---

## MCP Server Setup

SentinelQA uses the [Model Context Protocol (MCP)](https://modelcontextprotocol.io) to expose each test runner as an isolated, callable tool server. The LangGraph agent communicates with these servers over `stdio` — no HTTP, no ports needed.

### What is MCP?

MCP is an open standard (by Anthropic) that lets AI agents call external tools via a structured JSON protocol. Each MCP server:

- Declares a list of tools with typed input schemas
- Accepts `call_tool` requests from the agent
- Returns structured results

Think of it as a type-safe plugin system for AI agents.

### Starting MCP servers individually

```bash
# Unit test runner
python mcp_servers/pytest_server.py

# API health checker
python mcp_servers/api_server.py

# Linter
python mcp_servers/lint_server.py
```

### MCP server tool reference

| Server | Tool name | Input | Output |
|---|---|---|---|
| `pytest_server` | `run_unit_tests` | `path`, `filter?` | `{passed, failed, failures[]}` |
| `api_server` | `run_api_tests` | `endpoints[]` | `{results[], passed, failed}` |
| `lint_server` | `run_lint` | `path`, `language` | `{violations[], count}` |

### How the agent calls MCP tools

```python
# agent/tools.py
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def call_mcp_tool(server_script: str, tool_name: str, args: dict) -> dict:
    params = StdioServerParameters(command="python", args=[server_script])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, args)
            return json.loads(result.content[0].text)
```

---

## LangChain & LangGraph Agent

### Why LangGraph?

LangGraph lets you define the agent as an explicit **state machine** — each node is a pure function that reads and updates state. This makes the flow predictable, debuggable, and easy to extend.

### Agent state

```python
class TestState(TypedDict):
    repo_path: str
    git_diff: str          # files changed in last commit
    test_plan: List[str]   # ["unit", "api", "lint"]
    unit_results: dict
    api_results: dict
    lint_results: dict
    diagnosis: str         # LLM root-cause explanation
    report: dict
    errors: List[str]
```

### Agent graph

```
[plan_tests]          reads git diff, decides what to run
      │
      ▼
[run_unit_tests]      calls mcp-pytest tool
      │
      ▼
[run_api_tests]       calls mcp-api tool
      │
      ▼
[run_lint]            calls mcp-lint tool
      │
      ▼
[diagnose_failures]   LLM reads failures + code context → root cause
      │
      ▼
[generate_report]     assembles final report dict
      │
      ▼
     END
```

### LLM setup (Groq — free)

```python
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=1024,
)
```

Groq's free tier provides ~14,400 requests/day on Llama 3.3 70B — more than enough for a dev team.

### Running the agent directly

```bash
source venv/bin/activate
python main.py --trigger=manual
```

---

## MERN Frontend & API

### Express API (server/)

Start the Node API server:

```bash
cd server
npm run dev     # nodemon with hot reload
```

The API exposes:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/runs` | Fetch all test run history |
| `GET` | `/api/runs/:id` | Fetch single run by ID |
| `POST` | `/api/trigger` | Trigger a new agent run |
| `GET` | `/api/health` | Health check |

### React dashboard (client/)

Start the Vite dev server:

```bash
cd client
npm run dev     # http://localhost:5173
```

The dashboard shows:

- Pass/fail summary metrics
- Test run history table with timestamps
- LLM diagnosis cards for failed runs
- Trend chart (pass rate over time)
- Manual trigger button

### MongoDB schema

```js
// server/src/models/TestRun.js
const TestRunSchema = new mongoose.Schema({
  trigger:     { type: String, enum: ['ci', 'manual', 'cron', 'slack'] },
  repo:        String,
  commitSha:   String,
  branch:      String,
  unitPassed:  Number,
  unitFailed:  Number,
  apiPassed:   Number,
  apiFailed:   Number,
  lintViolations: Number,
  diagnosis:   String,
  status:      { type: String, enum: ['pass', 'fail'] },
  durationMs:  Number,
  createdAt:   { type: Date, default: Date.now }
});
```

---

## Rate Limiting

Rate limiting is applied at the Express layer using `express-rate-limit`.

```js
// server/src/middleware/rateLimiter.js
const rateLimit = require('express-rate-limit');

// General API limiter
const apiLimiter = rateLimit({
  windowMs: process.env.RATE_LIMIT_WINDOW_MS || 15 * 60 * 1000, // 15 min
  max: process.env.RATE_LIMIT_MAX || 100,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    status: 429,
    error: 'Too many requests. Please try again after 15 minutes.'
  }
});

// Stricter limiter for trigger endpoint (agent spawns are expensive)
const triggerLimiter = rateLimit({
  windowMs: 60 * 1000,  // 1 minute
  max: 5,
  message: {
    status: 429,
    error: 'Agent trigger rate limit exceeded. Max 5 runs per minute.'
  }
});

module.exports = { apiLimiter, triggerLimiter };
```

Applied in `app.js`:

```js
app.use('/api/', apiLimiter);
app.use('/api/trigger', triggerLimiter);
```

---

## XSS Prevention

### Server-side (Express)

Three layers of protection:

```js
// server/src/middleware/security.js
const helmet      = require('helmet');
const xssClean    = require('xss-clean');
const mongoSanitize = require('express-mongo-sanitize');
const hpp         = require('hpp');
const cors        = require('cors');

module.exports = (app) => {
  // 1. Security headers (CSP, HSTS, X-Frame-Options, etc.)
  app.use(helmet());

  // 2. CORS — only allow your frontend origin
  app.use(cors({
    origin: process.env.CORS_ORIGIN || 'http://localhost:5173',
    methods: ['GET', 'POST'],
    credentials: true
  }));

  // 3. Sanitize user input — strips < > " ' / from req.body, req.params, req.query
  app.use(xssClean());

  // 4. NoSQL injection prevention — strips $ and . from MongoDB queries
  app.use(mongoSanitize());

  // 5. HTTP parameter pollution protection
  app.use(hpp());
};
```

### Client-side (React)

Any LLM-generated diagnosis text (or user-supplied content) must be sanitized before rendering:

```js
// client/src/utils/sanitize.js
import DOMPurify from 'dompurify';

/**
 * Sanitize HTML string before injecting into the DOM.
 * Use this whenever rendering content from API responses.
 */
export const sanitizeHTML = (dirty) => {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['p', 'strong', 'em', 'code', 'pre', 'br', 'ul', 'li'],
    ALLOWED_ATTR: []
  });
};

/**
 * Strip all HTML — use for plain text fields.
 */
export const sanitizeText = (dirty) => {
  return DOMPurify.sanitize(dirty, { ALLOWED_TAGS: [], ALLOWED_ATTR: [] });
};
```

Usage in a component:

```jsx
// DiagnosisCard.jsx
import { sanitizeHTML } from '../utils/sanitize';

export function DiagnosisCard({ diagnosis }) {
  return (
    <div
      className="diagnosis-content"
      dangerouslySetInnerHTML={{ __html: sanitizeHTML(diagnosis) }}
    />
  );
}
```

> **Never** render raw LLM output with `dangerouslySetInnerHTML` without `DOMPurify`. LLM responses can contain arbitrary text including HTML tags.

---

## Running the Project

### Option A — Docker Compose (recommended)

```bash
docker-compose up --build
```

Starts: MongoDB, Express API, React client, Python FastAPI agent.

### Option B — Manual (all services)

```bash
# Terminal 1 — MongoDB (if local)
mongod

# Terminal 2 — Express API
cd server && npm run dev

# Terminal 3 — React client
cd client && npm run dev

# Terminal 4 — Python AI agent (FastAPI mode)
source venv/bin/activate
uvicorn agent.api:app --reload --port 8001

# Run agent manually
python main.py --trigger=manual
```

### Option C — Agent only (no MERN)

```bash
source venv/bin/activate
python main.py --trigger=manual
```

---

## GitHub Actions CI

SentinelQA runs automatically on every push and PR via GitHub Actions.

```yaml
# .github/workflows/sentinelqa.yml
name: SentinelQA

on:
  push:
    branches: [main, develop]
  pull_request:
  workflow_dispatch:

jobs:
  sentinel:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - uses: actions/setup-node@v4
        with:
          node-version-file: ".nvmrc"
      - run: pip install -r requirements.txt
      - name: Run SentinelQA Agent
        env:
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
          REPO: ${{ github.repository }}
          COMMIT_SHA: ${{ github.sha }}
        run: python main.py --trigger=ci
```

Add `GROQ_API_KEY`, `GITHUB_TOKEN`, and `SLACK_WEBHOOK_URL` in your repo's **Settings → Secrets and variables → Actions**.

---

## API Reference

### `POST /api/trigger`

Triggers the AI agent to run tests.

**Rate limit:** 5 requests/minute

**Request body:**
```json
{
  "trigger": "manual",
  "repo_path": "/path/to/repo",
  "branch": "main"
}
```

**Response:**
```json
{
  "status": "started",
  "runId": "64f3a...",
  "message": "Agent triggered successfully"
}
```

### `GET /api/runs`

Returns paginated test run history.

**Query params:** `?page=1&limit=20&status=fail`

**Response:**
```json
{
  "runs": [...],
  "total": 142,
  "page": 1,
  "pages": 8
}
```

### `GET /api/runs/:id`

Returns full details for a single run including LLM diagnosis.

---

## Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

Please run `npm run lint` and `flake8 .` before submitting. Format with `prettier --write .`.

---

## License

MIT — see [LICENSE](./LICENSE) for details.

---

Built with LangGraph, MCP, and the MERN stack. Free to run, open to extend.
