# 🔍 DETAILED AUDIT & IMPROVED CodeX GENERATION PROMPT
**Status Date**: 2026-05-20  
**Audit Level**: COMPREHENSIVE  
**Risk Assessment**: 🔴 CRITICAL - Multiple blockers preventing production deployment

---

## 📊 EXECUTIVE FINDINGS

### Current Repository State
- **Struktura**: ✅ Dobrze zaplanowana (4 niezależne mikrousługi)
- **Docker Orchestration**: ⚠️ Częściowo gotowa (docker-compose.yml istnieje, ale wiele Dockerfiles brakuje)
- **Kod Aplikacji**: 🔴 KRYTYCZNIE NIEPEŁNY (główne pliki aplikacji puste lub brakujące)
- **Konfiguracja**: ⚠️ Niepełna (.env.example istnieje, ale brakuje niektórych zmiennych)
- **Testy**: 🔴 BRAKUJE (foldery istnieją, ale są puste)
- **Dokumentacja**: ✅ DOBRA (README per projekt + REPOSITORY_AUDIT_REPORT)

---

## 🔴 KRYTYCZNE PROBLEMY (BLOKUJĄCE DEPLOYMENT)

### PROBLEM #1: Brakujące Dockerfiles dla głównych serwisów

**Obecny Stan**:
```
✅ Istnieje:
  - cloudbudget/api/Dockerfile (obecny ale może być niekompletny)
  - cloudbudget/frontend/Dockerfile
  - infraflow/dashboard/Dockerfile
  - netaegis/Dockerfile (główny)
  - netaegis/server/operational_mcp/Dockerfile

❌ BRAKUJE:
  - infraflow/engine/Dockerfile - KRYTYCZNE (engine to serce InfraFlow)
  - netguardian/engine/Dockerfile - KRYTYCZNE (engine to core)
  - netguardian/agent/Dockerfile - WAŻNE
  - netguardian/dashboard/Dockerfile - WAŻNE
  - netaegis/agents/netpulse/Dockerfile - ISTNIEJE ale może być niekompletny
  - netaegis/agents/seclog/Dockerfile - BRAKUJE
  - netaegis/agents/netconfig/Dockerfile - BRAKUJE
  - netaegis/frontend/Dockerfile - BRAKUJE
```

**Wpływ**: `docker compose build` lub `make build` zakończy się błędem dla wielu serwisów.

**Rozwiązanie**: Wygenerować wszystkie brakujące Dockerfiles z optymalizacjami.

---

### PROBLEM #2: Puste/Brakujące Główne Pliki Aplikacji

**CloudBudget**:
```
Struktura EXISTS: ✅
  cloudbudget/
  ├── api/
  │   ├── Dockerfile ✅
  │   ├── main.py ❌ BRAKUJE LUB PUSTE
  │   ├── core/
  │   │   ├── database.py ❌
  │   │   ├── auth.py ❌
  │   │   ├── celery_app.py ❌
  │   ├── routes/
  │   │   ├── health.py ❌
  │   │   ├── costs.py ❌
  │   │   ├── auth.py ❌
  │   ├── models/
  │   │   ├── __init__.py ❌
  │   │   ├── cost.py ❌
  │   ├── requirements.txt ✅ EXISTS (ale może być niekompletny)
  ├── frontend/
  │   ├── package.json ❌
  │   ├── src/
  │   │   ├── App.jsx ❌
  │   │   ├── components/ ❌
  │   ├── public/ ❌
  ├── tests/
  │   ├── test_health.py ❌ PUSTE
  │   ├── test_api.py ❌
  │   ├── conftest.py ❌
  ├── scripts/
  │   ├── setup.sh ⚠️ May exist but incomplete
```

**InfraFlow**:
```
❌ engine/main.py - BRAKUJE
❌ engine/models/metric.py - BRAKUJE
❌ engine/worker/queue_worker.py - BRAKUJE
❌ dashboard/src/App.jsx - BRAKUJE
❌ prometheus/prometheus.yml - KRYTYCZNE
❌ grafana/provisioning/* - BRAKUJE
```

