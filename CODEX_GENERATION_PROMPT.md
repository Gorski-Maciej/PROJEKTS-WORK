# 🤖 CodeX Generation Prompt - PROJEKTS-WORK

**Cel**: Automatyzacja generacji kodu, Dockerfile, testów i konfiguracji dla 4 projektów mikrousług.

---

## 📋 Kontekst

Repozytorium zawiera 4 niezależne projekty Python FastAPI zarządzane przez Docker Compose:

1. **CloudBudget** - FinOps platform (FastAPI + PostgreSQL + DuckDB + RabbitMQ + Celery)
2. **InfraFlow** - Infrastructure monitoring (FastAPI + TimescaleDB + Prometheus + Grafana)
3. **NetGuardian** - SecOps/SIEM (FastAPI + Kafka + TimescaleDB + DuckDB)
4. **NetAegis** - Agent orchestration (FastAPI + MCP servers + Multiple agents)

---

## 🎯 Prompt dla CodeX (Complete Generation Task)

```markdown
# Full Repository Code Generation & Architecture Scaffolding

## Objective
Generate production-ready code, Dockerfiles, tests, and configurations for a 4-service microservices 
ecosystem using Docker Compose. Ensure all services are independently deployable, 
interconnected, resilient with health checks, and include comprehensive test coverage.

## Repository Structure
```
PROJEKTS-WORK/
├── cloudbudget/           # FinOps platform
├── infraflow/             # Infrastructure monitoring
├── netguardian/           # SecOps/SIEM platform
├── netaegis/              # Agent orchestration system
├── docker-compose.yml     # Global orchestration (generate)
├── Makefile               # Build automation
├── verify_all_ports.sh    # Port collision detector (exists)
└── README.md              # Main documentation
```

## Services to Generate

### 1. CloudBudget (Port: 8100)
**Architecture**: [FastAPI API] + [PostgreSQL] + [DuckDB] + [Redis] + [RabbitMQ] + [Celery Worker] + [Frontend]

**Files to Generate**:

#### `cloudbudget/api/Dockerfile`
- Python 3.12 slim base
- Install dependencies from requirements.txt
- EXPOSE 8000
- Healthcheck: GET /docs endpoint
- Multi-stage build to optimize size

#### `cloudbudget/api/main.py`
- FastAPI app initialization
- JWT authentication middleware
- CORS configuration
- API routes: /health, /docs, /auth/login
- Database initialization on startup
- Graceful shutdown handling

#### `cloudbudget/api/core/database.py`
- SQLAlchemy ORM setup with PostgreSQL
- DuckDB initialization (create file at /data/cloudbudget.duckdb)
- Connection pooling with psycopg
- Migration support with Alembic
- Schema: tables for costs, recommendations, audit logs

#### `cloudbudget/api/core/celery_app.py`
- Celery initialization with RabbitMQ broker
- Task definitions: cost.ingest, cost.analyze, action.exec
- Retry policies with exponential backoff
- Error handling and logging

#### `cloudbudget/api/core/auth.py`
- JWT token generation/validation (min 32 chars)
- Demo user: username=demo, password=demo
- Token expiration: 24h
- Role-based access control (RBAC)

#### `cloudbudget/api/routes/health.py`
- GET /health - Full service health
- GET /docs - Swagger UI redirect
- Check: database, redis, rabbitmq connectivity

#### `cloudbudget/api/routes/costs.py`
- GET /api/v1/costs - List costs with pagination
- POST /api/v1/costs/ingest - Trigger cost ingestion
- GET /api/v1/recommendations - Cost optimization recommendations
- Async endpoints for large data processing

#### `cloudbudget/api/routes/auth.py`
- POST /auth/login - JWT token generation
- POST /auth/validate - Token validation
- POST /auth/refresh - Token refresh

#### `cloudbudget/frontend/Dockerfile`
- Node.js 20 slim base
- React + Vite build
- EXPOSE 3000
- Nginx reverse proxy in production

#### `cloudbudget/frontend/package.json`
- React 18, React Router v6
- Axios for API calls
- Chart.js for data visualization
- Tailwind CSS for styling
- ESLint + Prettier

#### `cloudbudget/frontend/src/App.jsx`
- Dashboard component
- Cost overview with charts
- Recommendations list
- Authentication flow

#### `cloudbudget/requirements.txt`
```
fastapi==0.116.0
uvicorn==0.35.0
pydantic==2.11.0
sqlalchemy==2.0.0
psycopg[binary]==3.2.0
alembic==1.16.0
celery==5.5.0
redis==6.2.0
duckdb==1.3.0
polars==1.31.0
prophet==1.1.7
scikit-learn==1.7.0
prometheus-client==0.22.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
strawberry-graphql[fastapi]==0.275.0
pytest==8.0.0
pytest-asyncio==0.23.0
httpx==0.25.0
```

#### `cloudbudget/tests/test_health.py`
- Test GET /health endpoint
- Test database connectivity
- Test redis connectivity
- Test JWT authentication
- Mark with @pytest.mark.integration

#### `cloudbudget/tests/test_api.py`
- Test /auth/login endpoint
- Test GET /api/v1/costs
- Test POST /api/v1/costs/ingest
- Test GET /api/v1/recommendations
- Test error handling (401, 403, 500)

#### `cloudbudget/tests/conftest.py`
- Pytest fixtures for FastAPI test client
- Mock database connections
- Mock Redis
- Mock RabbitMQ

#### `cloudbudget/scripts/setup.sh`
```bash
#!/bin/bash
set -e
echo "Setting up CloudBudget..."
cp .env.example .env || true
docker compose up -d
echo "CloudBudget started on http://localhost:8100"
```

#### `cloudbudget/.env.example`
```
JWT_SECRET=CHANGE_ME_WITH_A_LONG_RANDOM_SECRET_MIN_32_CHARS
POSTGRES_DB=cloudbudget
POSTGRES_USER=cloudbudget
POSTGRES_PASSWORD=CHANGE_ME_SECURE_PASSWORD
DATABASE_URL=postgresql+psycopg://cloudbudget:CHANGE_ME_SECURE_PASSWORD@postgres:5432/cloudbudget
REDIS_URL=redis://redis:6379/0
RABBITMQ_URL=amqp://guest:CHANGE_ME_SECURE_PASSWORD@rabbitmq:5672//
CELERY_BROKER_URL=amqp://guest:CHANGE_ME_SECURE_PASSWORD@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/1
DUCKDB_PATH=/data/cloudbudget.duckdb
SLACK_WEBHOOK_URL=
```

#### `cloudbudget/Makefile` (project-specific)
```makefile
.PHONY: up down logs test build clean

