# CloudBudget 2.0 – Autonomous FinOps Platform

![FinOps](https://img.shields.io/badge/FinOps-optimized-blue)

CloudBudget 2.0 to samodzielna platforma FinOps, która nie tylko monitoruje koszty wielu chmur (AWS, Azure, GCP, on‑premise), ale aktywnie proponuje optymalizacje, prognozuje przyszłe wydatki i automatycznie wykonuje zaakceptowane rekomendacje. System łączy nowoczesny frontend (Next.js) z zaawansowanym backendem analitycznym (FastAPI, DuckDB, Prophet).

## 🚀 Kluczowe cechy
- **Multi‑cloud cost aggregation** – dane z AWS, Azure, GCP i Kubernetes w jednym miejscu
- **Inteligentne rekomendacje** – idle resources, unattached volumes, rightsizing, RI/Savings Plans
- **Symulacje What‑If** – migracja między chmurami, zmiana typu instancji, analiza kosztów przed wdrożeniem
- **Automatyczne akcje (AutoPilot)** – samoczynne zatrzymywanie nieużywanych zasobów po okresie akceptacji
- **Predykcja kosztów** – Prophet z sezonowością i alertami o przekroczeniu budżetu
- **OCR faktur** – ekstrakcja danych z PDF za pomocą Tesseract + LLM
- **Wielodostępność** – izolacja danych per tenant (Row‑Level Security)
- **Monitoring** – Prometheus + Grafana + Alertmanager

## 📦 Technologie
- **Backend:** FastAPI, Celery, RabbitMQ, PostgreSQL, DuckDB, Redis
- **Analityka:** Polars, dbt, Prophet, Isolation Forest
- **Frontend:** Next.js 14, React, TailwindCSS, Tremor, GraphQL
- **DevOps:** Docker Compose, Kubernetes, Helm, Pulumi, GitHub Actions
- **Bezpieczeństwo:** Keycloak, HashiCorp Vault, Trivy, OWASP ZAP

## ⚡ Szybki start
```bash
cd cloudbudget
cp .env.example .env
bash scripts/setup.sh
```