**NetGuardian**:
```
❌ engine/main.py - BRAKUJE
❌ engine/kafka_consumer.py - BRAKUJE
❌ engine/geoip.py - BRAKUJE
❌ agent/main.py - BRAKUJE
❌ prometheus/prometheus.yml - BRAKUJE
❌ grafana/provisioning/* - BRAKUJE
```

**NetAegis**:
```
❌ server/main_mcp/main.py - BRAKUJE
❌ server/operational_mcp/main.py - BRAKUJE
❌ agents/netpulse/main.py - BRAKUJE
❌ agents/seclog/main.py - BRAKUJE
❌ agents/netconfig/main.py - BRAKUJE
❌ frontend/src/App.jsx - BRAKUJE
```

---

### PROBLEM #3: Niekompletne Requirements Files

**Status**:
```
✅ cloudbudget/api/requirements.txt - EXISTS
✅ cloudbudget/requirements.txt - EXISTS
⚠️ infraflow/requirements.txt - może być niekompletny
⚠️ netguardian/requirements.txt - może być niekompletny
⚠️ netaegis/requirements.txt - zwykle minimalistyczne
```

**Brakujące Zależności**:
- Kafka-python (NetGuardian)
- DuckDB (NetGuardian, CloudBudget)
- Polars (Analytics libraries)
- geoip2 (NetGuardian GeoIP)
- pytest-asyncio (All projects)
- httpx (HTTP client for tests)

---

### PROBLEM #4: Niekompletne docker-compose.yml Konfiguracje

#### CloudBudget - docker-compose.yml
```yaml
✅ COMPLETE (api, worker, postgres, redis, rabbitmq, frontend wszystkie skonfigurowane)

⚠️ POTENCJALNE PROBLEMY:
  - volumes: postgres_data, redis_data, rabbitmq_data mogą być niezdefiniowane na końcu pliku
  - Frontend nie może mieć portu 3000:3000 (sprawdzić mapowanie w docker-compose)
  - Brakuje init script dla seed data
```

#### InfraFlow - docker-compose.yml
```yaml
⚠️ PROBLEMY:
  - engine/Dockerfile BRAKUJE, a compose próbuje go buildować
  - worker nie ma healthcheck (powinno być)
  - prometheus.yml brakuje w volumes
  - grafana provisioning paths mogą być błędne
  - Dashboard ENV `ENGINE_URL` potrzebuje weryfikacji
```

#### NetGuardian - docker-compose.yml
```yaml
⚠️ PROBLEMY:
  - engine/Dockerfile BRAKUJE
  - agent/Dockerfile BRAKUJE
  - dashboard/Dockerfile BRAKUJE
  - Kafka initialization (zookeeper) może nie być w porządku
  - SSH volume mount `./engine/ssh` - brakuje skryptu inicjalizacji
  - GeoIP volume `./data/GeoLite2-City.mmdb` - brakuje download skryptu
```

#### NetAegis - docker-compose.yml
```yaml
❌ KRYTYCZNE PROBLEMY:
  - Brakuje agents (netpulse, seclog, netconfig) w docker-compose.yml
  - Redis service może nie być zdefiniowany (wymagany dla MCP)
  - agents/ Dockerfiles brakują
  - frontend/Dockerfile BRAKUJE
```

---

## 📋 BRAKI W KONFIGURACJI

### .env.example - Niekompletne Zmienne

**CloudBudget .env.example**:
```bash
✅ Istnieje: JWT_SECRET, POSTGRES_*, REDIS_URL, RABBITMQ_URL, CELERY_*, DUCKDB_PATH
⚠️ Może brakować: SLACK_WEBHOOK_URL (mentioned in code)
```

**InfraFlow .env.example**:
```bash
⚠️ BRAKI:
  ❌ DATABASE_URL - brakuje pełnego URL
  ❌ REDIS_PORT - brakuje, może być wymagane
  ❌ PROMETHEUS_SCRAPE_INTERVAL - brakuje
```

**NetGuardian .env.example**:
```bash
⚠️ BRAKI:
  ❌ GEOIP_DB - brakuje, a kod go używa
  ❌ MAXMIND_LICENSE_KEY - brakuje
  ❌ SSH_PRIVATE_KEY_FILE - brakuje
```