up:
	docker compose up -d
	@echo "CloudBudget running on http://localhost:8100"

down:
	docker compose down

logs:
	docker compose logs -f api

test:
	pytest -v tests/

build:
	docker compose build --no-cache

clean:
	docker compose down -v --rmi all
```

---

### 2. InfraFlow (Port: 8001)
**Architecture**: [FastAPI Engine] + [TimescaleDB] + [Redis Queue] + [Worker] + [Dashboard] + [Prometheus] + [Grafana]

**Files to Generate**:

#### `infraflow/engine/Dockerfile`
- Python 3.12 slim
- Install dependencies
- EXPOSE 8000
- Healthcheck via HTTP

#### `infraflow/engine/main.py`
- FastAPI app
- TimescaleDB connection
- Prometheus metrics
- Streaming metrics endpoint

#### `infraflow/engine/worker/queue_worker.py`
- Redis queue consumer
- Process metric ingestion jobs
- Graceful shutdown (SIGTERM/SIGINT)
- Retry mechanism with exponential backoff

#### `infraflow/engine/models/metric.py`
- SQLAlchemy ORM for metrics
- TimescaleDB hypertable extension
- Schema: host_metrics, event_logs

#### `infraflow/dashboard/Dockerfile`
- Node.js 20 slim
- React + Chart.js

#### `infraflow/dashboard/src/App.jsx`
- Real-time metrics dashboard
- WebSocket connection to engine
- Charts for CPU, Memory, Disk

#### `infraflow/prometheus/prometheus.yml`
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'infraflow'
    static_configs:
      - targets: ['engine:8000']
```