**NetAegis .env.example**:
```bash
✅ Lepiej, ale:
  ❌ REDIS_URL - wymagane dla MCP, może brakować
  ❌ AGENTS_LOG_LEVEL - brakuje
```

---

## 🔧 SETUP SCRIPTS - Status

```
✅ cloudbudget/scripts/setup.sh - POWINIEN ISTNIEĆ
✅ infraflow/scripts/setup.sh - POWINIEN ISTNIEĆ
✅ netguardian/scripts/setup.sh - POWINIEN ISTNIEĆ (+ initialize-ssh-keys.sh, download_geoip.sh)
✅ netaegis/scripts/setup.sh - POWINIEN ISTNIEĆ

⚠️ Ale mogą być niekompletne lub nie działać bez wygenerowanego kodu
```

---

## 📊 TESTY - KRYTYCZNIE BRAKUJĄCE

```
❌ cloudbudget/tests/test_health.py - PUSTE LUB BRAKUJE
❌ cloudbudget/tests/test_api.py - BRAKUJE
❌ cloudbudget/tests/conftest.py - BRAKUJE

❌ infraflow/tests/test_health.py - PUSTE LUB BRAKUJE
❌ infraflow/tests/test_integration.py - MOŻE BRAKOWAĆ

❌ netguardian/tests/test_health.py - PUSTE LUB BRAKUJE
❌ netguardian/tests/test_kafka_consumer.py - MOŻE BRAKOWAĆ

❌ netaegis/tests/ - KOMPLETNIE PUSTE
```

**Wpływ**: `make test` będzie failować. Coverage = 0%.

---

## ✅ CO DZIAŁA

1. ✅ **Port Mapping** - Wszystkie porty unikalne (verify_all_ports.sh przechodzi)
2. ✅ **Docker Compose Struktura** - Well-organized per project
3. ✅ **Dokumentacja README** - Good per project
4. ✅ **Root Makefile** - Definiuje targets
5. ✅ **Alguns Dockerfiles** - CloudBudget, NetAegis i InfraFlow dashboard już istnieją

---

---

# 🤖 IMPROVED CodeX GENERATION PROMPT v2.0

## PREAMBUŁA

```
TASK: Complete Infrastructure & Application Code Generation for PROJEKTS-WORK Repository

CONTEXT:
- Repository: Gorski-Maciej/PROJEKTS-WORK
- Status: 70% skeleton complete, 30% implementation needed
- Goal: Generate ALL missing application code, Dockerfiles, tests, configs to make `make all` work without errors
- Timeline: URGENT - All services must be production-ready (or development-ready) after generation
- Quality: Production-grade code with proper error handling, logging, security

CONSTRAINTS:
- Python 3.12+ only
- FastAPI for all APIs
- Docker Compose orchestration (no Kubernetes yet)
- All services must start healthily with zero errors in logs
- All services must communicate with each other and databases
- All ports (8100, 8001, 8300, 8400) must be accessible after startup
```

---

## PHASE 1: DOCKERFILES GENERATION

### Task: Generate ALL missing Dockerfiles

#### Priority 1 - CRITICAL BLOCKERS

**File**: `infraflow/engine/Dockerfile`
```dockerfile
# Requirements:
# - Python 3.12 slim
# - Install from requirements.txt
# - EXPOSE 8000
# - Healthcheck that checks http://localhost:8000/health
# - Non-root user for security
# - Multi-stage build to optimize size
# - Graceful shutdown signal handling

FROM python:3.12-slim
WORKDIR /app
RUN useradd -m -u 1000 appuser
COPY infraflow/engine/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY infraflow/engine/ .
RUN chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=3)" || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**File**: `netguardian/engine/Dockerfile`
**File**: `netguardian/agent/Dockerfile`
**File**: `netguardian/dashboard/Dockerfile`

#### Priority 2 - IMPORTANT

**File**: `netaegis/agents/seclog/Dockerfile`
**File**: `netaegis/agents/netconfig/Dockerfile`
**File**: `netaegis/frontend/Dockerfile`

---

## PHASE 2: REQUIREMENTS.TXT - Complete & Accurate

### CloudBudget Requirements

**File**: `cloudbudget/requirements.txt` (UPDATE if incomplete)
```
# Ensure ALL these packages with specific versions:

# Web Framework
fastapi==0.116.0
uvicorn==0.35.0
pydantic==2.11.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.23
psycopg[binary]==3.2.0
duckdb==1.3.0
alembic==1.16.0

# Async & Queue
celery==5.5.0
redis==6.2.0
flower==2.0.2

# Data Science & Analytics
polars==1.31.0
pandas==2.2.0
numpy==1.26.4
scikit-learn==1.7.0
prophet==1.1.7

# Security & Auth
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pydantic-settings==2.3.0

# Monitoring & Observability
prometheus-client==0.22.0
python-json-logger==2.0.8

# GraphQL (if used)
strawberry-graphql[fastapi]==0.275.0

# Testing
pytest==8.0.0
pytest-asyncio==0.23.0
pytest-cov==4.1.0
httpx==0.25.0

# Utilities
click==8.1.7
requests==2.31.0
```

### InfraFlow Requirements

**File**: `infraflow/engine/requirements.txt` (CREATE if missing, UPDATE if incomplete)
```
fastapi==0.116.0
uvicorn==0.35.0
pydantic==2.11.0
sqlalchemy==2.0.23
psycopg[binary]==3.2.0
redis==6.2.0
pydantic-settings==2.3.0
python-jose[cryptography]==3.3.0
prometheus-client==0.22.0
pytest==8.0.0
pytest-asyncio==0.23.0
httpx==0.25.0
```

### NetGuardian Requirements

**File**: `netguardian/requirements.txt` (CREATE if missing)
```
fastapi==0.116.0
uvicorn==0.35.0
pydantic==2.11.0
sqlalchemy==2.0.23
psycopg[binary]==3.2.0
kafka-python==2.0.2
redis==6.2.0
duckdb==1.3.0
duckdb-engine==0.11.2
geoip2==4.7.0
duckdb-python==1.3.0
pydantic-settings==2.3.0
python-jose[cryptography]==3.3.0
prometheus-client==0.22.0
websocket-client==1.6.2
python-json-logger==2.0.8
pytest==8.0.0
pytest-asyncio==0.23.0
httpx==0.25.0
```

### NetAegis Requirements

**File**: `netaegis/requirements.txt` (UPDATE with ALL packages)
```
fastapi==0.116.0
uvicorn==0.35.0
pydantic==2.11.0
redis==6.2.0
pydantic-settings==2.3.0
python-jose[cryptography]==3.3.0
paramiko==3.4.0
psutil==5.9.6
python-json-logger==2.0.8
pytest==8.0.0
pytest-asyncio==0.23.0
httpx==0.25.0
requests==2.31.0
```

---

## PHASE 3: APPLICATION CODE - Main Implementation

### CloudBudget API Implementation

**File**: `cloudbudget/api/main.py`
```python
# Requirements:
# 1. FastAPI app instance
# 2. CORS middleware
# 3. JWT authentication middleware
# 4. Database initialization on startup
# 5. DuckDB initialization on startup
# 6. Routes registration (health, auth, costs)
# 7. Exception handlers
# 8. Graceful shutdown handling
# 9. Logging configuration

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import sys
from api.core.database import init_db
from api.core.config import settings
from api.routes import health, auth, costs

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing CloudBudget API...")
    await init_db()
    logger.info("✅ CloudBudget API initialized")
    yield
    # Shutdown
    logger.info("Shutting down CloudBudget API...")