#### `infraflow/grafana/provisioning/datasources/prometheus.yml`
```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
    access: proxy
    isDefault: true
```

#### `infraflow/.env.example`
```
JWT_SECRET=CHANGE_ME_WITH_A_LONG_RANDOM_SECRET_MIN_32_CHARS
DATABASE_URL=postgresql://postgres:CHANGE_ME@timescaledb:5432/infraflow
REDIS_HOST=redis
REDIS_PORT=6379
CONFIG_PATH=/app/config/servers.yml
```

#### `infraflow/tests/test_health.py`
- Test GET /health endpoint
- Test TimescaleDB connectivity
- Test Redis connectivity
- Test metrics collection

#### `infraflow/scripts/setup.sh`
```bash
#!/bin/bash
set -e
cp .env.example .env || true
docker compose up -d
echo "InfraFlow started on http://localhost:8001"
```

---

### 3. NetGuardian (Port: 8300)
**Architecture**: [FastAPI Engine] + [Kafka] + [Zookeeper] + [TimescaleDB] + [DuckDB] + [Redis] + [Agent] + [Dashboard] + [Prometheus] + [Grafana]

**Files to Generate**:

#### `netguardian/engine/Dockerfile`
- Python 3.12 slim
- Install dependencies including kafka-python
- EXPOSE 8000
- Healthcheck

#### `netguardian/engine/main.py`
- FastAPI app
- Kafka consumer initialization
- WebSocket support for real-time events
- API endpoints: /health, /events, /rules

#### `netguardian/engine/kafka_consumer.py`
- Kafka message processing
- Event correlation engine
- DuckDB offline storage
- Alert generation

#### `netguardian/engine/geoip.py`
- GeoIP enrichment (optional with SKIP_GEOIP_CHECK)
- Fallback if database not found

#### `netguardian/agent/Dockerfile`
- Python 3.12 slim
- Kafka producer
- Network packet capture capabilities

#### `netguardian/agent/main.py`
- Network event listener
- Kafka producer for events
- SSH key support for remote access

#### `netguardian/scripts/initialize-ssh-keys.sh`
```bash
#!/bin/bash
SSH_DIR="./engine/ssh"
mkdir -p "$SSH_DIR"
if [[ ! -f "$SSH_DIR/id_rsa" ]]; then
  ssh-keygen -t rsa -b 4096 -f "$SSH_DIR/id_rsa" -N ""
  chmod 600 "$SSH_DIR/id_rsa"
  echo "SSH keys generated"
fi
```

#### `netguardian/scripts/download_geoip.sh`
```bash
#!/bin/bash
# Download MaxMind GeoLite2 City (requires free account)
# https://www.maxmind.com/en/accounts/current/license-key
GEOIP_PATH="./engine/data/GeoLite2-City.mmdb"
mkdir -p ./engine/data
if [[ ! -f "$GEOIP_PATH" ]]; then
  echo "Downloading GeoIP database..."
  # Use LICENSE_KEY from .env
  # curl -L "https://download.maxmind.com/..." -o "$GEOIP_PATH"
  echo "Skipping - set MAXMIND_LICENSE_KEY in .env"
fi
```

#### `netguardian/agent/authorized_keys`
```
ssh-rsa AAAA... # generated key
```