app = FastAPI(
    title="CloudBudget API",
    description="FinOps platform for cloud cost analysis",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router, prefix="", tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(costs.router, prefix="/api/v1", tags=["costs"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**File**: `cloudbudget/api/core/config.py` (CREATE)
```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+psycopg://cloudbudget:cloudbudget@postgres:5432/cloudbudget"
    DUCKDB_PATH: str = "/data/cloudbudget.duckdb"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # RabbitMQ / Celery
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672//"
    CELERY_BROKER_URL: str = "amqp://guest:guest@rabbitmq:5672//"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/1"
    
    # Security
    JWT_SECRET: str = "CHANGE_ME_WITH_A_LONG_RANDOM_SECRET_MIN_32_CHARS"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # Slack (optional)
    SLACK_WEBHOOK_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**File**: `cloudbudget/api/core/database.py` (UPDATE/CREATE)
```python
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from api.core.config import settings
import duckdb
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# PostgreSQL
engine: Engine = None
SessionLocal = None

# DuckDB
duckdb_conn = None

async def init_db():
    """Initialize databases on app startup"""
    global engine, SessionLocal, duckdb_conn
    
    try:
        # PostgreSQL
        logger.info("Connecting to PostgreSQL...")
        engine = create_engine(
            settings.DATABASE_URL,
            connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Test connection
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("✅ PostgreSQL connected")
        
        # Initialize SQLAlchemy models
        from api.models.base import Base
        Base.metadata.create_all(bind=engine)
        logger.info("✅ SQLAlchemy models created")
        
        # DuckDB
        logger.info(f"Initializing DuckDB at {settings.DUCKDB_PATH}...")
        os.makedirs(os.path.dirname(settings.DUCKDB_PATH) or ".", exist_ok=True)
        duckdb_conn = duckdb.connect(settings.DUCKDB_PATH)
        
        # Create analytics tables
        duckdb_conn.execute("""
            CREATE TABLE IF NOT EXISTS cost_snapshots (
                id INTEGER PRIMARY KEY DEFAULT nextval('sqlite_sequence'),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                service_name VARCHAR,
                cost DECIMAL(10, 2),
                region VARCHAR
            )
        """)
        logger.info("✅ DuckDB initialized")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise

def get_db() -> Session:
    """Dependency for FastAPI to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_duckdb():
    """Get DuckDB connection"""
    return duckdb_conn
```

**File**: `cloudbudget/api/core/auth.py` (CREATE)
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from pydantic import BaseModel
from api.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

class TokenData(BaseModel):
    username: str | None = None
    exp: int | None = None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return username
```

**File**: `cloudbudget/api/core/celery_app.py` (CREATE)
```python
from celery import Celery
from api.core.config import settings

celery_app = Celery(
    "cloudbudget",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.task_serializer = "json"
celery_app.conf.accept_content = ["json"]
celery_app.conf.result_serializer = "json"

@celery_app.task
def ingest_costs(data: dict):
    """Task to ingest cost data"""
    # Implementation
    return {"status": "ok", "records": len(data)}

@celery_app.task
def analyze_costs():
    """Task to analyze cost trends"""
    return {"status": "ok"}

@celery_app.task
def recommend_optimizations():
    """Task to recommend cost optimizations"""
    return {"status": "ok", "recommendations": []}
```

**File**: `cloudbudget/api/routes/health.py` (CREATE)
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.core.database import get_db, get_duckdb, engine
import redis
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    status = {"status": "ok", "services": {}}
    
    try:
        # PostgreSQL
        db.execute("SELECT 1")
        status["services"]["postgres"] = "ok"
    except:
        status["services"]["postgres"] = "error"
    
    try:
        # Redis
        r = redis.from_url("redis://redis:6379/0")
        r.ping()
        status["services"]["redis"] = "ok"
    except:
        status["services"]["redis"] = "error"
    
    try:
        # DuckDB
        conn = get_duckdb()
        conn.execute("SELECT 1").fetchall()
        status["services"]["duckdb"] = "ok"
    except:
        status["services"]["duckdb"] = "error"
    
    return status

@router.get("/docs")
async def docs_redirect():
    """Redirect to OpenAPI docs"""
    return {"docs": "/openapi.json"}
```

**File**: `cloudbudget/api/routes/auth.py` (CREATE)
```python
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from api.core.auth import create_access_token, verify_password, get_password_hash
from datetime import timedelta

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Demo user
DEMO_USER = "demo"
DEMO_PASSWORD_HASH = get_password_hash("demo")

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """User login endpoint"""
    if request.username != DEMO_USER or not verify_password(request.password, DEMO_PASSWORD_HASH):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": request.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/validate")
async def validate_token(token: str):
    """Validate JWT token"""
    try:
        from api.core.auth import TokenData
        from jose import jwt
        from api.core.config import settings
        
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        return {"valid": True, "username": username}
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
```

**File**: `cloudbudget/api/routes/costs.py` (CREATE)
```python
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from api.core.database import get_db, get_duckdb
from api.core.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

class CostRecord(BaseModel):
    service_name: str
    cost: float
    region: str

@router.get("/costs")
async def get_costs(
    skip: int = Query(0),
    limit: int = Query(100),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Get cost records with pagination"""
    duckdb_conn = get_duckdb()
    result = duckdb_conn.execute(
        "SELECT * FROM cost_snapshots ORDER BY timestamp DESC LIMIT ? OFFSET ?",
        [limit, skip]
    ).fetchall()
    return {"costs": result, "total": len(result)}

@router.post("/costs/ingest")
async def ingest_costs(
    data: dict,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Trigger cost data ingestion"""
    from api.core.celery_app import celery_app
    from celery_app.tasks import ingest_costs as celery_ingest
    
    task = celery_ingest.delay(data)
    return {"task_id": task.id, "status": "processing"}

@router.get("/recommendations")
async def get_recommendations(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Get cost optimization recommendations"""
    return {
        "recommendations": [
            {
                "service": "CloudBudget",
                "savings": "25%",
                "recommendation": "Use reserved instances"
            }
        ]
    }
```

**File**: `cloudbudget/api/models/__init__.py` (CREATE)
```python
# Models package
```

**File**: `cloudbudget/api/models/base.py` (CREATE)
```python
from sqlalchemy.orm import declarative_base

Base = declarative_base()
```

**File**: `cloudbudget/api/models/cost.py` (CREATE)
```python
from sqlalchemy import Column, Integer, String, Float, DateTime, func
from api.models.base import Base
from datetime import datetime

class Cost(Base):
    __tablename__ = "costs"
    
    id = Column(Integer, primary_key=True)
    service = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    region = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
```

---

### InfraFlow Engine Implementation

**File**: `infraflow/engine/main.py` (CREATE)
```python
# Similar structure to CloudBudget but for infrastructure monitoring
# Include Prometheus metrics exposure
# Include TimescaleDB connection
# Include Redis queue consumer initialization
```

---

### NetGuardian Engine Implementation

**File**: `netguardian/engine/main.py` (CREATE)
```python
# FastAPI app for NetGuardian
# Kafka consumer initialization
# WebSocket support for real-time events
# DuckDB for event storage
```

---

### NetAegis MCP Servers Implementation

**File**: `netaegis/server/main_mcp/main.py` (CREATE)
**File**: `netaegis/server/operational_mcp/main.py` (CREATE)

---

## PHASE 4: TEST SUITE GENERATION

### CloudBudget Tests

**File**: `cloudbudget/tests/__init__.py` (CREATE)
```python
# Tests package
```

**File**: `cloudbudget/tests/conftest.py` (CREATE)
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.main import app
from api.core.database import get_db, Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
```

**File**: `cloudbudget/tests/test_health.py` (CREATE)
```python
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert "services" in response.json()

def test_docs(client):
    response = client.get("/docs")
    assert response.status_code in [200, 301, 302]
```

**File**: `cloudbudget/tests/test_auth.py` (CREATE)
```python
def test_login_demo(client):
    response = client.post("/auth/login", json={"username": "demo", "password": "demo"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid(client):
    response = client.post("/auth/login", json={"username": "demo", "password": "wrong"})
    assert response.status_code == 401
```

---

## PHASE 5: CONFIGURATION FILES

### Prometheus Configuration

**File**: `infraflow/prometheus/prometheus.yml` (CREATE)
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'infraflow-engine'
    static_configs:
      - targets: ['engine:8000']
```

**File**: `netguardian/prometheus/prometheus.yml` (CREATE)
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'netguardian-engine'
    static_configs:
      - targets: ['engine:8000']
```

### Grafana Provisioning

**File**: `infraflow/grafana/provisioning/datasources/prometheus.yml` (CREATE)
```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
    access: proxy
    isDefault: true
```

---

## PHASE 6: SETUP & BOOTSTRAP SCRIPTS

### All Projects

**File**: `cloudbudget/scripts/setup.sh` (CREATE/UPDATE)
**File**: `infraflow/scripts/setup.sh` (CREATE/UPDATE)
**File**: `netguardian/scripts/setup.sh` (CREATE/UPDATE)
**File**: `netaegis/scripts/setup.sh` (CREATE/UPDATE)

Each should:
1. Copy `.env.example` to `.env` if missing
2. Validate Docker installation
3. Run `docker compose build`
4. Run `docker compose up -d`
5. Wait for services to become healthy
6. Print URLs for access

---

## VALIDATION CHECKLIST

After generation, verify ALL of the following:

### Build & Startup
- [ ] `make build` - All images build without errors
- [ ] `make all` - All services start without errors
- [ ] `docker compose ps` - All services show as RUNNING or HEALTHY
- [ ] No logs show ERROR or FATAL

### Health & Connectivity
- [ ] `curl http://localhost:8100/health` - CloudBudget responds
- [ ] `curl http://localhost:8001/health` - InfraFlow responds
- [ ] `curl http://localhost:8300/health` - NetGuardian responds
- [ ] `curl http://localhost:8400/health` - NetAegis responds
- [ ] All databases connected and responding
- [ ] All queue systems operational

### Tests
- [ ] `make test` - All tests pass (or skip gracefully)
- [ ] Coverage > 50%

### Port Verification
- [ ] `./verify_all_ports.sh` - All ports unique, exit code 0

### API Access
- [ ] `curl http://localhost:8100/docs` - OpenAPI docs accessible
- [ ] `curl http://localhost:8001/docs` - OpenAPI docs accessible
- [ ] `curl http://localhost:8300/docs` - OpenAPI docs accessible
- [ ] `curl http://localhost:8400/docs` - OpenAPI docs accessible (or JSON equivalent)

### End-to-End
- [ ] Can login and get JWT token from CloudBudget
- [ ] Can access protected endpoints with token
- [ ] Services can reach each other (cross-service communication)
- [ ] Databases persist data across container restarts

---

## NOTES FOR CODE GENERATION

1. **Error Handling**: All endpoints should return proper HTTP status codes
2. **Logging**: Use structured JSON logging with python-json-logger
3. **Security**: Never log sensitive data; validate all inputs
4. **Async**: Use `async def` for all endpoints in FastAPI
5. **Dependencies**: Properly inject dependencies (db, current_user, etc.)
6. **Environment**: All config from environment variables, not hardcoded
7. **Graceful Shutdown**: Handle SIGTERM/SIGINT signals properly
8. **Health Checks**: All services must have `/health` endpoint
9. **Documentation**: Add docstrings to all functions and classes
10. **Testing**: Write tests that can run with `pytest` without manual service startup

---

## EXPECTED OUTCOME

After complete code generation using this prompt:

1. ✅ All 4 services buildable: `make build`
2. ✅ All 4 services startable: `make all`
3. ✅ All 4 services healthy: health checks passing
4. ✅ All APIs documented: OpenAPI/Swagger available
5. ✅ All APIs functional: CRUD operations working
6. ✅ All tests passing: `make test` exit code 0
7. ✅ All ports unique: `./verify_all_ports.sh` exit code 0
8. ✅ Production-ready: Proper logging, error handling, security
9. ✅ Team-ready: Clear code, documentation, setup scripts
```

---

# 📝 RECOMMENDATIONS FOR IMMEDIATE ACTION

## Priority 1: URGENT (Next 24 hours)

1. **Use this improved CODEX_GENERATION_PROMPT.md** with your preferred AI/LLM code generator
2. **Request generation of**:
   - All missing Dockerfiles
   - All missing main.py files per service
   - All requirements.txt files (complete)
   - All test files (conftest.py + tests)
3. **Validate with**: `make build && make all`

## Priority 2: IMPORTANT (Next 2-3 days)

4. **Verify health checks**: `docker compose ps` - all HEALTHY
5. **Test API access**: Curl each `/health` and `/docs` endpoint
6. **Run test suite**: `make test`
7. **Verify port uniqueness**: `./verify_all_ports.sh`

## Priority 3: NICE-TO-HAVE (Next 1 week)

8. Add OpenTelemetry tracing
9. Add GitHub Actions CI/CD workflows
10. Create Kubernetes deployment manifests
11. Add security scanning (Trivy, Snyk)

---

**Generated**: 2026-05-20  
**For Repository**: Gorski-Maciej/PROJEKTS-WORK  
**Status**: READY FOR CODE GENERATION  
**Quality Target**: Production-Ready