#### `netguardian/.env.example`
```
JWT_SECRET=CHANGE_ME_WITH_A_LONG_RANDOM_SECRET_MIN_32_CHARS
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
REDIS_HOST=redis
DATABASE_URL=postgresql://postgres:CHANGE_ME@timescaledb:5432/netguardian
DUCKDB_PATH=/data/netguardian.db
SKIP_GEOIP_CHECK=true
GEOIP_DB=/app/data/GeoLite2-City.mmdb
ABUSEIPDB_API_KEY=
MISP_URL=
MISP_KEY=
SSH_PRIVATE_KEY_FILE=/app/ssh/id_rsa
SSH_AGENT_HOST=agent
SSH_AGENT_USER=root
SLACK_WEBHOOK_URL=
```

#### `netguardian/tests/test_health.py`
- Test Kafka connectivity
- Test TimescaleDB connectivity
- Test DuckDB file creation
- Test WebSocket events

#### `netguardian/scripts/setup.sh`
```bash
#!/bin/bash
set -e
cp .env.example .env || true
bash scripts/initialize-ssh-keys.sh
# bash scripts/download_geoip.sh  # Optional
docker compose up -d
echo "NetGuardian started on http://localhost:8300"
```

---

### 4. NetAegis (Port: 8400)
**Architecture**: [main_mcp] + [operational_mcp] + [netpulse_agent] + [seclog_agent] + [netconfig_agent] + [Frontend]

**Files to Generate**:

#### `netaegis/server/main_mcp/Dockerfile`
- Python 3.12 slim
- FastAPI + MCP framework
- EXPOSE 8000

#### `netaegis/server/main_mcp/main.py`
- MCP server for orchestration
- API routes: /api/realtime/health, /api/incidents, /api/policies
- Redis backend connection
- WebSocket support

#### `netaegis/server/operational_mcp/Dockerfile`
- Python 3.12 slim

#### `netaegis/server/operational_mcp/main.py`
- MCP server for operational agents
- Agent management endpoints
- Task dispatch
- Result aggregation

#### `netaegis/agents/netpulse/Dockerfile`
- Python 3.12 slim
- Network telemetry agent

#### `netaegis/agents/netpulse/main.py`
- Periodic network health checks
- Connectivity monitoring
- POST results to operational_mcp

#### `netaegis/agents/seclog/Dockerfile`
- Python 3.12 slim

#### `netaegis/agents/seclog/main.py`
- Security log aggregator
- Monitor /var/log/auth.log, /var/log/nginx/access.log
- Parse and send to operational_mcp
- File tailing with inotify

#### `netaegis/agents/netconfig/Dockerfile`
- Python 3.12 slim
- SSH client

#### `netaegis/agents/netconfig/main.py`
- Network device configuration agent
- SSH connection to device (NETCONFIG_DEVICE_IP)
- Config backup and deployment

#### `netaegis/frontend/Dockerfile`
- Node.js 20 slim

#### `netaegis/frontend/src/App.jsx`
- Multi-agent dashboard
- Real-time status monitoring
- Incident management UI

#### `netaegis/.env.example`
```
NETCONFIG_DEVICE_IP=192.168.1.1
NETCONFIG_DEVICE_USERNAME=CHANGE_ME
NETCONFIG_DEVICE_PASSWORD=CHANGE_ME
NETPULSE_INTERVAL=30
SECLOG_WATCH_PATHS=/var/log/auth.log,/var/log/nginx/access.log
OPERATIONAL_MCP_URL=http://operational_mcp:8001
MAIN_MCP_URL=http://main_mcp:8000
```

#### `netaegis/scripts/setup.sh`
```bash
#!/bin/bash
set -e
cp .env.example .env || true
docker compose up -d
echo "NetAegis started on http://localhost:8400"
```

---

### 5. Global docker-compose.yml (Root)
**Generate orchestration file that coordinates all services**:

```yaml
version: '3.9'

services:
  # CloudBudget stack
  cloudbudget-postgres:
    ...

  # InfraFlow stack
  infraflow-timescaledb:
    ...

  # NetGuardian stack
  netguardian-kafka:
    ...

  # NetAegis stack
  netaegis-redis:
    ...

# Global validation via verify_all_ports.sh
```

---

## ✅ Quality Requirements

### Code Quality
- Python 3.12+ with type hints
- PEP 8 compliance (Black, isort, flake8)
- DocStrings for all public functions
- Error handling with custom exceptions

### Docker
- Multi-stage builds to minimize image size
- Non-root user execution
- Health checks for all services
- Graceful shutdown handling

### Security
- No hardcoded secrets (use .env)
- JWT token validation
- CORS configuration
- SQL injection prevention via ORM
- Password hashing with bcrypt

### Testing
- Unit tests with pytest (60%+ coverage)
- Integration tests with Docker services
- Mock external dependencies
- Async test support with pytest-asyncio
- Fixtures for common setup

### Documentation
- Comprehensive README per project
- API documentation (OpenAPI/Swagger)
- Deployment guide
- Troubleshooting section
- Architecture diagrams (ASCII art)

---

## 📋 Deliverables

```
For EACH project (cloudbudget, infraflow, netguardian, netaegis):

1. ✅ Dockerfile (optimized, multi-stage)
2. ✅ Python application (main.py + modules)
3. ✅ Requirements management (requirements.txt or pyproject.toml)
4. ✅ Configuration files (.env.example, config.yml)
5. ✅ Unit tests (tests/test_*.py)
6. ✅ Integration tests (tests/test_integration.py)
7. ✅ Setup script (scripts/setup.sh)
8. ✅ Makefile (build/test/run targets)
9. ✅ Documentation (README.md with examples)
10. ✅ Helper scripts (where needed: init_db.py, setup-keys.sh)
```

**Global deliverables**:
1. ✅ Root docker-compose.yml (coordinates all services)
2. ✅ Root Makefile (all, down, test, clean targets)
3. ✅ Comprehensive architecture documentation

---

## 🚀 Success Criteria

- [ ] All projects build successfully: `make build`
- [ ] All projects start: `make all`
- [ ] All health checks pass: `docker compose ps` shows healthy
- [ ] All APIs respond: `curl http://localhost:8100/docs` (and 8001, 8300, 8400)
- [ ] All tests pass: `make test`
- [ ] Port verification passes: `./verify_all_ports.sh` returns 0
- [ ] All services interconnected: Services can reach databases, brokers, etc.
- [ ] Graceful shutdown: `make down` stops all services cleanly

---

## 🔄 Iteration Process

1. **Phase 1**: Generate core application files for each service
2. **Phase 2**: Generate Dockerfiles and validate builds
3. **Phase 3**: Generate test suites and validate coverage
4. **Phase 4**: Generate documentation and helper scripts
5. **Phase 5**: Integration testing and troubleshooting

---

## 📝 Notes

- Use Alpine/slim base images for optimization
- Implement proper logging (structured JSON logs)
- Add OpenTelemetry for distributed tracing (optional but recommended)
- Use environment variables for all configuration
- Implement circuit breaker pattern for external API calls
- Add request/response middleware for logging and metrics
```

---

## 🎯 Quick Start Template (After Code Generation)

```bash
# 1. Generate all code
codex generate --prompt CODEX_GENERATION_PROMPT.md --output ./

# 2. Validate setup
./verify_all_ports.sh

# 3. Build all services
make build

# 4. Start all services
make all

# 5. Check health
docker compose ps

# 6. Run tests
make test

# 7. View logs
docker compose logs -f
```

---

## 🔗 Related Files

- `REPOSITORY_AUDIT_REPORT.md` - Detailed audit findings
- `Makefile` - Build orchestration
- `verify_all_ports.sh` - Port collision detector
- `README.md` - Main repository documentation

